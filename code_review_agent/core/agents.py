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
        sys = f"You are the Lead Technical Writer for {language}. You hate redundancy."
        prompt = f"""
        Analyze this code:
        {code}
        
        Task: Identify where comments are critical.
        Rules:
        1. IGNORE getters, setters, and obvious logic.
        2. ONLY flag complex algorithms or non-obvious business logic.
        3. If the code is self-explanatory, return 'NO_COMMENTS_NEEDED'.
        
        Output: A concise list of strictly necessary documentation updates.
        """
        return await self._call_llm(prompt, sys)

    # --- The Mentor (Synthesis) ---
    async def mentor_agent(self, code, language, optimization_report, policy_report, documentation_report):
        sys = f"""You are a Principal {language} Architect. 
        Synthesize feedback and rewrite the code.
        Your style is: Minimalist, Pragmatic, Professional.
        """

        prompt = f"""
        ORIGINAL CODE:
        {code}

        TEAM REPORTS:
        1. Optimization: {optimization_report}
        2. Policy: {policy_report}
        3. Docs: {documentation_report}

        YOUR MISSION:
        1. Refactor the code to address valid points.
        2. DO NOT add inline comments for every change. Only comment on complex logic.
        3. Create a top-level block comment (using {language} syntax) at the VERY TOP.
           - Format: Bullet points only.
           - Content: Summary of changes and 1-2 critical tips.
           - Tone: Direct and technical. No fluff (e.g., avoid "I have improved...").
        4. Output ONLY the code. No markdown backticks.
        """
        raw = await self._call_llm(prompt, sys)
        return raw.replace(f"```{language.lower()}", "").replace("```", "").strip()