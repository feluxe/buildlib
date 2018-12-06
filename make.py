import sys
import os
import subprocess as sp
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from cmdi import print_summary
from buildlib import buildmisc, git, wheel, project, yaml
from docopt import docopt

interface = """
    Install:
        pipenv install --dev --pre
        pipenv run python make.py

    Usage:
        make.py build [options]
        make.py deploy [options]
        make.py test [options]
        make.py bump [options]
        make.py git [options]
        make.py -h | --help

    Options:
    -h, --help               Show this screen.
"""

proj = yaml.loadfile('Project')


class Cfg:
    version = proj['version']
    registry = 'pypi'


def build(cfg: Cfg):
    return wheel.cmd.build(clean_dir=True)


def deploy(cfg: Cfg):
    return wheel.cmd.push(clean_dir=True, repository=cfg.registry)


def test(cfg: Cfg):
    sp.run(['pipenv', 'run', 'python', '-m', 'tests'])


def bump(cfg: Cfg):

    r = []

    if project.prompt.should_bump_version():
        result = project.cmd.bump_version()
        cfg.version = result.val
        r.append(result)

    new_release = cfg.version != proj['version']

    r.extend(git.seq.bump_git(cfg.version, new_release))

    if wheel.prompt.should_push('PYPI'):
        r.append(deploy(cfg))

    return r


def run():

    cfg = Cfg()
    uinput = docopt(interface)
    results = []

    if uinput['build']:
        results.append(build(cfg))

    if uinput['deploy']:
        results.append(deploy(cfg))

    if uinput['test']:
        test(cfg)

    if uinput['git']:
        results.extend(git.seq.bump_git(cfg.version, new_release=False))

    if uinput['bump']:
        results.extend(bump(cfg))

    print_summary(results)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user.')
