import os
import time
from pathlib import Path
import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") 
CONVENTION_FILE_PATH = "conventions.md" 
SOURCE_DIR = "./src"
SKIP_EXTENSIONS = [".pyc", ".git", ".md", "_pr.py", "_pr.js"] # Avoid re-processing output files

genai.configure(api_key=API_KEY)


MODEL_NAME = "gemini-2.5-flash"

# --- Agent Roles & Definitions ---

def get_expert_persona(file_extension):
    """
    Returns the specific persona based on the file type.
    This simulates having different agents with specific expertise.
    """
    personas = {
        ".py": "Senior Python Backend Engineer proficient in PEP8 and type hinting.",
        ".js": "Senior JavaScript/TypeScript Developer focused on ES6+ standards.",
        ".ts": "Senior TypeScript Developer focused on strict typing.",
        ".go": "Senior Go Developer focused on idiomatic Go.",
        ".java": "Senior Java Engineer focused on Enterprise standards.",
    }
    return personas.get(file_extension, "Senior Software Engineer focused on Clean Code.")

# --- The "Convention Analyst" Agent ---

def digest_conventions(convention_text):
    """
    Agent 1: Reads verbose documentation and converts it into a 
    strict checklist to save context window and improve adherence.
    """
    print("🤖 Agent [Convention Analyst]: Digesting organization rules...")
    
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    You are a Lead Architect. Analyze the following organization convention document.
    Summarize it into a concise, bulleted list of strictly actionable rules for code reviewers.
    Ignore fluff/introductory text. Focus on naming conventions, formatting, and structural rules.
    
    Convention Document:
    {convention_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- The "Refactorer" Agent ---

@retry.Retry(predicate=retry.if_transient_error)
def refactor_code(filepath, code_content, rules_checklist):
    """
    Agent 2: Applies the rules to the code.
    """
    extension = Path(filepath).suffix
    expert_role = get_expert_persona(extension)
    
    print(f"🤖 Agent [{expert_role}]: Refactoring {filepath}...")

    model = genai.GenerativeModel(
        MODEL_NAME,
        system_instruction=f"You are a {expert_role}. You strictly follow instructions."
    )
    
    prompt = f"""
    TASK: Refactor the provided code to comply with the Organization Rules.
    
    ORGANIZATION RULES:
    {rules_checklist}
    
    INSTRUCTIONS:
    1. Apply the rules to the code below.
    2. Do NOT change the logic or functionality of the code. Only fix style, naming, and structure.
    3. Return ONLY the raw code. Do not use Markdown backticks (```) or add explanation text.
    
    ORIGINAL CODE:
    {code_content}
    """
    
    # We set temperature low for deterministic code output
    response = model.generate_content(prompt, generation_config={"temperature": 0.1})
    
    # Simple cleanup in case the model adds markdown despite instructions
    clean_code = response.text.replace("```python", "").replace("```javascript", "").replace("```", "").strip()
    return clean_code

# --- The Coordinator (Main Logic) ---

def main():
    # 1. Read the convention file
    if not os.path.exists(CONVENTION_FILE_PATH):
        print(f"❌ Error: Convention file '{CONVENTION_FILE_PATH}' not found.")
        return

    with open(CONVENTION_FILE_PATH, "r", encoding="utf-8") as f:
        raw_conventions = f.read()

    # 2. Run the Convention Analyst Agent
    rules_checklist = digest_conventions(raw_conventions)
    print(f"\n📋 Derived Rules:\n{rules_checklist}\n{'-'*40}")

    # 3. Recursively find files
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = Path(root) / file
            
            # Skip irrelevant files
            if any(str(file_path).endswith(ext) for ext in SKIP_EXTENSIONS):
                continue
            
            # Only process code files (you can expand this list)
            if file_path.suffix not in ['.py', '.js', '.ts', '.java', '.go', '.cpp']:
                continue

            # 4. Read original code
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_code = f.read()
                
                # 5. Run the Refactorer Agent
                fixed_code = refactor_code(file_path, original_code, rules_checklist)
                
                # 6. Save as _pr file
                new_filename = f"{file_path.stem}_pr{file_path.suffix}"
                new_path = file_path.parent / new_filename
                
                with open(new_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                    
                print(f"✅ Created: {new_path}")
                
                # Avoid hitting rate limits (optional, depending on your tier)
                time.sleep(1) 
                
            except Exception as e:
                print(f"❌ Failed to process {file_path}: {e}")

if __name__ == "__main__":
    main()