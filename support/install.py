# install script for azcam_90prime

import os

if os.name == "posix":

    AZCAM_ROOT = "~/azcam"

    commands = [
        'sudo apt-get install python3-tk',
        f'. {AZCAM_ROOT}/venvs/azcam/bin/activate ; pip install -e {AZCAM_ROOT}/azcam-90prime',
    ]

    for command in commands:
        os.system(command)

else:

    AZCAM_ROOT = "/azcam"

    commands = [
        f'{AZCAM_ROOT}/venvs/azcam/scripts/activate.bat ',
        f'& pip install -e {AZCAM_ROOT}/azcam-90prime ',
    ]

    command = ''
    for cmd in commands:
        command = command + cmd
    os.system(command)
