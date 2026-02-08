from pathlib import Path

class CodeTools:
    """Atomic operations available to the agents."""
    
    @staticmethod
    def detect_tooling():
        linter_configs = {
            ".clang-format": "C/C++ formatting.",
            "pylintrc": "Python linting.",
            ".prettierrc": "JS/TS formatting.",
            "checkstyle.xml": "Java Checkstyle.",
            "tsconfig.json": "TypeScript Configuration."
        }
        found = [desc for conf, desc in linter_configs.items() if Path(conf).exists()]
        return "\n".join(found) if found else "No specific config files found."

    @staticmethod
    def get_lang_name(ext):
        mapping = {
            ".py": "Python", 
            ".js": "JavaScript", 
            ".ts": "TypeScript", 
            ".java": "Java", 
            ".cpp": "C++", 
            ".hpp": "C++ Header",
            ".cc": "C++",
            ".c": "C"
        }
        return mapping.get(ext, "Unknown Language")