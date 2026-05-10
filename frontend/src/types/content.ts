export type ContentPieceType = 'text' | 'video' | 'audio' | 'flashcard_set' | 'quiz'

export interface TextContent { body: string }
export interface VideoContent { url: string; title: string; caption: string }
export interface AudioContent { url: string; title: string; duration_seconds: number }
export interface FlashCard { card_id: string; front: string; back: string }
export interface FlashcardSetContent { cards: FlashCard[] }
export type QuestionType = 'multiple_choice' | 'true_false'
export interface QuizQuestion {
  question_id: string
  question_text: string
  type: QuestionType
  options?: string[]
  correct_answer: string
  explanation: string
}
export interface QuizContent { questions: QuizQuestion[] }

export interface ContentPiece {
  type: ContentPieceType
  content: TextContent | VideoContent | AudioContent | FlashcardSetContent | QuizContent
}

export interface Section {
  section_id: string
  section_title: string
  content_pieces: ContentPiece[]
}

export interface GeneratedLesson {
  lesson_id: string
  lesson_title: string
  sections: Section[]
  validation: {
    type: 'multiple_choice' | 'true_false' | 'mark_complete'
    questions?: QuizQuestion[]
  }
}

export interface GeneratedModule {
  module_id: string
  module_title: string
  lessons: GeneratedLesson[]
}
