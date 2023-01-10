# azcamserver config file for 90prime

import os
import sys
import ctypes

import azcam
import azcam.server
import azcam.shortcuts
from azcam.tools.cmdserver import CommandServer
from azcam.tools.system import System
from azcam.tools.arc.controller_arc import ControllerArc
from azcam.tools.arc.exposure_arc import ExposureArc
from azcam.tools.archon.controller_archon import ControllerArchon
from azcam.tools.archon.exposure_archon import ExposureArchon
from azcam.tools.archon.tempcon_archon import TempConArchon
from azcam.tools.tempcon_cryocon24 import TempConCryoCon24
from azcam.tools.ds9display import Ds9Display
from azcam.tools.sendimage import SendImage
from azcam.tools.focus import Focus

from azcam.tools.webserver.fastapi_server import WebServer
from azcam.tools.webtools.exptool.exptool import Exptool
from azcam.tools.webtools.status.status import Status

from azcam_90prime.telescope_bok import BokTCS

from azcam_90prime.instrument_pf import PrimeFocusInstrument
from azcam_90prime.instrument_pf_ngserver import PrimeFocusInstrumentUpgrade

# ****************************************************************
# parse command line arguments
# ****************************************************************
option = "menu"
try:
    i = sys.argv.index("-normal")
    option = "normal"
except ValueError:
    pass
try:
    i = sys.argv.index("-90primeone")
    option = "90primeone"
except ValueError:
    pass
try:
    i = sys.argv.index("-overscan")
    option = "overscan"
except ValueError:
    pass
try:
    i = sys.argv.index("-fast")
    option = "fast"
except ValueError:
    pass
try:
    i = sys.argv.index("-css")
    option = "css"
except ValueError:
    pass
try:
    i = sys.argv.index("-newmosaic")
    option = "newmosaic"
except ValueError:
    pass
try:
    i = sys.argv.index("-datafolder")
    datafolder = sys.argv[i + 1]
except ValueError:
    datafolder = None

try:
    i = sys.argv.index("-remotehost")
    remote_host = sys.argv[i + 1]
except ValueError:
    remote_host = None

# ****************************************************************
# define folders for system
# ****************************************************************
azcam.db.systemname = "90prime"

azcam.db.rootfolder = os.path.abspath(os.path.dirname(__file__))

azcam.db.systemfolder = os.path.dirname(__file__)
azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)

if datafolder is None:
    droot = os.environ.get("AZCAM_DATAROOT")
    if droot is None:
        droot = "/data"
    azcam.db.datafolder = os.path.join(droot, azcam.db.systemname)
else:
    azcam.db.datafolder = datafolder

# ****************************************************************
# configuration menu
# ****************************************************************
menu_options = {
    "90prime (standard mode)": "normal",
    "90primeOne": "90primeone",
    "90prime with overscan rows": "overscan",
    "90prime FAST mode (with overscan rows)": "fast",
    "CSS mode": "css",
    "New mosaic": "newmosaic",
}
if option == "menu":
    print("90Prime Startup Menu\n")
    option = azcam.utils.show_menu(menu_options)

CSS = 0
ARCHON = 0
if "90primeone" in option:
    parfile = os.path.join(azcam.db.datafolder, "parameters", "parameters_server_90prime_one.ini")
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90primeone_master.txt")
    timingfile = os.path.join(
        azcam.db.datafolder,
        "dspcode",
        "dspcode_90prime",
        "dsptiming_90primeone",
        "90PrimeOne_config0.lod",
    )
    azcam.db.servermode = "90primeone"
    cmdport = 2432
elif "normal" in option:
    parfile = os.path.join(
        azcam.db.datafolder, "parameters", "parameters_server_90prime_normal.ini"
    )
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90prime_master.txt")
    timingfile = os.path.join(
        azcam.db.datafolder,
        "dspcode",
        "dspcode_90prime",
        "dsptiming_90prime",
        "90Prime_config0.lod",
    )
    azcam.db.servermode = "normal"
    cmdport = 2402
elif "fast" in option:
    parfile = os.path.join(azcam.db.datafolder, "parameters", "parameters_server_90prime_fast.ini")
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90prime_master.txt")
    timingfile = os.path.join(
        azcam.db.datafolder,
        "dspcode",
        "dspcode_90prime",
        "dspcode_90prime",
        "dsptiming_fast",
        "90Prime_config1.lod",
    )
    azcam.db.servermode = "fast"
    cmdport = 2402
elif "overscan" in option:
    parfile = os.path.join(
        azcam.db.datafolder, "parameters", "parameters_server_90prime_overscan.ini"
    )
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90prime_master.txt")
    timingfile = os.path.join(
        azcam.db.datafolder,
        "dspcode",
        "dspcode_90prime",
        "dsptiming_90prime",
        "90Prime_config0.lod",
    )
    azcam.db.servermode = "overscan"
    cmdport = 2402
elif "css" in option:
    CSS = 1
    parfile = os.path.join(azcam.db.datafolder, "parameters", "parameters_server_90prime_css.ini")
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90prime_css.txt")
    timingfile = os.path.join(
        azcam.db.systemfolder,
        "dspcode",
        "dspcode_90prime",
        "dsptiming_90prime",
        "90Prime_config0.lod",
    )
    azcam.db.servermode = "CSS"
    cmdport = 2422
elif "newmosaic" in option:
    ARCHON = 1
    parfile = os.path.join(
        azcam.db.datafolder, "parameters", "parameters_server_90prime_newmosaic.ini"
    )
    template = os.path.join(azcam.db.datafolder, "templates", "fits_template_90prime_newmosaic.txt")
    timingfile = os.path.join(
        azcam.db.datafolder,
        "dspcode",
        "archon",
        "90prime_config0.acf",
    )
    azcam.db.servermode = "newmosaic"
    cmdport = 2442
else:
    raise azcam.AzcamError("bad server configuration")

# ****************************************************************
# logging
# ****************************************************************
logfile = os.path.join(azcam.db.datafolder, "logs", "server.log")
azcam.db.logger.start_logging(logfile=logfile)
azcam.log(f"90prime mode: {option}")

# ****************************************************************
# controller
# ****************************************************************
if ARCHON:
    controller = ControllerArchon()
    controller.timing_file = timingfile
    controller.camserver.port = 4242
    controller.camserver.host = "10.30.3.6"  # archon at Bok
    controller.reset_flag = 1  # 0 for soft reset, 1 to upload code
    controller.verbosity = 2
else:
    controller = ControllerArc()
    controller.timing_board = "arc22"
    controller.clock_boards = ["arc32"]
    controller.video_boards = ["arc47", "arc47", "arc47", "arc47"]
    controller.set_boards()
    controller.video_gain = 1
    controller.video_speed = 1
    controller.camserver.set_server("localhost", 2405)
    controller.pci_file = os.path.join(
        azcam.db.systemfolder, "dspcode", "dspcode_90prime", "dsppci", "pci3.lod"
    )
    controller.timing_file = timingfile

# ****************************************************************
# temperature controller
# ****************************************************************
if ARCHON:
    tempcon = TempConArchon(description="90prime Archon")
    tempcon.temperature_ids = [0, 2]  # camtemp, dewtemp
    tempcon.heaterx_board = "MOD1"
    tempcon.control_temperature = -95.0
    controller.heater_board_installed = 1

else:
    tempcon = TempConCryoCon24(description="90prime CryoCon")
    tempcon.control_temperature = -135.0
    # tempcon.host = "10.0.0.45"
    tempcon.host = "10.30.3.32"
    tempcon.init_commands = [
        "input A:units C",
        "input B:units C",
        "input C:units C",
        "input A:isenix 2",
        "input B:isenix 2",
        "loop 1:type pid",
        "loop 1:range mid",
        "loop 1:maxpwr 100",
    ]

# ****************************************************************
# exposure
# ****************************************************************
if ARCHON:
    exposure = ExposureArchon()
    exposure.filetype = exposure.filetypes["MEF"]
    exposure.image.filetype = exposure.filetypes["MEF"]
    # exposure.update_headers_in_background = 1
    exposure.display_image = 0
    sendimage = SendImage()
    exposure.add_extensions = 1
else:
    exposure = ExposureArc()
    exposure.filetype = exposure.filetypes["MEF"]
    exposure.image.filetype = exposure.filetypes["MEF"]
    exposure.update_headers_in_background = 1
    exposure.display_image = 0
    sendimage = SendImage()

if remote_host is None:
    pass
else:
    exposure.send_image = 1
    # sendimage.set_remote_imageserver("10.30.1.2", 6543, "dataserver")
    sendimage.set_remote_imageserver(remote_host, 6543, "dataserver")

# ****************************************************************
# instrument
# ****************************************************************
instrument = PrimeFocusInstrument()
# instrument = PrimeFocusInstrumentUpgrade()

# ****************************************************************
# telescope
# ****************************************************************
telescope = BokTCS()

# ****************************************************************
# focus
# ****************************************************************
focus = Focus()
focus.focus_component = "instrument"
focus.focus_type = "step"
focus.initialize()

# ****************************************************************
# system header template
# ****************************************************************
system = System("90prime", template)
system.set_keyword("DEWAR", "90prime", "Dewar name")

# ****************************************************************
# detector
# ****************************************************************
if "90primeone" in option:
    from azcam_90prime.detector_bok90prime import detector_bok90prime_one

    exposure.set_detpars(detector_bok90prime_one)
elif "newmosaic" in option:
    from azcam_90prime.detector_bok90prime import detector_bok90prime_newmosaic

    exposure.set_detpars(detector_bok90prime_newmosaic)
    exposure.fileconverter.set_detector_config(detector_bok90prime_newmosaic)

else:
    from azcam_90prime.detector_bok90prime import detector_bok90prime

    if "overscan" in option:
        detector_bok90prime["format"] = [4032 * 2, 6, 0, 20, 4096 * 2, 0, 0, 20, 0]
    exposure.set_detpars(detector_bok90prime)

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()

# ****************************************************************
# system-specific
# ****************************************************************
if CSS:
    from azcam_90prime.css import CSS

    css = CSS()
    azcam.db.tools["css"] = css
    if remote_host is None:
        sendimage.set_remote_imageserver("10.30.6.2", 6543, "azcam")
    else:
        sendimage.set_remote_imageserver(remote_host, 6543, "azcam")
    exposure.folder = "/home/css"

# ****************************************************************
# parameter file
# ****************************************************************
azcam.db.tools["parameters"].read_parfile(parfile)
azcam.db.tools["parameters"].update_pars(0, "azcamserver")

# ****************************************************************
# command server
# ****************************************************************
cmdserver = CommandServer()
cmdserver.port = cmdport
azcam.log(f"Starting cmdserver - listening on port {cmdserver.port}")
# cmdserver.welcome_message = "Welcome - azcam-itl server"
cmdserver.start()

# ****************************************************************
# web server
# ****************************************************************
if 1:
    webserver = WebServer()
    webserver.logcommands = 0
    webserver.index = os.path.join(azcam.db.systemfolder, "index_90prime.html")
    webserver.port = 2403  # common port for all configurations
    webserver.start()

    webstatus = Status()
    webstatus.initialize()

    exptool = Exptool()
    exptool.initialize()

# ****************************************************************
# controller server
# ****************************************************************
if ARCHON:
    pass
else:
    import azcam_90prime.restart_cameraserver

# ****************************************************************
# GUIs
# ****************************************************************
if 0:
    if os.name != "posix":
        import azcam_90prime.start_azcamtool

# cli commands
from azcam.cli import *

# try to change window title
try:
    ctypes.windll.kernel32.SetConsoleTitleW("azcamserver")
except Exception:
    pass

# ****************************************************************
# finish
# ****************************************************************
azcam.log("Configuration complete")
