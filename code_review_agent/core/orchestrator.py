import trio
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from .agents import SpecialistSquad
from .tools import CodeTools

load_dotenv()

class Orchestrator:
    """The Manager that routes code to the correct language squad."""
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.tools = CodeTools()
        
        # Load the files Organization specific conventions/exceptions
        self.conventions = self._read_file("./docs/CONVENTIONS.md")
        self.exceptions = self._read_file("./docs/EXCEPTIONS.md")
        # Load the new LLM-Instructive Constitution
        self.constitution = self._read_file("./docs/LLM_CONSTITUTION.md")
        # Pass constitution to the squad
        self.squad = SpecialistSquad(self.client, self.constitution)

    def _read_file(self, path):
        p = Path(path)
        return p.read_text(encoding="utf-8") if p.exists() else ""

    async def review_flow(self, file_path, code_content=None):
        """
        Parallel Agent Workflow:
        1. Identify Language.
        2. Spawn 3 specialist agents (Optimize, Policy, Comment).
        3. Mentor synthesizes results.
        """
        p = Path(file_path)
        lang = self.tools.get_lang_name(p.suffix)
        
        if lang == "Unknown Language":
            return f"// Skipping {file_path}: Language not supported."

        if not code_content:
            code_content = await trio.to_thread.run_sync(lambda: p.read_text(encoding="utf-8"))

        # --- Parallel Execution in Trio Nursery ---
        async with trio.open_nursery() as nursery:
            results = [None, None, None] # Mutable container for results
            
            # 1. Optimizer Task
            nursery.start_soon(self._run_agent, self.squad.optimizer_agent, 
                               (code_content, lang), results, 0)
            
            # 2. Enforcer Task
            nursery.start_soon(self._run_agent, self.squad.enforcer_agent, 
                               (code_content, lang, self.conventions, self.exceptions), results, 1)
            
            # 3. Documenter Task
            nursery.start_soon(self._run_agent, self.squad.documenter_agent, 
                               (code_content, lang), results, 2)

        opt_report, policy_report, doc_report = results

        # --- Mentor Synthesis ---
        final_code = await self.squad.mentor_agent(
            code=code_content,
            language=lang,
            optimization_report=opt_report,
            policy_report=policy_report,
            documentation_report=doc_report
        )
        
        return final_code

    async def _run_agent(self, func, args, result_list, index):
        """Helper to store agent result in specific index."""
        result_list[index] = await func(*args)
    
    def sync_digest_rules(self):
        """Returns the loaded rules text for the Hero section."""
        return f"{self.conventions}\n\n{self.exceptions}"

    def sync_refactor(self, path_str, code):
        """Runs the async trio loop for the UI."""
        async def _run():
            return await self.review_flow(path_str, code)
        return trio.run(_run)