# start script for azcam_90prime

import os

if os.name == "posix":
    pass
    # AZCAM_DATAROOT="/home/lesser/data"
    # export AZCAM_DATAROOT
    # echo AzCam data root is $AZCAM_DATAROOT
    # echo Activating azcam virtual environment
    # source ~/azcam/venvs/azcam/bin/activate
    # ipython --profile azcamserver -i -c "import azcam_90prime.server; from azcam.cli import *"

else:
    AZCAM_DATAROOT='/data'
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT
    AZCAM_AZCAMTOOL='C:\\azcam\\azcam-tool\\azcam_tool\\builds\\azcamtool.exe'
    os.environ['AZCAM_AZCAMTOOL']=AZCAM_AZCAMTOOL

    print(f'AzCam data root is {AZCAM_DATAROOT}')

    print('Activating azcam virtual environment')

    command = "\\data\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server\""
    os.system(command)

