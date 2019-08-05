"""Install:
  pipenv install --dev --pre

Usage:
  make.py [<command>] [options]

Commands:
  build    Build wheel.
  push     Push wheel to pypi.
  test     Run tests.
  bump     Run interacitve bump sequence.
  git      Run interactive git sequence.

Options:
  -h, --help  Show this screen.
"""
import sys
import os
import subprocess as sp
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from cmdi import print_summary
import prmt
from buildlib import buildmisc, git, wheel, project, yaml
from docopt import docopt

proj = yaml.loadfile('Project')


class Cfg:
    version = proj['version']
    registry = 'pypi'


def build(cfg: Cfg):
    return wheel.cmd.build(cleanup=True)


def push(cfg: Cfg):
    w = wheel.find_wheel('./dist', semver_num=cfg.version)
    return wheel.cmd.push(f'./dist/{w}')


def test(cfg: Cfg):
    sp.run(['pipenv', 'run', 'python', '-m', 'tests'])


def bump(cfg: Cfg):

    r = []

    if prmt.confirm("BUMP VERSION number?", 'y'):
        result = project.cmd.bump_version()
        cfg.version = result.val
        r.append(result)

    if prmt.confirm("BUILD wheel?", 'y'):
        r.append(build(cfg))

    if prmt.confirm("PUSH wheel to PYPI?", 'y'):
        r.append(push(cfg))

    new_release = cfg.version != proj['version']

    r.extend(git.seq.bump_git(cfg.version, new_release))

    return r


def run():

    cfg = Cfg()
    args = docopt(__doc__)
    results = []

    if args['<command>'] == 'build':
        results.append(build(cfg))

    elif args['<command>'] == 'push':
        results.append(push(cfg))

    elif args['<command>'] == 'test':
        test(cfg)

    elif args['<command>'] == 'git':
        results.extend(git.seq.bump_git(cfg.version, new_release=False))

    elif args['<command>'] == 'bump':
        results.extend(bump(cfg))

    else:
        print(__doc__)
        return

    print_summary(results)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user.')
