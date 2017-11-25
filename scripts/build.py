import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))

from typing import Optional
from headlines import h3
from buildlib.utils.yaml import load_yaml
from buildlib.cmds import semver
from buildlib.cmds import git
from buildlib.cmds import build


def bump_routine(
    should_bump_version: Optional[bool] = None,
    should_build_wheel: Optional[bool] = None,
    should_bump_git: Optional[bool] = None,
    should_push_registry: Optional[bool] = None,
) -> None:
    """"""
    print('')

    results = []
    cfg_file = 'CONFIG.yaml'

    cur_version: str = load_yaml(
        file=cfg_file,
        keep_order=True
    ).get('version')

    if should_bump_version is None:
        should_bump_version: bool = build.prompt.should_update_version(
            default='y'
        )

    if should_bump_version:
        version: str = semver.prompt.semver_num_by_choice(
            cur_version=cur_version
        )
    else:
        version: str = cur_version

    if should_build_wheel is None:
        should_build_wheel: bool = build.prompt.should_build_wheel(
            default='y'
        )

    if should_bump_version:
        results.append(
            build.update_version_num_in_cfg_yaml(
                config_file=cfg_file,
                semver_num=version
            )
        )

    if should_build_wheel:
        results.append(
            build.build_python_wheel(clean_dir=True)
        )

    if should_push_registry is None:
        should_push_registry: bool = build.prompt.should_push_pypi(
            default='y' if should_bump_version else 'n'
        )

    if should_bump_git is None:
        should_bump_git: bool = git.prompt.should_run_any('y')

    if should_bump_git:
        should_bump_git: bool = all([
            git.prompt.confirm_status('y'),
            git.prompt.confirm_diff('y')
        ])

    if should_bump_git:
        should_add_all: bool = git.prompt.should_add_all(
            default='y'
        )

        should_commit: bool = git.prompt.should_commit(
            default='y'
        )

        if should_commit:
            commit_msg: str = git.prompt.commit_msg()

        should_tag: bool = git.prompt.should_tag(
            default='y' if should_bump_version else 'n'
        )

        should_push_git: bool = git.prompt.should_push(
            default='y'
        )

        if any([
            should_tag,
            should_push_git
        ]):
            branch: str = git.prompt.branch()

        if should_add_all:
            results.append(
                git.add_all()
            )

        if should_commit:
            results.append(
                git.commit(commit_msg)
            )

        if should_tag:
            results.append(
                git.tag(version, branch)
            )

        if should_push_git:
            results.append(
                git.push(branch)
            )

    if should_push_registry:
        results.append(
            build.push_python_wheel_to_pypi(
                clean_dir=True
            )
        )

    print(h3('Publish Results'))

    for i, result in enumerate(results):
        print(result.summary)


if __name__ == '__main__':
    try:
        args = sys.argv

        if args[1] == 'bump':
            bump_routine()

        elif args[1] == 'bump-version':
            bump_routine(
                should_bump_version=True,
            )

        elif args[1] == 'build-wheel':
            bump_routine(
                should_build_wheel=True,
                should_bump_git=False,
                should_push_registry=False,
            )

        elif args[1] == 'bump-git':
            bump_routine(
                should_bump_git=True,
                should_build_wheel=False,
                should_push_registry=False,
            )

        elif args[1] == 'push-registry':
            bump_routine(
                should_push_registry=True,
                should_bump_git=False,
                should_build_wheel=False,
            )

    except KeyboardInterrupt:
        print('\n\nScript aborted by user.\n')
        sys.exit(1)
