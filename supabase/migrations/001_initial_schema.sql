-- =============================================================================
-- Neptune MVP — Initial Schema
-- Run this in the Supabase SQL editor for your project.
-- =============================================================================

-- Enable UUID extension (usually already enabled)
create extension if not exists "uuid-ossp";

-- =============================================================================
-- PROFILES
-- Extends auth.users — created automatically on first /profiles/me call
-- =============================================================================
create table if not exists public.profiles (
  id                  uuid references auth.users(id) on delete cascade primary key,
  display_name        text,
  educational_level   text check (educational_level in ('secondary','undergraduate','postgraduate','professional')),
  background_domain   text,
  preferred_language  text not null default 'English',
  default_chunking    text not null default 'standard',
  default_scaffolding text not null default 'guided',
  default_media_mix   jsonb not null default '{"video":40,"interactive":40,"text":20}'::jsonb,
  default_pacing      text not null default 'steady',
  tutor_tone          text not null default 'direct',
  tutor_pace          text not null default 'steady',
  tutor_register      text not null default 'practitioner',
  learning_philosophy text not null default 'direct_instruction',
  claude_api_key      text,           -- encrypted at application layer
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);

-- =============================================================================
-- COURSES
-- =============================================================================
create table if not exists public.courses (
  id                     uuid primary key default gen_random_uuid(),
  user_id                uuid not null references public.profiles(id) on delete cascade,
  title                  text not null,
  terminal_objective     text,
  delivery_path          text not null,
  harness                jsonb not null,        -- full Core + Track Layer
  modules_generated      integer not null default 0 check (modules_generated >= 0),
  status                 text not null default 'active' check (status in ('active','complete','archived')),
  target_completion_date date,
  created_at             timestamptz not null default now(),
  updated_at             timestamptz not null default now()
);

create index if not exists idx_courses_user_id on public.courses(user_id);

-- =============================================================================
-- LESSON COMPLETIONS
-- =============================================================================
create table if not exists public.lesson_completions (
  id           uuid primary key default gen_random_uuid(),
  course_id    uuid not null references public.courses(id) on delete cascade,
  user_id      uuid not null references public.profiles(id) on delete cascade,
  lesson_id    text not null,
  module_id    text not null,
  completed_at timestamptz not null default now(),
  attempts     integer not null default 1 check (attempts > 0),
  final_score  float check (final_score >= 0 and final_score <= 1),
  passed       boolean not null
);

create index if not exists idx_completions_course_id on public.lesson_completions(course_id);
create index if not exists idx_completions_user_lesson on public.lesson_completions(user_id, lesson_id);

-- =============================================================================
-- UPDATED_AT trigger
-- =============================================================================
create or replace function public.handle_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists on_profiles_updated on public.profiles;
create trigger on_profiles_updated
  before update on public.profiles
  for each row execute procedure public.handle_updated_at();

drop trigger if exists on_courses_updated on public.courses;
create trigger on_courses_updated
  before update on public.courses
  for each row execute procedure public.handle_updated_at();

-- =============================================================================
-- ROW LEVEL SECURITY
-- =============================================================================
alter table public.profiles          enable row level security;
alter table public.courses           enable row level security;
alter table public.lesson_completions enable row level security;

-- Profiles: users can only see/edit their own
create policy "profiles_select_own" on public.profiles for select using (auth.uid() = id);
create policy "profiles_insert_own" on public.profiles for insert with check (auth.uid() = id);
create policy "profiles_update_own" on public.profiles for update using (auth.uid() = id);

-- Courses: users can only see/edit their own
create policy "courses_select_own"  on public.courses for select using (auth.uid() = user_id);
create policy "courses_insert_own"  on public.courses for insert with check (auth.uid() = user_id);
create policy "courses_update_own"  on public.courses for update using (auth.uid() = user_id);
create policy "courses_delete_own"  on public.courses for delete using (auth.uid() = user_id);

-- Lesson completions: users can only see/edit their own
create policy "completions_select_own" on public.lesson_completions for select using (auth.uid() = user_id);
create policy "completions_insert_own" on public.lesson_completions for insert with check (auth.uid() = user_id);
create policy "completions_update_own" on public.lesson_completions for update using (auth.uid() = user_id);

-- =============================================================================
-- Notes for setup:
-- 1. After running this, go to Authentication → Users → Add user
--    to create your developer account manually.
-- 2. The profiles row is created automatically by the backend on first login.
-- 3. RLS policies use auth.uid() — the service role key bypasses RLS,
--    which is why the FastAPI backend uses the service role key.
-- =============================================================================
