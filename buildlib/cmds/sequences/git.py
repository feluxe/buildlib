import prmt
from typing import NamedTuple, Union, List, Optional
from headlines import h3
from cmdinter import CmdFuncResult
from buildlib.utils.yaml import load_yaml
from buildlib.cmds import git
from buildlib.cmds.git.prompt import prompt_commit_msg, prompt_branch
from buildlib.utils.semver.prompt import prompt_semver_num_by_choice, prompt_semver_num_manually
from buildlib.cmds.build import update_version_num_in_cfg_yaml


def load_cfg(path):
    try:
        return load_yaml(path, keep_order=True)
    except:
        return None


def get_cur_version(cfg_file):
    cfg = load_cfg(cfg_file)
    cur_version: str = cfg and cfg.get('version')
    return cur_version


def get_new_version(cur_version):
    if cur_version:
        return prompt_semver_num_by_choice(cur_version)
    else:
        return prompt_semver_num_manually()


def git_sequence(
    cfg_file: Optional[str] = None,
    show_status: Union[bool, str] = 'y',
    show_diff: Union[bool, str] = 'y',
    run_update_version: Union[bool, str] = 'n',
    run_add_all: Union[bool, str] = 'y',
    run_commit: Union[bool, str] = 'y',
    run_tag: Union[bool, str] = 'n',
    run_push: Union[bool, str] = 'y',
    cur_version: Optional[str] = None,
    new_version: Optional[str] = None,
    branch: Optional[str] = None,
    ) -> List[CmdFuncResult]:
    """"""
    result = []

    if show_status:
        print(h3('Git Status'))
        git.status()
        default = show_status if type(show_status) == str else ''
        question: str = 'Is the current GIT STATUS ok"?'
        if not prmt.confirm(question, default=default):
            return result

    if show_diff:
        print(h3('Git Diff'))
        git.diff()
        default = show_diff if type(show_diff) == str else ''
        question: str = 'Is the current GIT DIFF ok"?'
        if not prmt.confirm(question, default=default):
            return result

    if run_update_version:
        default = run_update_version if type(run_update_version) == str else ''
        question: str = 'Do you want to update the VERSION NUMBER? [y|n]'
        if prmt.confirm(question, default=default):
            cur_version = cur_version or get_cur_version(cfg_file)
            new_version = get_new_version(cur_version)
            result.append(update_version_num_in_cfg_yaml(cfg_file, new_version))

    if run_add_all:
        default = run_add_all if type(run_add_all) == str else ''
        question: str = 'Do you want to run GIT ADD ALL ("git add --all")?'
        if prmt.confirm(question, default=default):
            result.append(git.add_all())

    if run_commit:
        default = run_commit if type(run_commit) == str else ''
        question: str = 'Do you want to run GIT COMMIT?'
        if prmt.confirm(question, default=default):
            commit_msg = prompt_commit_msg()
            result.append(git.commit(commit_msg))

    if run_tag:
        default = run_tag if type(run_tag) == str else ''
        question: str = 'Do you want to GIT TAG with current version number?'
        if prmt.confirm(question, default=default):
            branch = branch or prompt_branch()
            version = new_version or cur_version or get_cur_version(cfg_file)
            result.append(git.tag(version, branch))

    if run_push:
        default = run_push if type(run_push) == str else ''
        question: str = 'Do you want to GIT PUSH current state to GITHUB?'
        if prmt.confirm(question, default=default):
            branch = branch or prompt_branch()
            result.append(git.push(branch))

    return result
