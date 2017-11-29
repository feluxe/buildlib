import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))

from typing import Optional, List
from headlines import h3
from buildlib.utils import yaml
from buildlib.cmds import semver, git, build, pipenv
from cmdinter import CmdFuncResult, Status

CWD = os.getcwd()
CFG_FILE = 'CONFIG.yaml'
CFG = yaml.load_yaml(
    file=CFG_FILE,
    keep_order=True
)


def get_version_from_user() -> str:
    """
    Get new Version number from user or use the one from CONFIG.yaml.
    """
    return semver.prompt.semver_num_by_choice(
        cur_version=CFG.get('version')
    )


def bump_version(version: str) -> CmdFuncResult:
    """
    Bump (update) version number in CONFIG.yaml.
    """
    return build.update_version_num_in_cfg_yaml(
        config_file=CFG_FILE,
        semver_num=version,
    )


class GitBumpSettings(dict):
    version: str
    should_bump_git: Optional[bool]
    should_add_all: Optional[bool]
    should_commit: Optional[bool]
    commit_msg: Optional[str]
    should_tag: Optional[bool]
    should_push_git: Optional[bool]
    branch: Optional[str]


def get_git_settings_from_user(
    version: str,
    should_tag_default: Optional[bool],
) -> GitBumpSettings:
    """"""
    s = GitBumpSettings()
    s.version = version

    # Ask user to run any git commands.
    s.should_bump_git: bool = git.prompt.confirm_status('y') \
                              and git.prompt.confirm_diff('y')

    # Git routine
    if s.should_bump_git:
        # Ask user to run 'git add -A.
        s.should_add_all: bool = git.prompt.should_add_all(
            default='y'
        )

        # Ask user to run commit.
        s.should_commit: bool = git.prompt.should_commit(
            default='y'
        )

        # Get commit msg from user.
        if s.should_commit:
            s.commit_msg: str = git.prompt.commit_msg()

        # Ask user to run 'tag'.
        s.should_tag: bool = git.prompt.should_tag(
            default='n' if should_tag_default is False else 'y'
        )

        # Ask user to push.
        s.should_push_git: bool = git.prompt.should_push(
            default='y'
        )

        # Ask user for branch.
        if any([
            s.should_tag,
            s.should_push_git
        ]):
            s.branch: str = git.prompt.branch()

    return s


def bump_git(
    s: GitBumpSettings
) -> List[CmdFuncResult]:
    """"""
    results = []

    # If any git commands should be run.
    if s.should_bump_git:
        # Run 'add -A'
        if s.should_add_all:
            results.append(
                git.add_all()
            )

        # Run 'commit -m'
        if s.should_commit:
            results.append(
                git.commit(s.commit_msg)
            )

        # Run 'tag'
        if s.should_tag:
            results.append(
                git.tag(s.version, s.branch)
            )

        # Run 'push'
        if s.should_push_git:
            results.append(
                git.push(s.branch)
            )

    return results


def build_wheel_routine() -> None:
    """"""
    result = build.build_python_wheel(clean_dir=True)
    print(f'\n{result.summary}')


def push_registry_routine() -> None:
    """"""
    result = build.push_python_wheel_to_pypi(
        clean_dir=True
    )
    print(f'\n{result.summary}')


def bump_version_routine() -> None:
    """"""
    result = bump_version(
        version=get_version_from_user()
    )
    print(f'\n{result.summary}')


def bump_git_routine() -> None:
    """"""
    results = []

    should_bump_version = build.prompt.should_update_version(
        default='y'
    )

    if should_bump_version:
        version = get_version_from_user()
    else:
        version = CFG.get('version')

    git_settings = get_git_settings_from_user(
        should_tag_default=version != CFG.get('version'),
        version=version,
    )

    if should_bump_version:
        results.append(bump_version(version))

    results += bump_git(git_settings)

    print('')
    for result in results:
        print(result.summary)


def bump_routine() -> None:
    """"""
    results = []

    should_bump_version: bool = build.prompt.should_update_version(
        default='y'
    )

    if should_bump_version:
        version = get_version_from_user()
    else:
        version = CFG.get('version')

    should_build_wheel: bool = build.prompt.should_build_wheel(
        default='y'
    )

    should_push_registry: bool = build.prompt.should_push_pypi(
        default='y' if should_bump_version else 'n'
    )

    if should_bump_version:
        results.append(bump_version(version))

    git_settings = get_git_settings_from_user(
        should_tag_default=version != CFG.get('version'),
        version=version,
    )

    if should_build_wheel:
        results.append(build.build_python_wheel(clean_dir=True))

    if git_settings.should_bump_git:
        results += bump_git(git_settings)

    if should_push_registry:
        results.append(build.push_python_wheel_to_pypi(
            clean_dir=True
        ))

    for result in results:
        print(result.summary)


if __name__ == '__main__':
    try:
        args = sys.argv

        if args[1] == 'init':
            print(pipenv.install(dev=True).summary)

        elif args[1] == 'build-wheel':
            build_wheel_routine()

        elif args[1] == 'push-registry':
            push_registry_routine()

        elif args[1] == 'bump-version':
            bump_version_routine()

        elif args[1] == 'bump-git':
            bump_git_routine()

        elif args[1] == 'bump':
            bump_routine()


    except KeyboardInterrupt:
        print('\n\nScript aborted by user.\n')
        sys.exit(1)
