"""
"""
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join('../..', 'buildlib')))
from buildlib import npm


def test_bump_version(as_cmd=False):

    packagejson = 'tests/npm/package.json'
    version = ''

    with open(packagejson) as f:
        data = json.load(f)
        version = data['version']

    assert version == '0.0.1'

    if as_cmd:
        npm.cmd.bump_version(new_version='0.0.2', filepath=packagejson)
    else:
        npm.bump_version(new_version='0.0.2', filepath=packagejson)

    with open(packagejson) as f:
        data = json.load(f)
        version = data['version']

    assert version == '0.0.2'

    npm.bump_version(new_version='0.0.1', filepath=packagejson)
