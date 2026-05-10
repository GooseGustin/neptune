from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from app.dependencies import get_current_user
from app.utils.supabase_client import get_admin_client
from app.services.generation import generate_harness_core, generate_module_content
from app.models.harness import Harness, CoreModule

router = APIRouter()

class HarnessRequest(BaseModel):
    intent: str
    delivery_path: str
    timeline: str | None = None

class CreateCourseRequest(BaseModel):
    harness: dict
    track_layer: dict

class CompleteLessonRequest(BaseModel):
    module_id: str
    attempts: int
    final_score: float | None
    passed: bool


def _get_user_profile(user_id: str) -> dict:
    db = get_admin_client()
    result = db.table("profiles").select("*").eq("id", user_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Profile not found. Complete settings first.")
    return result.data


@router.post("/harness")
async def generate_harness(req: HarnessRequest, current_user: dict = Depends(get_current_user)):
    profile = _get_user_profile(current_user["user_id"])
    if not profile.get("claude_api_key"):
        raise HTTPException(status_code=400, detail="Claude API key not configured in settings.")

    harness_core = await generate_harness_core(
        encrypted_api_key=profile["claude_api_key"],
        intent=req.intent,
        delivery_path=req.delivery_path,
        background_domain=profile.get("background_domain", "general knowledge"),
        educational_level=profile.get("educational_level", "undergraduate"),
        timeline=req.timeline,
    )
    return {"harness_draft": harness_core}


@router.post("")
async def create_course(req: CreateCourseRequest, current_user: dict = Depends(get_current_user)):
    profile = _get_user_profile(current_user["user_id"])
    db = get_admin_client()

    harness_obj = Harness(**{"core": req.harness, "track": req.track_layer})
    first_module_def = harness_obj.core.modules[0]

    first_module = await generate_module_content(
        encrypted_api_key=profile["claude_api_key"],
        harness=harness_obj,
        module=first_module_def,
        background_domain=profile.get("background_domain", "general"),
        learning_philosophy=profile.get("learning_philosophy", "direct_instruction"),
    )

    course_data = {
        "user_id": current_user["user_id"],
        "title": harness_obj.core.course_title,
        "terminal_objective": harness_obj.core.terminal_objective,
        "delivery_path": req.track_layer.get("path", "marathon"),
        "harness": harness_obj.model_dump(),
        "modules_generated": 1,
        "status": "active",
        "target_completion_date": None,
    }
    result = db.table("courses").insert(course_data).execute()
    course = result.data[0]

    return {"course_id": course["id"], "first_module": first_module.model_dump()}


@router.get("")
async def list_courses(current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    result = db.table("courses").select("id,title,delivery_path,status,modules_generated,created_at") \
               .eq("user_id", current_user["user_id"]).order("created_at", desc=True).execute()
    return {"courses": result.data}


@router.get("/{course_id}")
async def get_course(course_id: str, current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    result = db.table("courses").select("*").eq("id", course_id).eq("user_id", current_user["user_id"]).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Course not found")
    return result.data


@router.post("/{course_id}/modules/{module_id}/generate")
async def generate_module(course_id: str, module_id: str, current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    course_result = db.table("courses").select("*").eq("id", course_id).eq("user_id", current_user["user_id"]).single().execute()
    if not course_result.data:
        raise HTTPException(status_code=404, detail="Course not found")

    course = course_result.data
    if course["modules_generated"] >= 10:
        raise HTTPException(status_code=402, detail="GENERATION_LIMIT_REACHED")

    profile = _get_user_profile(current_user["user_id"])
    harness = Harness(**course["harness"])

    module_def = next((m for m in harness.core.modules if m.module_id == module_id), None)
    if not module_def:
        raise HTTPException(status_code=404, detail="Module not found in harness")

    generated = await generate_module_content(
        encrypted_api_key=profile["claude_api_key"],
        harness=harness,
        module=module_def,
        background_domain=profile.get("background_domain", "general"),
        learning_philosophy=profile.get("learning_philosophy", "direct_instruction"),
    )

    db.table("courses").update({"modules_generated": course["modules_generated"] + 1}).eq("id", course_id).execute()
    return {"module": generated.model_dump()}


@router.get("/{course_id}/progress")
async def get_progress(course_id: str, current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    result = db.table("lesson_completions").select("*") \
               .eq("course_id", course_id).eq("user_id", current_user["user_id"]).execute()
    return {"completions": result.data}


@router.post("/{course_id}/lessons/{lesson_id}/complete")
async def complete_lesson(course_id: str, lesson_id: str, req: CompleteLessonRequest, current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    # Check for existing completion
    existing = db.table("lesson_completions").select("id") \
                 .eq("course_id", course_id).eq("lesson_id", lesson_id).eq("user_id", current_user["user_id"]).execute()

    data = {
        "course_id": course_id,
        "user_id": current_user["user_id"],
        "lesson_id": lesson_id,
        "module_id": req.module_id,
        "attempts": req.attempts,
        "final_score": req.final_score,
        "passed": req.passed,
        "completed_at": datetime.utcnow().isoformat(),
    }

    if existing.data:
        db.table("lesson_completions").update(data).eq("id", existing.data[0]["id"]).execute()
    else:
        db.table("lesson_completions").insert(data).execute()

    return {"status": "ok"}
