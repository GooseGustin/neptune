import json
import anthropic
from app.models.harness import Harness, CoreModule
from app.models.content import GeneratedModule
from app.utils.encryption import decrypt

CLAUDE_MODEL = "claude-sonnet-4-20250514"

HARNESS_SYSTEM_PROMPT = """You are a course architect for the Neptune learning platform.
Return ONLY valid JSON matching the schema provided. Never include explanation or markdown outside the JSON block.
The JSON must be parseable with json.loads()."""

CONTENT_SYSTEM_PROMPT = """You are a course content generator for the Neptune learning platform.
You generate structured educational content in strict JSON format.
Never include text outside the JSON block. The JSON must be parseable with json.loads().
Adapt all explanations to the learner's background domain using analogies where relevant.
Apply the specified tutor persona consistently across all content."""

def get_client(encrypted_api_key: str) -> anthropic.Anthropic:
    api_key = decrypt(encrypted_api_key)
    return anthropic.Anthropic(api_key=api_key)

async def generate_harness_core(
    encrypted_api_key: str,
    intent: str,
    delivery_path: str,
    background_domain: str,
    educational_level: str,
    timeline: str | None,
) -> dict:
    client = get_client(encrypted_api_key)

    schema = """{
  "course_title": "string",
  "terminal_objective": "string",
  "estimated_weeks": number,
  "modules": [
    {
      "module_id": "string (slug format, e.g. module-01-http-basics)",
      "module_title": "string",
      "order": number,
      "lessons": [
        {
          "lesson_id": "string (slug format)",
          "lesson_title": "string",
          "order": number,
          "prerequisites": ["lesson_id", "..."],
          "validation": {
            "type": "multiple_choice | true_false | mark_complete",
            "pass_threshold": 0.8,
            "question_count": 5
          }
        }
      ]
    }
  ]
}"""

    user_prompt = f"""Generate a course Core Layer Harness for the following:

Intent: {intent}
Delivery path: {delivery_path}
Learner background: {background_domain}
Educational level: {educational_level}
Target completion: {timeline or "unspecified"}

Return a JSON object with this exact schema:
{schema}

Aim for 6-8 modules with 3-5 lessons each. Make lesson_ids unique slugs like "lesson-http-get-post"."""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=HARNESS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


async def generate_module_content(
    encrypted_api_key: str,
    harness: Harness,
    module: CoreModule,
    background_domain: str,
    learning_philosophy: str,
) -> GeneratedModule:
    client = get_client(encrypted_api_key)

    harness_summary = {
        "course_title": harness.core.course_title,
        "terminal_objective": harness.core.terminal_objective,
        "track": harness.track.model_dump(),
    }

    user_prompt = f"""Generate full content for this module.

--- HARNESS SUMMARY ---
{json.dumps(harness_summary, indent=2)}

--- MODULE TO GENERATE ---
{module.model_dump_json(indent=2)}

--- LEARNER CONTEXT ---
Background domain: {background_domain}
Learning philosophy: {learning_philosophy}
Tutor: pace={harness.track.tutor.pace}, tone={harness.track.tutor.tone}, register={harness.track.tutor.register}

Return a JSON object with this exact schema:
{{
  "module_id": "{module.module_id}",
  "module_title": "{module.module_title}",
  "lessons": [
    {{
      "lesson_id": "string",
      "lesson_title": "string",
      "sections": [
        {{
          "section_id": "string",
          "section_title": "string",
          "content_pieces": [
            {{
              "type": "text|video|audio|flashcard_set|quiz",
              "content": {{ /* type-specific fields */ }}
            }}
          ]
        }}
      ],
      "validation": {{
        "type": "multiple_choice|true_false|mark_complete",
        "questions": [ /* if applicable */ ]
      }}
    }}
  ]
}}

Text content: {{"body": "markdown string"}}
Video content: {{"url": "youtube embed-friendly url", "title": "string", "caption": "string"}}
Flashcard set: {{"cards": [{{"card_id": "string", "front": "string", "back": "string"}}]}}
Quiz: {{"questions": [{{"question_id": "string", "question_text": "string", "type": "multiple_choice", "options": ["A","B","C","D"], "correct_answer": "A", "explanation": "string"}}]}}

Generate 2-4 sections per lesson. Match media mix: video={harness.track.media_mix.video}%, interactive={harness.track.media_mix.interactive}%, text={harness.track.media_mix.text}%."""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8192,
        system=CONTENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    data = json.loads(raw)
    return GeneratedModule(**data)
