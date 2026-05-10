import type { Harness } from './harness'

export type CourseStatus = 'active' | 'complete' | 'archived'

export interface Course {
  id: string
  user_id: string
  title: string
  terminal_objective: string | null
  delivery_path: string
  harness: Harness
  modules_generated: number
  status: CourseStatus
  target_completion_date: string | null
  created_at: string
  updated_at: string
}

export interface LessonCompletion {
  id: string
  course_id: string
  lesson_id: string
  module_id: string
  completed_at: string
  attempts: number
  final_score: number | null
  passed: boolean
}

export interface UserProfile {
  id: string
  display_name: string | null
  educational_level: string | null
  background_domain: string | null
  preferred_language: string
  default_chunking: string
  default_scaffolding: string
  default_media_mix: { video: number; interactive: number; text: number }
  default_pacing: string
  tutor_tone: string
  tutor_pace: string
  tutor_register: string
  learning_philosophy: string
  claude_api_key: string | null
  created_at: string
  updated_at: string
}
