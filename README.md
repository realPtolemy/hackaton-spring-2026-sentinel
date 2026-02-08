# hackaton-spring-2026-sentinel

# SquadReview: AI Multi-Agent Code Reviewer

**SquadReview** is a local developer tool that uses a parallel squad of AI agents to review, refactor, and ensure your code meets company standards before you commit.

## 🚀 Key Features

- **🤖 Multi-Agent System:** Spawns specialized agents (Optimizer, Enforcer, Documenter) in parallel using `trio`.
- **⚡ Polyglot Support:** Automatically detects and reviews **Java, C++, Python, and JS/TS**.
- **🏢 Custom Conventions:** Enforces _your_ specific rules defined in `docs/CONVENTIONS.md` `docs/LLM_CONSTITUTION.md`, `docs/EXCEPTIONS.md`.
- **🔄 Git Integration:** Automatically detects modified files in `src/` and stages changes (`git add`) upon acceptance.

## 🛠️ Quick Start

### 1. Setup

```bash
git clone [https://github.com/your-username/hackathon-spring-2026-sentinel.git](https://github.com/your-username/squad-review.git)
cd hackathon-spring-2026-sentinel
pip install -r requirements.txt
```

# Configure

Create a .env file with your Gemini API key:

```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run code_review_agent/main.py
```

workflow
Code: Edit files in your src/ folder.

Launch: Open the UI. Click the Robot Icon (🤖) next to a file.

Review: The squad analyzes performance, style, and docs simultaneously.

Accept: Review the diff. Click ✅ Accept to overwrite and stage the file.
