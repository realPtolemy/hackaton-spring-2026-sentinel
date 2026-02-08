import trio
from google.genai import types 

MAX_CONCURRENT_FILES = 5
MODEL_NAME = "gemini-2.0-flash"

class ReviewAgents:
    """Personas and prompt logic for the MAS."""
    def __init__(self, client):
        self.client = client

    async def call_llm(self, prompt, system_instruction):
        """Standardized async wrapper for LLM calls."""
        response = await trio.to_thread.run_sync(
            lambda: self.client.models.generate_content(
                model=MODEL_NAME, 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2 
                )
            )
        )
        return response.text

    async def lawyer(self, language, conventions, exceptions, tooling):
        sys = "You are the Code Lawyer. You define strict legal frameworks for codebases."
        prompt = f"Define a checklist for {language}.\nConventions: {conventions}\nExceptions: {exceptions}\nTooling: {tooling}\nRULE: Forbid renaming public APIs."
        return await self.call_llm(prompt, sys)

    async def detective(self, code, ruleset, language):
        sys = f"You are the {language} Detective. You find violations with surgical precision."
        prompt = f"Rules: {ruleset}\nCode: {code}\nTask: List violations. If none, return 'NO_VIOLATIONS'."
        return await self.call_llm(prompt, sys)

    async def diplomat(self, code, violations, language):
        sys = "You are the Diplomat. You refactor code while maintaining public API stability."
        prompt = f"Original Code: {code}\nViolations: {violations}\nTask: Rewrite code. Fix internal style but NEVER change public signatures."
        raw = await self.call_llm(prompt, sys)
        return raw.replace(f"```{language.lower()}", "").replace("```", "").strip()