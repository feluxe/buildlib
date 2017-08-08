import sys
from typing import NamedTuple

import prmt
from headlines import h3

from buildlib.cmds import git
from cmds.git.prompt import prompt_branch, prompt_commit_msg


class Answers(NamedTuple):
    should_run_git_add_all: bool
    should_run_git_commit: bool
    commit_msg: str
    should_run_git_tag: bool
    should_run_git_push: bool
    branch: str


def get_answers() -> Answers:
    """"""

    print(h3('Git Status'))
    git.status()
    question: str = 'Is the current git status ok"?'
    if not prmt.confirm(question, default='y'):
        sys.exit(1)

    print(h3('Git Diff'))
    git.diff()
    question: str = 'Is the current git diff ok"?'
    if not prmt.confirm(question, default='y'):
        sys.exit(1)

    question: str = 'Do you want to run "git add --all"?'
    should_run_git_add_all = prmt.confirm(question, default='y')

    question: str = 'Do you want to run git COMMIT?'
    should_run_git_commit = prmt.confirm(question, default='y')

    commit_msg = prompt_commit_msg() if should_run_git_commit else None

    question: str = 'Do you want to TAG with current version number?'
    should_run_git_tag = prmt.confirm(question, default='n')

    question: str = 'Do you want to PUSH current state to GITHUB?'
    should_run_git_push = prmt.confirm(question, default='y')

    branch = prompt_branch() if should_run_git_tag or should_run_git_push else None

    return Answers(
        should_run_git_add_all=should_run_git_add_all,
        should_run_git_commit=should_run_git_commit,
        commit_msg=commit_msg,
        should_run_git_tag=should_run_git_tag,
        should_run_git_push=should_run_git_push,
        branch=branch,
        )
