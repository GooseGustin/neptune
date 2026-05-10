from pydantic import BaseModel
from typing import Optional, Literal

class ValidationGate(BaseModel):
    type: Literal["multiple_choice", "true_false", "mark_complete"]
    pass_threshold: float = 0.8
    question_count: int = 5

class CoreLesson(BaseModel):
    lesson_id: str
    lesson_title: str
    order: int
    prerequisites: list[str] = []
    validation: ValidationGate

class CoreModule(BaseModel):
    module_id: str
    module_title: str
    order: int
    lessons: list[CoreLesson]

class CoreLayer(BaseModel):
    course_title: str
    terminal_objective: str
    estimated_weeks: int
    modules: list[CoreModule]

class MediaMix(BaseModel):
    video: int = 40
    interactive: int = 40
    text: int = 20

class TutorPersona(BaseModel):
    pace: str = "steady"
    tone: str = "direct"
    register: str = "practitioner"

class TrackLayer(BaseModel):
    path: str
    scaffolding: str = "guided"
    gating: str = "strict"
    chunking: str = "standard"
    media_mix: MediaMix = MediaMix()
    pacing_mode: str = "steady"
    feedback_style: str = "direct"
    assessment_preference: str = "mixed"
    tutor: TutorPersona = TutorPersona()
    session_cap_minutes: int = 60
    srs_enabled: bool = True

class Harness(BaseModel):
    core: CoreLayer
    track: TrackLayer
