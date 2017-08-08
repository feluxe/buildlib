import sys
import os
from buildlib.utils.yaml import load_yaml
from buildlib.cmds import git
from buildlib.cmds import build
from headlines import h2, h3
from buildlib.cmds.sequences import publish as prompt_seq_publish
from buildlib.cmds.sequences.publish import Answers
from buildlib.utils.semver import get_python_wheel_name_from_semver_num, convert_semver_to_wheelver

CWD = os.getcwd()
CFG_FILE = CWD + '/CONFIG.yaml'
CFG = load_yaml(CFG_FILE, keep_order=True)


def publish_sequence() -> None:
    print(h2('Publish'))

    kwargs = {
        'ask_build': True,
        'ask_registry': True,
        'cur_version': CFG['version'],
        'gemfury_env': CFG['gemfury_env'],
        }

    a: Answers = prompt_seq_publish.get_answers(**kwargs)
    result = list()

    if a.should_update_version_num:
        result.append(build.update_version_num_in_cfg_yaml(CFG_FILE, a.version))

    if a.should_run_build_py:
        result.append(build.run_build_file(CWD + '/build.py'))

    if a.should_run_git_commands:
        if a.should_run_git_add_all:
            result.append(git.add_all())

        if a.should_run_git_commit:
            result.append(git.commit(a.commit_msg))

        if a.should_run_git_tag:
            result.append(git.tag(a.version, a.branch))

        if a.should_run_git_push:
            result.append(git.push(a.branch))

    if a.should_push_registry:
        if a.should_push_gemfury:
            wheel_version_num = convert_semver_to_wheelver(a.version)
            wheel_file = get_python_wheel_name_from_semver_num(wheel_version_num, CWD + '/dist')
            result.append(build.push_python_wheel_to_gemfury('dist/' + wheel_file))

    print(h3('Publish Results'))
    for item in result:
        print(item.return_msg)


def execute() -> None:
    try:
        publish_sequence()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


if __name__ == '__main__':
    execute()
