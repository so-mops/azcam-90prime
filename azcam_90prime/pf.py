"""
Startup command for azcam-90prime
Usage:
  python pf.py -console
  python pf.py -server -normal

For installations, this is the "pf" command.
"""

import os
import sys

def main():

    args=sys.argv[1:]

    if "-console" in args:
        tabColor = "#000099"
        tabTitle = "azcamconsole"
    elif "-server" in args:
        tabColor = "#990000"
        tabTitle = "azcamserver"
    else:
        print("Usage error: -server or -console required")
        return

    if os.name == "posix":
        cmds = [
            ". ~/azcam/venvs/azcam/bin/activate ; python3 -m azcam_90prime.primefocus",
            f"{' '.join(args)}",
        ]    
    else:
        cmds = [
            f"wt -w azcam --suppressApplicationTitle=True --title {tabTitle} --tabColor {tabColor}",
            "cmd /k",
            "\"/azcam/venvs/azcam/Scripts/activate.bat & python -m azcam_90prime.primefocus\"",
            f"{' '.join(args)}",
        ]    
    command = " ".join(cmds)
    os.system(command)

if __name__ == '__main__':
    main()
