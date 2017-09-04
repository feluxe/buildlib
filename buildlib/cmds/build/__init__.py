import os
import shutil
from processy import run, ProcResult
from cmdinter import CmdFuncResult, Status
from buildlib.cmds.build import prompt
from buildlib.utils import yaml, module


def update_version_num_in_cfg_yaml(
    config_file: str,
    semver_num: str,
) -> CmdFuncResult:
    """
    Check if version num from proj-cfg is valid.
    Increase version num based on user input or ask user for a new version number.
    """
    title = 'Update Version Num In Config Yaml.'

    cfg: dict = yaml.load_yaml(
        config_file,
        keep_order=True
    )

    cfg.update({'version': semver_num})

    yaml.save_yaml(cfg, config_file)

    return CmdFuncResult(
        return_code=0,
        return_msg=Status.ok + title,
        return_val=None
    )


def push_python_wheel_to_gemfury(
    wheel_file: str
) -> CmdFuncResult:
    """"""
    title = 'Push Python Wheel to Gemfury.'

    if not os.path.isfile(wheel_file):
        print('Warning: Could not find wheel to push to Gemfury.')
        return_code: int = 1

    else:
        p: ProcResult = run(
            cmd=['fury', 'push', wheel_file],
            return_stdout=True
        )

        if 'this version already exists' in p.out:
            return_code: int = 1

        else:
            return_code: int = p.return_code

    if return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=return_code,
        return_msg=status + title,
        return_val=None
    )


def push_python_wheel_to_pypi() -> CmdFuncResult:
    """"""
    title = 'Push Python Wheel to Pypi.'

    p: ProcResult = run(cmd=['python', 'setup.py', 'bdist_wheel', 'upload', '-r', 'pypi'])

    return_code: int = p.return_code

    if return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=return_code,
        return_msg=status + title,
        return_val=None
    )


def build_python_wheel(
    clean_dir: bool = False
) -> CmdFuncResult:
    """
    Build python wheel for deployment, if it does not exists already.
    @clean_dir: Clean 'build' dir before running build command. This may be necessary because of
    this: https://bitbucket.org/pypa/wheel/issues/147/bdist_wheel-should-start-by-cleaning-up
    """
    title = 'Build Python Wheel.'

    build_dir: str = os.getcwd() + '/build'

    if clean_dir and os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    p: ProcResult = run(cmd=['python', 'setup.py', 'bdist_wheel'])

    if clean_dir and os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def inject_interface_txt_into_readme_md(
    interface_file: str,
    readme_file: str = 'README.md',
) -> CmdFuncResult:
    """
    Add content of help.txt into README.md
    Content of help.txt will be placed into the first code block (```) of README.md.
    If no code block is found, a new one will be added to the beginning of README.md.
    """
    title = 'Inject interface.txt into README.md.'

    readme_content: str = open(readme_file, 'r').read()
    help_content: str = '```\n{}\n```'.format(open(interface_file, 'r').read())

    start: int = readme_content.find('```') + 3
    end: int = readme_content.find('```', start)

    if '```' in readme_content:
        mod_content: str = readme_content[0:start - 3] + \
                           help_content + \
                           readme_content[end + 3:]

    else:
        mod_content: str = help_content + readme_content

    with open('README.md', 'w') as modified_readme:
        modified_readme.write(mod_content)

    return CmdFuncResult(
        return_code=0,
        return_msg=Status.ok + title,
        return_val=None
    )


def run_build_file(build_file: str) -> CmdFuncResult:
    """"""
    title = 'Run Build File.'

    build_module = module.load_module_from_file(build_file)
    build_module.execute()

    # Add empty line
    print('\n')

    return CmdFuncResult(
        return_code=0,
        return_msg=Status.ok + title,
        return_val=None
    )


def build_read_the_docs(clean_dir: bool = False) -> CmdFuncResult:
    """"""
    title = 'Build Read The Docs.'

    build_dir = '{}/docs/build'.format(os.getcwd())

    if clean_dir and os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    p: ProcResult = run(
        cmd=['make', 'html'],
        cwd='{}/docs'.format(os.getcwd())
    )

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def create_py_venv(
    py_bin: str,
    venv_dir: str,
) -> CmdFuncResult:
    """
    @interpreter: must be the exact interpreter name. E.g. 'python3.5'
    """
    title = 'Create Python Virtual Environment.'
    cmd: list = [py_bin, '-m', 'venv', venv_dir]

    p: ProcResult = run(cmd)

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def create_autoenv(
    venv_dir: str,
) -> CmdFuncResult:
    """
    Create autoenv for automatic activation of virtual env when cd into dir.
    """
    title = 'Create Auto Env File.'

    venv_dir = os.path.normpath(venv_dir)
    venv_parent_dir: str = os.path.dirname(venv_dir)
    env_file_path: str = '{}/.env'.format(venv_parent_dir)

    with open(env_file_path, 'w+') as f:
        f.write('source {}/bin/activate\n'.format(venv_dir))

    return CmdFuncResult(
        return_code=0,
        return_msg=Status.ok + title,
        return_val=None
    )
