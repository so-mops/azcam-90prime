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

    AZCAM_ROOT='/azcam'
    os.environ['AZCAM_ROOT']=AZCAM_ROOT

    AZCAM_DATAROOT='/data'
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT

    AZCAM_AZCAMTOOL='C:\\azcam\\azcam-tool\\azcam_tool\\builds\\azcamtool.exe'
    os.environ['AZCAM_AZCAMTOOL']=AZCAM_AZCAMTOOL

    # print('Activating azcam virtual environment')
    # command = "\\data\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server\""
    # os.system(command)

