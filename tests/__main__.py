"""
"""

import sys
import os
import tests.npm as npm

npm.test_bump_version()
npm.test_bump_version(as_cmd=True)

print('\nTests Finished')
