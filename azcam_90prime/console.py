# azcamconsole config file

import os
import sys
import threading
import ctypes

import azcam
import azcam_console.console
import azcam_console.shortcuts
import azcam_console.tools.console_tools
from azcam_console.tools.ds9display import Ds9Display
from azcam_console.tools.focus import FocusConsole

try:
    i = sys.argv.index("-datafolder")
    datafolder = sys.argv[i + 1]
except ValueError:
    datafolder = None

# ****************************************************************
# files and folders
# ****************************************************************
azcam.db.systemname = "90prime"

azcam.db.systemfolder = f"{os.path.dirname(__file__)}"

if datafolder is None:
    droot = os.environ.get("AZCAM_DATAROOT")
    if droot is None:
        droot = "/data"
    azcam.db.datafolder = os.path.join(droot, azcam.db.systemname)
else:
    azcam.db.datafolder = datafolder
azcam.db.datafolder = azcam.utils.fix_path(azcam.db.datafolder)

parfile = os.path.join(
    azcam.db.datafolder, "parameters", f"parameters_console_{azcam.db.systemname}.ini"
)

# ****************************************************************
# start logging
# ****************************************************************
logfile = os.path.join(azcam.db.datafolder, "logs", "console.log")
azcam.db.logger.start_logging(logfile=logfile)
azcam.log(f"Configuring console for {azcam.db.systemname}")

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()
dthread = threading.Thread(target=display.initialize, args=[])
dthread.start()  # thread just for speed

# ****************************************************************
# console tools
# ****************************************************************
from azcam_console.tools import create_console_tools

create_console_tools()

# ****************************************************************
# observe
# ****************************************************************
azcam.log("Loading observe")
from azcam_observe.observe_cli.observe_cli import ObserveCli

observe = ObserveCli()
observe.move_telescope_during_readout = 1

# ****************************************************************
# focus tool
# ****************************************************************
focus = FocusConsole()
focus.focus_component = "instrument"
focus.focus_type = "step"

# ****************************************************************
# try to connect to azcamserver
# ****************************************************************
ports = [2402, 2412, 2422, 2432, 2442]
connected = 0
server = azcam.db.tools["server"]
for port in ports:
    connected = server.connect(port=port)
    if connected:
        break

if connected:
    azcam.log("Connected to azcamserver")
else:
    azcam.log("Not connected to azcamserver")

# ****************************************************************
# parameter file
# ****************************************************************
azcam.db.parameters.read_parfile(parfile)
azcam.db.parameters.update_pars("azcamconsole")

# cli commands
from azcam.cli import *

# try to change window title
try:
    ctypes.windll.kernel32.SetConsoleTitleW("azcamconsole")
except Exception:
    pass
