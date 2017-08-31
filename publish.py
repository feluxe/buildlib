import sys
import os
from headlines import h3
from buildlib.utils.yaml import load_yaml
from buildlib.cmds.sequences import publish as publish_seq
from buildlib.cmds.sequences import git as git_seq

cwd = os.getcwd()
cfg_file = cwd + '/CONFIG.yaml'
build_file = cwd + '/build.py'
wheel_dir = cwd + '/dist'


def load_cfg():
    return load_yaml(cfg_file, keep_order=True)


def get_version_from_cfg():
    return load_cfg().get('version')


def publish() -> None:
    """"""

    publish_seq_args_1 = publish_seq.get_args_interactively(
        run_update_version='y',
        run_build_file='y',
        build_file=build_file,
        cur_version=get_version_from_cfg(),
    )

    results_1 = [*publish_seq.run_seq(**publish_seq_args_1)]

    git_seq_args = git_seq.get_args_interactively(
        run_any='y',
        confirm_status='y',
        confirm_diff='y',
        run_add_all='y',
        run_commit='y',
        run_tag='y',
        run_push='y',
        new_version=publish_seq_args_1.get('version') or get_version_from_cfg()
    )

    publish_seq_args_2 = publish_seq.get_args_interactively(
        run_push_pypi='y',
        cfg_file=cfg_file,
        wheel_dir=wheel_dir,
        new_version=publish_seq_args_1.get('version') or get_version_from_cfg()
    )

    results = [*git_seq.run_seq(**git_seq_args), *publish_seq.run_seq(**publish_seq_args_2)]

    print(h3('Publish Results'))

    for result in results:
        print(result.return_msg)


def execute() -> None:
    try:
        publish()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


if __name__ == '__main__':
    execute()
