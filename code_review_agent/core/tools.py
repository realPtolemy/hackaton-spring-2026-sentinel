from pathlib import Path
class CodeTools:
    """Atomic operations available to the agents."""
    @staticmethod
    def detect_tooling():
        linter_configs = {
            ".clang-format": "C/C++ formatting handled by clang-format.",
            "pylintrc": "Python linting handled by Pylint.",
            ".prettierrc": "JS/TS formatting handled by Prettier."
        }
        found = [desc for conf, desc in linter_configs.items() if Path(conf).exists()]
        return "\n".join(found) if found else "No specific linting tools detected."

    @staticmethod
    def get_lang_name(ext):
        mapping = {".py": "Python", ".js": "JavaScript", ".go": "Go", ".rs": "Rust", ".ts": "TypeScript"}
        return mapping.get(ext, f"code ending in {ext}")