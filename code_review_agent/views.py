import streamlit as st
import difflib
import subprocess
from pathlib import Path

def render_hero_section(rules):
    st.title("🛡️ MAS Polyglot Reviewer")
    st.markdown("##### Java • C++ • Python • JS/TS")
    with st.expander("⚖️ Active Company Policy"):
        st.markdown(rules)

def render_sidebar(orchestrator, modified_files):
    st.sidebar.header("📁 Git Changes (src)")
    
    # Filter out files that might have been staged but are still in the list cache
    # (Optional extra safety, though rerun handles it)
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
            # 1. Apply the fix
            Path(orig_path).write_text(prop_text, encoding='utf-8')
            
            # 2. Remove the proposal file
            Path(prop_path).unlink()
            
            # 3. Git Add (Stage) the file
            # This removes it from `git ls-files -m`, making it vanish from the sidebar
            subprocess.run(["git", "add", str(orig_path)], check=False)
            
            st.toast(f"Fixed & Staged: {Path(orig_path).name}")
            st.rerun()
            
    # --- REJECT LOGIC ---
    with col_reject:
        if st.button("❌ Reject", use_container_width=True):
            Path(prop_path).unlink()
            st.toast(f"Rejected proposal for {Path(orig_path).name}")
            st.rerun()

    # --- DIFF RENDERING (No Changes Needed Here) ---
    diff = difflib.ndiff(orig_text.splitlines(), prop_text.splitlines())
    
    left_html = []
    right_html = []
    base_style = "font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.5; white-space: pre-wrap; padding: 0 5px;"
    
    for line in diff:
        code = line[2:]
        if not code: code = "&nbsp;" 
        
        if line.startswith("- "):
            left_html.append(f'<div style="{base_style} background-color: rgba(255, 0, 0, 0.2); text-decoration: line-through; opacity: 0.7;">{code}</div>')
            right_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>') 
        elif line.startswith("+ "):
            left_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>')
            right_html.append(f'<div style="{base_style} background-color: #fff5b1; color: black; font-weight: bold;">{code}</div>')
        elif line.startswith("  "):
            left_html.append(f'<div style="{base_style} color: inherit;">{code}</div>')
            right_html.append(f'<div style="{base_style} color: inherit;">{code}</div>')

    c1, c2 = st.columns(2)
    with c1:
        st.caption("👈 **Original**")
        st.markdown(f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto;">{"".join(left_html)}</div>', unsafe_allow_html=True)
    with c2:
        st.caption("👉 **Agent Squad Proposal**")
        st.markdown(f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto;">{"".join(right_html)}</div>', unsafe_allow_html=True)