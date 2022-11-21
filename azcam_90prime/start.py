"""
Start script for azcam_90prime package.
Runs azamserver or azcamconsole

Usage Example:
>> ipython -m azcam_90prime.start -i -- -console
"""

import sys

# set defaults
CONSOLE = False
SERVER = True

args = sys.argv[1:]

if "-console" in args:
    CONSOLE = True
    SERVER = False
if "-server" in args:
    CONSOLE = False
    SERVER = True

if SERVER:
    import azcam_90prime.server
    from azcam.cli import *

elif CONSOLE:
    import azcam_90prime.console
    from azcam.cli import *
