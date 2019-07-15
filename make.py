"""
Install:
  pipenv install --dev --pre
  pipenv run python make.py

Usage:
  make.py build
  make.py push
  make.py test
  make.py bump
  make.py git
  make.py -h | --help

Options:
  -h, --help               Show this screen.
"""

import sys
import os
import subprocess as sp
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from cmdi import print_summary
from buildlib import buildmisc, git, wheel, project, yaml
from docopt import docopt

proj = yaml.loadfile('Project')


class Cfg:
    version = proj['version']
    registry = 'pypi'


def build(cfg: Cfg):
    return wheel.cmd.build(clean_dir=True)


def push(cfg: Cfg):
    w = wheel.find_wheel('./dist', semver_num=cfg.version)
    return wheel.cmd.push(f'./dist/{w}')


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
        r.append(push(cfg))

    return r


def run():

    cfg = Cfg()
    args = docopt(__doc__)
    results = []

    if args['build']:
        results.append(build(cfg))

    if args['push']:
        results.append(push(cfg))

    if args['test']:
        test(cfg)

    if args['git']:
        results.extend(git.seq.bump_git(cfg.version, new_release=False))

    if args['bump']:
        results.extend(bump(cfg))

    print_summary(results)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user.')
