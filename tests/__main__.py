"""
"""

import sys
import os
# import tests.npm as npm

# npm.test_bump_version()
# npm.test_bump_version(as_cmd=True)

from buildlib import git

import io
o = io.StringIO()
r = git.cmd.log("-5", reverse=True, _verbose=False)


