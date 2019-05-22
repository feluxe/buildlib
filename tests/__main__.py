"""
"""

import sys
import os
# import tests.npm as npm

# npm.test_bump_version()
# npm.test_bump_version(as_cmd=True)

from buildlib import yaml

yaml.loadfile('test.yaml', safe=False)

print('\nTests Finished')
