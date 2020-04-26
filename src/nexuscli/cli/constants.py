import os
from subprocess import CalledProcessError

ENV_VAR_PREFIX = 'NEXUS3'

try:
    _, TTY_MAX_WIDTH = os.popen('stty size', 'r').read().split()
    TTY_MAX_WIDTH = int(TTY_MAX_WIDTH)
except (ValueError, CalledProcessError):
    TTY_MAX_WIDTH = 80

# see cli.util.get_client()
REQUIRED_NEXUS_OPTIONS = ['PASSWORD', 'USERNAME', 'URL']
OPTIONAL_NEXUS_OPTIONS = ['API_VERSION', 'X509_VERIFY']
