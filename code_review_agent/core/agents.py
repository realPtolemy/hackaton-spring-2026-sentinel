import trio
from google.genai import types 

MODEL_NAME = "gemini-2.5-flash"

class SpecialistSquad:
    """A squad of specialized agents for polyglot code review."""
    def __init__(self, client):
        self.client = client

    async def _call_llm(self, prompt, system_instruction):
        """Standard async wrapper for Gemini calls."""
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

    # --- The Specialists ---

    async def optimizer_agent(self, code, language):
        sys = f"You are a Senior Performance Engineer specialized in {language}. Your goal is Efficiency."
        prompt = f"""
        Analyze this code:
        {code}
        
        Task: Identify O(n^2) loops, memory leaks, redundant computations, or inefficient data structures.
        Output: A concise bulleted list of specific optimization steps.
        """
        return await self._call_llm(prompt, sys)

    async def enforcer_agent(self, code, language, conventions, exceptions):
        sys = f"You are the {language} Policy Enforcer. You uphold the Company CONVENTIONS strictly."
        prompt = f"""
        Conventions: {conventions}
        Exceptions: {exceptions}
        Code:
        {code}
        
        Task: List deviations from the style guide. Focus on naming, banned functions, and architectural patterns.
        Output: A concise bulleted list of violations.
        """
        return await self._call_llm(prompt, sys)

    async def documenter_agent(self, code, language):
        sys = f"You are the Lead Technical Writer for {language}."
        prompt = f"""
        Analyze this code:
        {code}
        
        Task: Identify where Javadoc/Docstrings/Comments are missing or unclear. 
        Output: A list of where comments should be added to explain 'WHY', not just 'WHAT'.
        """
        return await self._call_llm(prompt, sys)

    # --- The Mentor (Synthesis) ---

    async def mentor_agent(self, code, language, optimization_report, policy_report, documentation_report):
        sys = f"""You are a Principal {language} Mentor. 
        Synthesize feedback from your team and rewrite the user's code.
        Be encouraging but firm about quality."""

        prompt = f"""
        ORIGINAL CODE:
        {code}

        TEAM REPORTS:
        1. Optimization: {optimization_report}
        2. Policy: {policy_report}
        3. Docs: {documentation_report}

        YOUR MISSION:
        1. Refactor the code to address ALL points (make it faster, clean, and well-documented).
        2. Create a top-level block comment (using {language} syntax) at the VERY TOP of the file.
           - Summarize changes.
           - Give specific guidance based on mistakes found.
        3. Output ONLY the code. No markdown backticks.
        """
        raw = await self._call_llm(prompt, sys)
        # Clean up markdown if the model returns it
        return raw.replace(f"```{language.lower()}", "").replace("```", "").strip()