"""
Python process start file
"""

import subprocess

OPTIONS = "-overscan"
CMD = f"ipython --ipython-dir=/data/ipython --profile azcamserver -i -m azcam_90prime.server -- {OPTIONS}"

p = subprocess.Popen(
    CMD,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
