# start script for azcam_90prime

import os
import sys

args=[]
try:
    i = sys.argv.index("-system")
    system = sys.argv[i + 1]
    args.append("-system")
    args.append(system)
except ValueError:
    system = None

if os.name == "posix":
    AZCAM_DATAROOT="/home/lesser/data"
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT
    print(f'AzCam data root is {AZCAM_DATAROOT}')

    print('Activating azcam virtual environment')
    command = f". /home/lesser/azcam/venvs/azcam/bin/activate ; ipython --profile azcamserver -i -c \"import azcam_90prime.server ; from azcam.cli import *\" -- {' '.join(args)}"
    os.system(command)

else:
    AZCAM_DATAROOT='/data'
    os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT

    AZCAM_AZCAMTOOL='C:\\azcam\\azcam-tool\\azcam_tool\\builds\\azcamtool.exe'
    os.environ['AZCAM_AZCAMTOOL']=AZCAM_AZCAMTOOL

    print('Activating azcam virtual environment')
    command = f"\\azcam\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server ; from azcam.cli import *\" -- {' '.join(args)}"
    os.system(command)

