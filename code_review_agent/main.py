import streamlit as st
import os
from core.orchestrator import Orchestrator
from state import UIState
from views import render_hero_section, render_sidebar, render_diff_viewer

st.set_page_config(layout="wide", page_title="MAS Reviewer", page_icon="🛡️")

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator(api_key=os.getenv("GOOGLE_API_KEY"))

def main():
    if "rules" not in st.session_state:
        st.session_state.rules = st.session_state.orchestrator.sync_digest_rules()

    render_hero_section(st.session_state.rules)

    modified_files = UIState.get_git_modified_files()
    render_sidebar(st.session_state.orchestrator, modified_files)

    proposals = UIState.get_active_proposals()
    
    if not proposals:
        st.info("No active proposals. Process a file in the sidebar to begin.")
        return

    selected_orig = st.selectbox("Reviewing file:", list(proposals.keys()))
    render_diff_viewer(selected_orig, proposals[selected_orig])

if __name__ == "__main__":
    main()