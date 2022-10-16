# start script for azcam_90prime

import os
import sys

def main():
    """
    Startup script for azcam-90prime.
    """

    CONSOLE = False
    SERVER = True  # default

    args=sys.argv[1:]

    if "-console" in args:
        CONSOLE = True
        SERVER = False
    if "-server" in args:
        CONSOLE = False
        SERVER = True

    if os.name == "posix":
        AZCAM_DATAROOT="/home/lesser/data"
        os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT
        print(f'AzCam data root is {AZCAM_DATAROOT}')

        command = f". /home/lesser/azcam/venvs/azcam/bin/activate ; ipython --profile azcamserver -i -c \"import azcam_90prime.server ; from azcam.cli import *\" -- {' '.join(args)}"
        os.system(command)

    else:
        AZCAM_DATAROOT='/data'
        os.environ['AZCAM_DATAROOT']=AZCAM_DATAROOT

        if SERVER:
            #command = f"\\azcam\\venvs\\azcam\\Scripts\\activate.bat & ipython --profile azcamserver -i -c \"import azcam_90prime.server ; from azcam.cli import *\" -- {' '.join(args)}"
            cmds = [
                #"wt -w azcam --title AzCamServer --tabColor #000099 &",
                #"\\azcam\\azcam-90prime\\support\\start_server_venv1.bat",
                "ipython --profile azcamserver -i -c" ,
                "\"import azcam_90prime.server ; from azcam.cli import *\"",
                f" -- {' '.join(args)}",
            ]
        if CONSOLE:
            cmds = [
                #"wt -w azcam --title AzCamConsole --tabColor #000099 &",
                #"\\azcam\\azcam-90prime\\support\\start_console_venv1.bat",
                # "\\azcam\\venvs\\azcam\\Scripts\\activate.bat",
                "ipython --profile azcamconsole -i -c" ,
                "\"import azcam_90prime.console ; from azcam.cli import *\"",
                f" -- {' '.join(args)}",
            ]
        
        command = " ".join(cmds)
        os.system(command)

if __name__ == '__main__':
    main()