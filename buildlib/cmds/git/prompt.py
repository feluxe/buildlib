import prmt
from buildlib.cmds.git import get_default_branch
from cmdinter import run_cmd


def prompt_commit_msg() -> str:
    question: str = 'Enter a COMMIT message:'
    return prmt.string(question, force_value=True)


def prompt_branch() -> str:
    question: str = 'Enter the BRANCH name you want to push to:'
    return prmt.string(question, default=run_cmd(silent=True)(get_default_branch).return_val)
