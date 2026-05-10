from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.dependencies import get_current_user
from app.utils.supabase_client import get_admin_client
from app.utils.encryption import encrypt

router = APIRouter()

class ProfileUpdate(BaseModel):
    display_name: str | None = None
    educational_level: str | None = None
    background_domain: str | None = None
    preferred_language: str | None = None
    default_chunking: str | None = None
    default_scaffolding: str | None = None
    default_media_mix: dict | None = None
    default_pacing: str | None = None
    tutor_tone: str | None = None
    tutor_pace: str | None = None
    tutor_register: str | None = None
    learning_philosophy: str | None = None

class ApiKeyUpdate(BaseModel):
    api_key: str


@router.get("/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    result = db.table("profiles").select("*").eq("id", current_user["user_id"]).single().execute()
    if not result.data:
        # Create profile on first access
        db.table("profiles").insert({"id": current_user["user_id"]}).execute()
        result = db.table("profiles").select("*").eq("id", current_user["user_id"]).single().execute()
    # Never return the encrypted key
    profile = result.data
    profile.pop("claude_api_key", None)
    return profile


@router.put("/me")
async def update_profile(update: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    db.table("profiles").upsert({"id": current_user["user_id"], **data}).execute()
    return {"status": "updated"}


@router.put("/me/api-key")
async def update_api_key(update: ApiKeyUpdate, current_user: dict = Depends(get_current_user)):
    if not update.api_key.startswith("sk-ant-"):
        raise HTTPException(status_code=400, detail="Invalid API key format")
    db = get_admin_client()
    encrypted = encrypt(update.api_key)
    db.table("profiles").upsert({"id": current_user["user_id"], "claude_api_key": encrypted}).execute()
    return {"status": "updated"}


@router.get("/me/api-key-status")
async def api_key_status(current_user: dict = Depends(get_current_user)):
    db = get_admin_client()
    result = db.table("profiles").select("claude_api_key").eq("id", current_user["user_id"]).single().execute()
    has_key = bool(result.data and result.data.get("claude_api_key"))
    return {"has_api_key": has_key}
