# start script for azcam_90prime

import os

if os.name == "posix":
    AZCAM_DATAROOT="/home/lesser/data"
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT
    print(f'AzCam data root is {AZCAM_DATAROOT}')

    print('Activating azcam virtual environment')
    command = ". /home/lesser/azcam/venvs/azcam/bin/activate ; ipython --profile azcamserver -i -c \"import azcam_90prime.server ; from azcam.cli import *\""
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

