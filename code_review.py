import os
import trio
import random
from pathlib import Path
from google import genai
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
MAX_CONCURRENT_FILES = 5  # Limits how many files are processed at once
MODEL_NAME = "gemini-2.0-flash"

class AsyncMultiAgentReviewer:
    def __init__(self, api_key, convention_path="./docs/CONVENTIONS.md", exception_path="./docs/EXCEPTIONS.md"):
        self.client = genai.Client(api_key=api_key)
        self.conventions = self._load_file(convention_path)
        self.exceptions = self._load_file(exception_path)
        self.tooling_context = self._detect_tooling()
        
        # Cache for Lawyer's rulesets
        self.rules_cache = {} 

    def _load_file(self, path_str):
        path = Path(path_str)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def _detect_tooling(self):
        linter_configs = {
            ".clang-format": "C/C++ formatting handled by clang-format.",
            "pylintrc": "Python linting handled by Pylint.",
            ".prettierrc": "JS/TS formatting handled by Prettier."
        }
        found = [desc for conf, desc in linter_configs.items() if Path(conf).exists()]
        return "\n".join(found) if found else ""

    def get_language_context(self, file_ext):
        return {".py": "Python", ".js": "JavaScript", ".go": "Go", ".rs": "Rust"}.get(file_ext, f"code ending in {file_ext}")

    # --- CORE ASYNC API WRAPPER (With Backoff) ---
    async def _call_gemini(self, prompt, system_instruction=None):
        """
        Wraps the blocking Google SDK call in a thread and handles rate limits (429)
        with async exponential backoff.
        """
        attempt = 0
        max_retries = 6
        
        while True:
            try:
                # 1. Offload the blocking network call to a worker thread
                # This ensures the main async loop doesn't freeze.
                response = await trio.to_thread.run_sync(
                    lambda: self.client.models.generate_content(
                        model=MODEL_NAME, 
                        contents=prompt,
                        config={"system_instruction": system_instruction} if system_instruction else None
                    )
                )
                return response.text

            except Exception as e:
                # 2. Check for Rate Limits
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt >= max_retries:
                        raise e # Give up after 6 tries
                    
                    attempt += 1
                    # Exponential backoff: 2, 4, 8... + random jitter
                    sleep_time = (4 ** attempt) + random.uniform(0, 1)
                    print(f"   ⏳ Rate limit hit. Retrying in {sleep_time:.2f}s...")
                    await trio.sleep(sleep_time) # Non-blocking sleep
                else:
                    raise e # Re-raise other errors (like 400 Bad Request)

    # --- ASYNC AGENTS ---

    async def _agent_lawyer(self, language):
        if language in self.rules_cache:
            return self.rules_cache[language]

        print(f"   ⚖️  The Lawyer is drafting rules for {language}...")
        prompt = f"""
        INPUTS: 
        - Conventions: {self.conventions}
        - Exceptions: {self.exceptions}
        - Tooling: {self.tooling_context}
        
        TASK:
        Create a strict checklist for {language}.
        CRITICAL SAFETY RULE: To allow for parallel processing, you must forbid renaming 
        public functions, classes, or exported variables. Only internal logic/style 
        can be changed.
        """
        
        rules = await self._call_gemini(prompt, system_instruction="You are the code Lawyer.")
        self.rules_cache[language] = rules
        return rules

    async def _agent_detective(self, code, ruleset, language):
        print(f"   🔎  The Detective is looking for styling violations for {language}...")
        prompt = f"""
        ROLE: Senior {language} code styling, error and bugs Detective.
        RULES: {ruleset}
        CODE: {code}
        
        TASK: List semantic/style violations.
        
        SPECIAL INSTRUCTION FOR GLOBALS:
        If you see a NEW global variable or exported constant being defined:
        1. Check strictly if the name is descriptive (e.g. 'MAX_RETRY_COUNT' is good, 'MAX' is bad).
        2. If the name is generic/bad, flag it as a CRITICAL VIOLATION.
        3. Do NOT allow generic globals to enter the codebase.
        """
        return await self._call_gemini(prompt)


    async def _agent_diplomat(self, code, violations, language):
        print(f"   🤝  The Diplomat is implementing the recommended changes for {language}...")
        prompt = f"""
        ROLE: You are the 'Diplomat'. You act as a safe code-fixer.

        INPUTS:
        - ORIGINAL CODE: {code}
        - VIOLATIONS FOUND: {violations}

        TASK:
        Rewrite the code to fix the violations, BUT YOU MUST ADHERE TO THIS HIERARCHY:
        
        1. [HIGHEST PRIORITY] PUBLIC API SAFETY:
           - You are FORBIDDEN from changing the names or signatures of public functions, classes, or exported variables.
           - If a violation asks you to rename a public function (e.g. "Rename GetUser to get_user"), you must IGNORE that violation.
           - Only rename internal/private variables (e.g. inside a function body).

        2. [LOWER PRIORITY] CODE STYLE:
           - Fix all other violations (formatting, internal naming, logic optimizations).

        OUTPUT:
        Return ONLY the rewritten code.
        """
        response_text = await self._call_gemini(prompt, system_instruction="You are the code Diplomat.")
        return response_text.replace("```" + language.lower(), "").replace("```", "").strip()

    # --- WORKER FUNCTION ---

    async def process_single_file(self, file_path, limiter, results_list):
        # The limiter ensures we don't start more than MAX_CONCURRENT_FILES at once
        async with limiter:
            try:
                language = self.get_language_context(file_path.suffix)
                # Read file in a thread to be safe (though SSDs are fast enough to block usually)
                code_content = await trio.to_thread.run_sync(
                    lambda: file_path.read_text(encoding="utf-8")
                )

                # 1. Lawyer
                ruleset = await self._agent_lawyer(language)

                # 2. Detective
                violations = await self._agent_detective(code_content, ruleset, language)

                if "NO_VIOLATIONS" in violations:
                    print(f"✅ {file_path.name}: Clean")
                    results_list.append("Clean")
                    return

                # 3. Diplomat
                fixed_code = await self._agent_diplomat(code_content, violations, language)
                
                # Write output (safe to do strictly if files are different, but we wrap it to be nice)
                output_path = file_path.parent / f"{file_path.stem}_pr{file_path.suffix}"
                await trio.to_thread.run_sync(
                    lambda: output_path.write_text(fixed_code, encoding="utf-8")
                )
                
                print(f"✨ {file_path.name}: Refactored")
                results_list.append("Refactored")

            except Exception as e:
                print(f"❌ {file_path.name}: Failed ({str(e)})")
                results_list.append("Failed")

    # --- SYNC WRAPPERS FOR STREAMLIT ---

    def digest_conventions(self):
        """Sync wrapper for the rules logic"""
        # Since _agent_lawyer is async, we run it via trio
        return trio.run(self._agent_lawyer, "General/Initial Analysis")

    def refactor_code(self, file_path_str, code):
        """Sync wrapper to process a single file string"""
        path = Path(file_path_str)
        language = self.get_language_context(path.suffix)
        
        async def _run_pipeline():
            ruleset = await self._agent_lawyer(language)
            violations = await self._agent_detective(code, ruleset, language)
            
            if "NO_VIOLATIONS" in violations:
                return code
            
            return await self._agent_diplomat(code, violations, language)
            
        return trio.run(_run_pipeline)


# --- MAIN TRIO ORCHESTRATOR ---

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: raise ValueError("No API Key found")

    reviewer = AsyncMultiAgentReviewer(api_key)
    source_dir = Path("./src")
    extensions = {'.py', '.js', '.ts', '.go', '.java', '.cpp'}
    
    # 1. Collect files
    files_to_process = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            p = Path(root) / file
            if p.suffix in extensions and "_sentinel" not in file:
                files_to_process.append(p)

    print(f"🚀 Starting Async Review for {len(files_to_process)} files...")
    
    # 2. Setup Concurrency Control
    limiter = trio.CapacityLimiter(MAX_CONCURRENT_FILES)
    results = []

    # 3. Launch the Swarm
    # The 'nursery' manages all child tasks. It won't exit until all tasks are done.
    async with trio.open_nursery() as nursery:
        for file_path in files_to_process:
            nursery.start_soon(reviewer.process_single_file, file_path, limiter, results)

    # 4. The Auditor (Runs after the nursery closes, meaning all tasks finished)
    print("\n🧾 The Auditor is checking for broken builds...")
    if "Failed" in results:
        print("🚨 Audit Failed: Some files crashed during review.")
    else:
        print("✅ Audit Pass: All files processed successfully.")

if __name__ == "__main__":
    trio.run(main)