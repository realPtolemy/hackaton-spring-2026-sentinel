import os
import trio
import random
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from .agents import ReviewAgents
from .tools import CodeTools

load_dotenv()

# --- Configuration ---
MAX_CONCURRENT_FILES = 5
MODEL_NAME = "gemini-2.0-flash"

class Orchestrator:
    """The MAS Manager that controls the workflow and concurrency."""
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.agents = ReviewAgents(self.client)
        self.tools = CodeTools()
        self.rules_cache = {}
        
        # Load static context
        self.conventions = self._read_file("./docs/CONVENTIONS.md")
        self.exceptions = self._read_file("./docs/EXCEPTIONS.md")

    def _read_file(self, path):
        p = Path(path)
        return p.read_text(encoding="utf-8") if p.exists() else ""

    async def review_flow(self, file_path, code_content=None):
        """The logical 'brain' that sequences agent interactions."""
        p = Path(file_path)
        lang = self.tools.get_lang_name(p.suffix)
        
        if not code_content:
            code_content = await trio.to_thread.run_sync(lambda: p.read_text(encoding="utf-8"))

        # 1. Lawyer drafting (with caching)
        if lang not in self.rules_cache:
            tooling = self.tools.detect_tooling()
            self.rules_cache[lang] = await self.agents.lawyer(lang, self.conventions, self.exceptions, tooling)
        
        rules = self.rules_cache[lang]

        # 2. Detective investigation
        violations = await self.agents.detective(code_content, rules, lang)
        
        if "NO_VIOLATIONS" in violations:
            return code_content, False

        # 3. Diplomat resolution
        fixed_code = await self.agents.diplomat(code_content, violations, lang)
        return fixed_code, True

    # --- Trio Entry Points ---
    def sync_digest_rules(self):
        """Streamlit-friendly way to get the 'Legal' rules."""
        async def _run():
            tooling = self.tools.detect_tooling()
            return await self.agents.lawyer("General", self.conventions, self.exceptions, tooling)
        return trio.run(_run)

    def sync_refactor(self, path_str, code):
        """Streamlit-friendly way to run the full MAS flow."""
        async def _run():
            fixed, changed = await self.review_flow(path_str, code)
            return fixed
        return trio.run(_run)