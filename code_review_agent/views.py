import streamlit as st
import difflib
import subprocess
from pathlib import Path

# --- NEW IMPORTS FOR SYNTAX HIGHLIGHTING ---
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

def render_hero_section(rules):
    st.title("🛡️ MAS Polyglot Reviewer")
    st.markdown("##### Java • C++ • Python • JS/TS")
    with st.expander("⚖️ Active Company Policy"):
        st.markdown(rules)

def render_sidebar(orchestrator, modified_files):
    st.sidebar.header("📁 Git Changes (src)")
    
    valid_files = [f for f in modified_files if Path(f).exists()]
    
    if not valid_files:
        st.sidebar.success("🎉 All files reviewed!")
        st.sidebar.info("No modified files found in git (unstaged).")
        return

    for f in valid_files:
        p = Path(f)
        pr_path = p.parent / f"{p.stem}_pr{p.suffix}"
        
        col_l, col_r = st.sidebar.columns([0.8, 0.2])
        col_l.caption(f"📄 {f}")
        
        if pr_path.exists():
            col_r.write("✅")
        else:
            if col_r.button("🤖", key=f"btn_{f}", help=f"Run Agent Squad on {f}"):
                with st.spinner(f"Squad refactoring {p.name}..."):
                    code = p.read_text(encoding="utf-8")
                    fixed_code = orchestrator.sync_refactor(str(p), code)
                    pr_path.write_text(fixed_code, encoding="utf-8")
                    st.rerun()

def render_diff_viewer(orig_path, prop_path):
    orig_text = Path(orig_path).read_text(encoding='utf-8')
    prop_text = Path(prop_path).read_text(encoding='utf-8')

    st.markdown(f"### 🔍 Reviewing: `{Path(orig_path).name}`")
    
    col_accept, col_reject = st.columns([0.5, 0.5])
    
    # --- ACCEPT LOGIC ---
    with col_accept:
        if st.button("✅ Accept Agent Fixes", type="primary", use_container_width=True): 
            Path(orig_path).write_text(prop_text, encoding='utf-8')
            Path(prop_path).unlink()
            subprocess.run(["git", "add", str(orig_path)], check=False)
            st.toast(f"Fixed & Staged: {Path(orig_path).name}")
            st.rerun()
            
    # --- REJECT LOGIC ---
    with col_reject:
        if st.button("❌ Reject", use_container_width=True):
            Path(prop_path).unlink()
            st.toast(f"Rejected proposal for {Path(orig_path).name}")
            st.rerun()

    # --- DIFF & SYNTAX HIGHLIGHTING ---
    diff = difflib.ndiff(orig_text.splitlines(), prop_text.splitlines())
    
    # 1. Detect Language based on file extension
    try:
        lexer = get_lexer_for_filename(orig_path)
    except ClassNotFound:
        lexer = TextLexer()

    # 2. Setup Formatter (Monokai matches the dark UI well)
    # 'noclasses=True' forces inline styles, 'nowrap=True' gives us just the span tags
    formatter = HtmlFormatter(style='monokai', noclasses=True, nowrap=True)
    
    left_html = []
    right_html = []
    
    # GitHub-like colors (Dark Mode specific)
    # Red background for deletions
    bg_delete = "rgba(248, 81, 73, 0.15)"
    # Green background for additions
    bg_add = "rgba(46, 160, 67, 0.15)"
    
    base_style = "font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.5; white-space: pre-wrap; padding: 0 5px;"
    
    for line in diff:
        code = line[2:]
        
        # Apply Syntax Highlighting to the raw code
        if code.strip():
            # Returns HTML <span> tags with colors
            highlighted_code = highlight(code, lexer, formatter) 
        else:
            highlighted_code = "&nbsp;"
        
        # Build the Side-by-Side Diff
        if line.startswith("- "):
            # Deleted: Red background on Left, Empty on Right
            left_html.append(f'<div style="{base_style} background-color: {bg_delete};">{highlighted_code}</div>')
            right_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>') 
            
        elif line.startswith("+ "):
            # Added: Empty on Left, Green background on Right
            left_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>')
            right_html.append(f'<div style="{base_style} background-color: {bg_add};">{highlighted_code}</div>')
            
        elif line.startswith("  "):
            # Unchanged: Transparent background
            left_html.append(f'<div style="{base_style} color: inherit;">{highlighted_code}</div>')
            right_html.append(f'<div style="{base_style} color: inherit;">{highlighted_code}</div>')
        
        elif line.startswith("? "):
            # Skip ndiff's internal guide lines
            continue

    c1, c2 = st.columns(2)
    with c1:
        st.caption("👈 **Original**")
        # Included a min-height to ensure the box looks good even if empty
        st.markdown(f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto; min-height: 200px;">{"".join(left_html)}</div>', unsafe_allow_html=True)
    with c2:
        st.caption("👉 **Agent Squad Proposal**")
        st.markdown(f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto; min-height: 200px;">{"".join(right_html)}</div>', unsafe_allow_html=True)