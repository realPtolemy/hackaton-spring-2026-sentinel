import streamlit as st
import difflib
from pathlib import Path

def render_hero_section(rules):
    st.title("🛡️ MAS Code Reviewer")
    with st.expander("⚖️ Active Legal Rules (Lawyer Agent)"):
        st.markdown(rules)

def render_sidebar(orchestrator, modified_files):
    st.sidebar.header("📁 Source Changes")
    for f in modified_files:
        p = Path(f)
        pr_path = p.parent / f"{p.stem}_pr{p.suffix}"
        
        col_l, col_r = st.sidebar.columns([0.8, 0.2])
        col_l.caption(f)
        
        if pr_path.exists():
            col_r.write("✅")
        else:
            if col_r.button("🤖", key=f"btn_{f}"):
                with st.spinner("Agents working..."):
                    code = p.read_text(encoding="utf-8")
                    fixed = orchestrator.sync_refactor(f, code)
                    pr_path.write_text(fixed, encoding="utf-8")
                    st.rerun()

def render_diff_viewer(orig_path, prop_path):
    orig_text = Path(orig_path).read_text(encoding='utf-8')
    prop_text = Path(prop_path).read_text(encoding='utf-8')

    # --- 1. ACTION BUTTONS (TOP) ---
    st.markdown("### 🔍 Review Proposal")
    col_accept, col_reject = st.columns([0.5, 0.5])
    
    with col_accept:
        if st.button("✅ Accept Proposal", type="primary", use_container_width=True): 
            Path(orig_path).write_text(prop_text, encoding='utf-8')
            Path(prop_path).unlink()
            st.rerun()
            
    with col_reject:
        if st.button("❌ Reject", use_container_width=True):
            Path(prop_path).unlink()
            st.rerun()

    # --- 2. SIDE-BY-SIDE DIFF LOGIC ---
    diff = difflib.ndiff(orig_text.splitlines(), prop_text.splitlines())
    
    left_html = []
    right_html = []
    
    base_style = "font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.5; white-space: pre-wrap; padding: 0 5px;"
    
    for line in diff:
        code = line[2:]
        if not code: code = "&nbsp;" 
        
        if line.startswith("- "):
            left_html.append(f'<div style="{base_style} background-color: rgba(255, 0, 0, 0.2); text-decoration: line-through; opacity: 0.7;">{code}</div>')
            right_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>') # Spacer
            
        elif line.startswith("+ "):
            left_html.append(f'<div style="{base_style} user-select: none;">&nbsp;</div>') # Spacer
            right_html.append(f'<div style="{base_style} background-color: #fff5b1; color: black; font-weight: bold;">{code}</div>')
            
        elif line.startswith("  "):
            left_html.append(f'<div style="{base_style} color: inherit;">{code}</div>')
            right_html.append(f'<div style="{base_style} color: inherit;">{code}</div>')
    
    # --- 3. RENDER COLUMNS ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.caption("👈 **Original Code**")
        st.markdown(
            f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto;">{"".join(left_html)}</div>', 
            unsafe_allow_html=True
        )
        
    with c2:
        st.caption("👉 **AI Proposal**")
        st.markdown(
            f'<div style="border: 1px solid #333; border-radius: 5px; background-color: #0e1117; padding: 10px; overflow-x: auto;">{"".join(right_html)}</div>', 
            unsafe_allow_html=True
        )