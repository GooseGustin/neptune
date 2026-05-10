from pydantic import BaseModel
from typing import Optional, Literal, Union

class TextContent(BaseModel):
    body: str

class VideoContent(BaseModel):
    url: str
    title: str
    caption: str = ""

class AudioContent(BaseModel):
    url: str
    title: str
    duration_seconds: int = 0

class FlashCard(BaseModel):
    card_id: str
    front: str
    back: str

class FlashcardSetContent(BaseModel):
    cards: list[FlashCard]

class QuizQuestion(BaseModel):
    question_id: str
    question_text: str
    type: Literal["multiple_choice", "true_false"]
    options: Optional[list[str]] = None
    correct_answer: str
    explanation: str

class QuizContent(BaseModel):
    questions: list[QuizQuestion]

class ContentPiece(BaseModel):
    type: Literal["text", "video", "audio", "flashcard_set", "quiz"]
    content: Union[TextContent, VideoContent, AudioContent, FlashcardSetContent, QuizContent]

class Section(BaseModel):
    section_id: str
    section_title: str
    content_pieces: list[ContentPiece]

class LessonValidation(BaseModel):
    type: Literal["multiple_choice", "true_false", "mark_complete"]
    questions: Optional[list[QuizQuestion]] = None

class GeneratedLesson(BaseModel):
    lesson_id: str
    lesson_title: str
    sections: list[Section]
    validation: LessonValidation

class GeneratedModule(BaseModel):
    module_id: str
    module_title: str
    lessons: list[GeneratedLesson]
