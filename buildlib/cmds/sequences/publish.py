import prmt
from cmdinter import CmdFuncResult
from typing import Optional, Union, List
from buildlib.utils.yaml import load_yaml
from buildlib.utils.semver.prompt import prompt_semver_num_by_choice, prompt_semver_num_manually
from buildlib.cmds import build
from buildlib.utils.semver import convert_semver_to_wheelver, get_python_wheel_name_from_semver_num


def load_cfg(path):
    try:
        return load_yaml(path, keep_order=True)
    except:
        return None


def get_version(cfg_path):
    cfg = load_cfg(cfg_path)
    cur_version: str = cfg and cfg.get('version')
    if cur_version:
        return prompt_semver_num_by_choice(cur_version)
    else:
        return prompt_semver_num_manually()


def publish_sequence(
    cfg_file: Optional[str] = None,
    build_file: Optional[str] = None,
    wheel_dir: Optional[str] = None,
    run_update_version: Union[bool, str] = True,
    run_build_file: Union[bool, str] = 'y',
    run_push_gemfury: Union[bool, str] = False,
    run_push_pypi: Union[bool, str] = False,
    cur_version: Optional[str] = None,
    ) -> List[CmdFuncResult]:
    """"""
    result = []
    new_version = None

    if run_update_version:
        default = run_update_version if type(run_update_version) == str else ''
        question: str = 'Do you want to update the VERSION NUMBER before publishing? [y|n]'
        if prmt.confirm(question, default=default):
            new_version = get_version(cfg_file)
            result.append(build.update_version_num_in_cfg_yaml(cfg_file, new_version))

    if run_build_file:
        default = run_build_file if type(run_build_file) == str else ''
        question: str = 'Do you want to run "build.py" before publishing?'
        if prmt.confirm(question, default=default):
            result.append(build.run_build_file(build_file))

    if run_push_gemfury:
        default = run_push_gemfury if type(run_push_gemfury) == str else ''
        question: str = 'Do you want to push the new version to GEMFURY?'
        if prmt.confirm(question, default=default):
            version = new_version or cur_version or get_version(cfg_file)
            wheel_version_num = convert_semver_to_wheelver(version)
            wheel_file = get_python_wheel_name_from_semver_num(wheel_version_num, wheel_dir)
            result.append(build.push_python_wheel_to_gemfury(wheel_dir + '/' + wheel_file))

    if run_push_pypi:
        print('PUSHING TO PYPI NOT YET IMPLEMENTED.')

    return result
