import os
from pathlib import Path
from google import genai  # New SDK
from google.api_core import retry
from dotenv import load_dotenv

load_dotenv()

class MultiAgentReviewer:
    def __init__(self, api_key, model_name="gemini-2.0-flash", convention_path="./docs/CONVENTIONS.md", exception_path="./docs/EXCEPTIONS.md"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.convention_path = convention_path
        self.exceptions = exception_path
        self.rules_checklist = None

    def get_expert_persona(self, file_extension):
        personas = {
            ".py": "Senior Python Backend Engineer proficient in PEP8 and type hinting.",
            ".js": "Senior JavaScript/TypeScript Developer focused on ES6+ standards.",
            ".ts": "Senior TypeScript Developer focused on strict typing.",
            ".go": "Senior Go Developer focused on idiomatic Go.",
            ".java": "Senior Java Engineer focused on Enterprise standards.",
        }
        return personas.get(file_extension, "Senior Software Engineer focused on Clean Code.")

    def digest_conventions(self):
        """Agent 1: Digests the convention file into a checklist."""
        if not os.path.exists(self.convention_path):
            return "No specific conventions found. Follow general clean code principles."

        with open(self.convention_path, "r", encoding="utf-8") as f:
            convention_text = f.read()

        prompt = f"""
        You are a Lead Architect. Analyze the following organization convention document.
        Summarize it into a concise, bulleted list of strictly actionable rules.
        Convention Document:
        {convention_text}
        """
        # New SDK syntax: client.models.generate_content
        response = self.client.models.generate_content(
            model=self.model_name, 
            contents=prompt
        )
        self.rules_checklist = response.text
        return self.rules_checklist

    @retry.Retry(predicate=retry.if_transient_error)
    def refactor_code(self, filepath, code_content):
        """Agent 2: Applies the rules to the code."""
        if not self.rules_checklist:
            self.digest_conventions()

        extension = Path(filepath).suffix
        expert_role = self.get_expert_persona(extension)
        
        prompt = f"""
        TASK: Refactor the provided code to comply with the Organization Rules.
        ORGANIZATION RULES:
        {self.rules_checklist}
        
        INSTRUCTIONS:
        1. Apply rules to code below. Do NOT change logic or functionality.
        2. Return ONLY the raw code. No Markdown backticks or explanations.
        
        ORIGINAL CODE:
        {code_content}
        """
        
        # New SDK uses config object for system_instruction and temperature
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "system_instruction": f"You are a {expert_role}. You strictly follow instructions.",
                "temperature": 0.1
            }
        )
        
        # Cleanup markdown
        clean_code = response.text.replace("```python", "").replace("```javascript", "").replace("```", "").strip()
        return clean_code
