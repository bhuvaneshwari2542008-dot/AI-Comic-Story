import asyncio
from app.config import get_settings
from app.models import ComicRequest, ComicStory, ComicPanel, Dialogue

class StoryGenerationError(RuntimeError):
    pass

class StoryGenerator:
    async def generate(self, request: ComicRequest) -> ComicStory:
        settings = get_settings()
        if settings.demo_mode or not settings.gemini_api_key:
            return self._demo_story(request)
        return await asyncio.to_thread(self._generate_with_gemini, request)

    def _generate_with_gemini(self, request: ComicRequest) -> ComicStory:
        try:
            from google import genai
            from google.genai import types
            settings = get_settings()
            client = genai.Client(api_key=settings.gemini_api_key)
            prompt = f"""Create a complete {request.panel_count}-panel comic.
Story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.story_tone}
Art style: {request.art_style}
Maintain one consistent character appearance. Include a beginning, conflict, and resolution. Keep dialogue concise. Image prompts must not request words, captions, or speech bubbles."""
            response = client.models.generate_content(
                model=settings.gemini_text_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ComicStory,
                    temperature=0.8,
                ),
            )
            story = response.parsed or ComicStory.model_validate_json(response.text)
            if len(story.panels) != request.panel_count:
                raise StoryGenerationError("The AI returned an incorrect panel count.")
            return story
        except StoryGenerationError:
            raise
        except Exception as exc:
            raise StoryGenerationError("Gemini story generation failed. Check your API key and model configuration.") from exc

    def _demo_story(self, request: ComicRequest) -> ComicStory:
        character = f"{request.character_name}, an expressive hero with a consistent outfit and recognizable silhouette"
        beats = [
            ("arrives", "A new adventure begins."),
            ("discovers a surprising clue", "Something unusual changes everything."),
            ("faces an unexpected obstacle", "The challenge suddenly grows."),
            ("finds a clever solution", "A brave idea offers hope."),
            ("celebrates a successful ending", "The adventure ends with a smile."),
            ("looks toward the next adventure", "But another story is waiting."),
        ]
        panels=[]
        for index in range(request.panel_count):
            action, narration = beats[index]
            scene=f"{request.character_name} {action} in {request.setting}."
            panels.append(ComicPanel(
                panel_number=index+1,
                scene=scene,
                narration=narration,
                dialogue=[Dialogue(speaker=request.character_name, text=["Let's begin!", "What could this mean?", "I won't give up!", "I have an idea!", "We did it!", "Onward!"][index])],
                image_prompt=f"{request.art_style}; {character}; {scene}; {request.story_tone} mood; clean comic panel; no written text; no speech bubbles",
            ))
        return ComicStory(title=f"{request.character_name} and the Unexpected Adventure", summary=request.story_prompt, character_description=character, panels=panels)
