# install script for azcam_90prime

import os

if os.name == "posix":

    AZCAM_ROOT = "~/azcam"

    commands = [
        'sudo apt-get install python3-tk',
        f'. {AZCAM_ROOT}/venvs/azcam/bin/activate',
        f'pip install -e {AZCAM_ROOT}/azcam-90prime'
    ]

    for command in commands:
        print(command)
        os.system(command)

else:

    AZCAM_ROOT = "/azcam"

    commands = [
        f'{AZCAM_ROOT}/venvs/azcam/scripts/activate.ps1 & pip install -e {AZCAM_ROOT}/azcam-90prime'
    ]

    for command in commands:
        print(command)
        os.system(command)


    # command = "\\data\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server\""
    # os.system(command)

