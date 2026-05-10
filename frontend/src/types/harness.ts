export type ValidationGateType = 'multiple_choice' | 'true_false' | 'mark_complete'
export type GatingModel = 'strict' | 'advisory' | 'open_world'
export type ScaffoldingLevel = 'full_scaffold' | 'guided' | 'prompted' | 'raw_mode'
export type ChunkingDensity = 'micro_atomic' | 'compact' | 'standard' | 'academic'
export type PacingMode = 'sprint' | 'steady' | 'flexible' | 'immersion'
export type TutorTone = 'formal' | 'direct' | 'conversational' | 'energetic'
export type TutorPace = 'slow' | 'steady' | 'fast'
export type TutorRegister = 'fundamentals' | 'practitioner' | 'expert_peer'
export type FeedbackStyle = 'direct' | 'explanatory' | 'socratic' | 'encouraging'
export type AssessmentPreference = 'drill_heavy' | 'project_anchored' | 'mixed' | 'exam_simulated'
export type LearningPhilosophy = 'direct_instruction' | 'socratic' | 'constructivist' | 'spaced_practice'

export interface ValidationGate {
  type: ValidationGateType
  pass_threshold: number
  question_count: number
}

export interface CoreLesson {
  lesson_id: string
  lesson_title: string
  order: number
  prerequisites: string[]
  validation: ValidationGate
}

export interface CoreModule {
  module_id: string
  module_title: string
  order: number
  lessons: CoreLesson[]
}

export interface CoreLayer {
  course_title: string
  terminal_objective: string
  estimated_weeks: number
  modules: CoreModule[]
}

export interface MediaMix {
  video: number
  interactive: number
  text: number
  audio?: number
  visual?: number
}

export interface TutorPersona {
  pace: TutorPace
  tone: TutorTone
  register: TutorRegister
}

export interface TrackLayer {
  path: string
  scaffolding: ScaffoldingLevel
  gating: GatingModel
  chunking: ChunkingDensity
  media_mix: MediaMix
  pacing_mode: PacingMode
  feedback_style: FeedbackStyle
  assessment_preference: AssessmentPreference
  tutor: TutorPersona
  session_cap_minutes: number
  srs_enabled: boolean
}

export interface Harness {
  core: CoreLayer
  track: TrackLayer
}
