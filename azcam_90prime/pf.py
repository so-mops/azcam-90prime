import os
import sys

def main():
    """
    Startup script for azcam-90prime.
    """

    args=sys.argv[1:]

    cmds = [
        "wt -w azcam --title AzCamServer --tabColor #000099 pf_commands.ps1",
        f" -- {' '.join(args)}",
    ]
    
    command = " ".join(cmds)
    print(command)

    os.system(command)

if __name__ == '__main__':
    main()