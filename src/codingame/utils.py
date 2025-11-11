"""Some utils to copy from task to task... (we cant import them since every challenge must be completed in a single file"""

import os
import sys


def debug(msg):
    print(msg, file=sys.stderr, flush=True)


DEBUG = os.getenv("DEBUG")
