# install script for azcam_90prime

import os

if os.name == "posix":

    commands = [
        'sudo apt-get install python3-tk',
        '. ~/azcam/venvs/azcam/bin/activate',
        'cd ~/azcam',
        'pip install -e ~/azcam/azcam-90prime'
    ]

    for command in commands:
        print(command)
        os.system(command)

else:
    AZCAM_DATAROOT='/data'
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT

    AZCAM_AZCAMTOOL='C:\\azcam\\azcam-tool\\azcam_tool\\builds\\azcamtool.exe'
    os.environ['AZCAM_AZCAMTOOL']=AZCAM_AZCAMTOOL

    print(f'AzCam data root is {AZCAM_DATAROOT}')

    print('Activating azcam virtual environment')
    command = "\\data\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server\""
    os.system(command)

