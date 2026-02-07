import streamlit as st
import os
import subprocess
from pathlib import Path
from code_review import MultiAgentReviewer 

# --- Config ---
PR_SUFFIX = "_pr"
WATCH_DIR = "src"  # Restricted directory
st.set_page_config(layout="wide", page_title="Multi-Agent Reviewer", page_icon="🛡️")

# Initialize the Engine
if "reviewer" not in st.session_state:
    st.session_state.reviewer = MultiAgentReviewer(api_key=os.getenv("GOOGLE_API_KEY"))

def get_git_modified_files():
    """Finds Modified, Added (Staged), and Untracked (New) files in WATCH_DIR."""
    try:
        cmd_mod = ["git", "diff", "--name-only", "--diff-filter=ACM", "--", WATCH_DIR]
        modified = subprocess.check_output(cmd_mod, encoding='utf-8').splitlines()
        
        cmd_staged = ["git", "diff", "--name-only", "--diff-filter=ACM", "--cached", "--", WATCH_DIR]
        staged = subprocess.check_output(cmd_staged, encoding='utf-8').splitlines()
        
        cmd_untracked = ["git", "ls-files", "--others", "--exclude-standard", "--", WATCH_DIR]
        untracked = subprocess.check_output(cmd_untracked, encoding='utf-8').splitlines()
        

        all_changed = set(modified + staged + untracked)
        
        valid_files = []
        for f in all_changed:
            path = Path(f)
            if path.exists() and PR_SUFFIX not in path.name:
                valid_files.append(str(path))
                
        return valid_files

    except subprocess.CalledProcessError:
        return []
    except Exception as e:
        st.error(f"Error scanning git files: {e}")
        return []

# --- UI ---

def main():
    st.title("🛡️ Multi-Agent Reviewer")
    st.caption(f"Monitoring changes in: `/{WATCH_DIR}`")
    
    # Pre-digest conventions
    if "rules" not in st.session_state:
        with st.spinner("Agent [Analyst] digesting conventions..."):
            st.session_state.rules = st.session_state.reviewer.digest_conventions()

    # Sidebar: File Selection
    modified_files = get_git_modified_files()
    st.sidebar.header(f"📁 {WATCH_DIR} Changes")
    
    if not modified_files:
        st.sidebar.info(f"No modifications found in {WATCH_DIR}/")
    else:
        for f in modified_files:
            p = Path(f)
            pr_path = p.parent / f"{p.stem}{PR_SUFFIX}{p.suffix}"
            
            col_left, col_right = st.sidebar.columns([0.7, 0.3])
            col_left.write(f)
            
            if pr_path.exists():
                col_right.write("✅")
            else:
                if col_right.button("🤖", key=f"btn_{f}"):
                    with st.spinner(f"Refactoring {f}..."):
                        code = p.read_text(encoding="utf-8")
                        fixed = st.session_state.reviewer.refactor_code(f, code)
                        pr_path.write_text(fixed, encoding="utf-8")
                        st.rerun()

    # Main Area: Review Proposals (Only look inside src/)
    # Path(WATCH_DIR).rglob ensures we don't look at root-level config files
    if os.path.exists(WATCH_DIR):
        pr_files = list(Path(WATCH_DIR).rglob(f"*{PR_SUFFIX}.*"))
    else:
        pr_files = []
        
    valid_pairs = []
    for pr in pr_files:
        orig_path = pr.parent / pr.name.replace(PR_SUFFIX, "")
        if orig_path.exists():
            valid_pairs.append({"orig": orig_path, "prop": pr, "name": str(orig_path)})

    if not valid_pairs:
        st.info(f"Click the 🤖 icon in the sidebar to process a file from the {WATCH_DIR} directory.")
        with st.expander("View Active Organization Rules"):
            st.write(st.session_state.rules)
        return

    selected = st.selectbox("Select file to review:", [v["name"] for v in valid_pairs])
    pair = next(v for v in valid_pairs if v["name"] == selected)

    # Diff Display
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Original")
        st.code(pair["orig"].read_text())
    with c2:
        st.subheader("AI Proposal")
        st.code(pair["prop"].read_text())

    # Final Actions
    b1, b2, _ = st.columns([1, 1, 3])
    if b1.button("✅ Accept", use_container_width=True):
        pair["orig"].write_text(pair["prop"].read_text())
        pair["prop"].unlink()
        st.rerun()
    
    if b2.button("❌ Reject", use_container_width=True):
        pair["prop"].unlink()
        st.rerun()

if __name__ == "__main__":
    main()