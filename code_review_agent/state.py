import streamlit as st
import subprocess
from pathlib import Path

PR_SUFFIX = "_pr"
WATCH_DIR = "src"

class UIState:
    @staticmethod
    def get_git_modified_files():
        try:
            cmd = ["git", "ls-files", "-m", "-o", "--exclude-standard", WATCH_DIR]
            files = subprocess.check_output(cmd, encoding='utf-8').splitlines()
            return [f for f in files if PR_SUFFIX not in f and Path(f).exists()]
        except:
            return []

    @staticmethod
    def get_active_proposals():
        pr_files = list(Path(WATCH_DIR).rglob(f"*{PR_SUFFIX}.*"))
        return {str(p.parent / p.name.replace(PR_SUFFIX, "")): p for p in pr_files}