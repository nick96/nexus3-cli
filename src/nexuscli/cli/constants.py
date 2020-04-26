import os
from subprocess import CalledProcessError

ENV_VAR_PREFIX = 'NEXUS3'

try:
    _, TTY_MAX_WIDTH = os.popen('stty size', 'r').read().split()
    TTY_MAX_WIDTH = int(TTY_MAX_WIDTH)
except (ValueError, CalledProcessError):
    TTY_MAX_WIDTH = 80
