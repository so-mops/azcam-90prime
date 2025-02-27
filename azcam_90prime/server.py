"""
Setup method for 90prime azcamserver.
Usage example:
  python -i -m azcam_90prime.server -- -archon
"""

import os
import sys

import azcam
import azcam.utils
import azcam.exceptions
from azcam.server import setup_server
import azcam.shortcuts
from azcam.cmdserver import CommandServer
from azcam.header import System
from azcam.tools.ds9display import Ds9Display
from azcam.tools.focus import Focus
from azcam.web.fastapi_server import WebServer

from azcam_90prime.telescope_bok import BokTCS
from azcam_90prime.instrument_pf import PrimeFocusInstrument
from azcam_90prime.instrument_pf_ngserver import PrimeFocusInstrumentUpgrade


def setup():

    # command line args
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
        i = sys.argv.index("-archon")
        option = "archon"
    except ValueError:
        pass
    try:
        i = sys.argv.index("-datafolder")
        datafolder = sys.argv[i + 1]
    except ValueError:
        datafolder = None
    try:
        i = sys.argv.index("-nogui")
        GUI = 0
    except ValueError:
        GUI = 1
    try:
        i = sys.argv.index("-remotehost")
        remote_host = sys.argv[i + 1]
    except ValueError:
        remote_host = None
        # remote_host = "10.30.1.7"  # bonsai NEW
        # remote_host = "10.30.1.2"  # bart OLD

    setup_server()

    # define folders for system
    azcam.db.systemname = "90prime"
    azcam.db.rootfolder = os.path.abspath(os.path.dirname(__file__))
    azcam.db.systemfolder = os.path.dirname(__file__)
    azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)
    azcam.db.datafolder = azcam.utils.get_datafolder(datafolder)

    # configuration menu
    menu_options = {
        "90prime (standard mode)": "normal",
        "90primeOne": "90primeone",
        "90prime with overscan rows": "overscan",
        "90prime FAST mode (with overscan rows)": "fast",
        "CSS mode": "css",
        "Archon controller with new mosaic": "archon",
    }
    if option == "menu":
        print("90Prime Startup Menu\n")
        option = azcam.utils.show_menu(menu_options)

    CSS = 0
    ARCHON = 0
    if "90primeone" in option:
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_one.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90primeone_master.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "dspcode_90prime",
            "dsptiming_90primeone",
            "90PrimeOne_config0.lod",
        )
        azcam.db.servermode = "90primeone"
        cmdport = 2432
        NUMCHANS = 4
    elif "normal" in option:
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_normal.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90prime_master.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "dspcode_90prime",
            "dsptiming_90prime",
            "90Prime_config0.lod",
        )
        azcam.db.servermode = "normal"
        cmdport = 2402
        NUMCHANS = 16
    elif "fast" in option:
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_fast.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90prime_master.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "dspcode_90prime",
            "dsptiming_fast",
            "90Prime_config1.lod",
        )
        azcam.db.servermode = "fast"
        cmdport = 2402
        NUMCHANS = 16
    elif "overscan" in option:
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_overscan.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90prime_master.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "dspcode_90prime",
            "dsptiming_90prime",
            "90Prime_config0.lod",
        )
        azcam.db.servermode = "overscan"
        cmdport = 2402
        NUMCHANS = 16
    elif "css" in option:
        CSS = 1
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_css.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90prime_css.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "dspcode_90prime",
            "dsptiming_90prime",
            "90Prime_config0.lod",
        )
        azcam.db.servermode = "CSS"
        cmdport = 2422
        NUMCHANS = 16
    elif "archon" in option:
        ARCHON = 1
        parfile = os.path.join(
            azcam.db.datafolder, "parameters", "parameters_server_90prime_archon.ini"
        )
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_90prime_archon.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "dspcode",
            "archon",
            "90prime_14feb25.acf",
        )
        azcam.db.servermode = "archon"
        cmdport = 2402
        NUMCHANS = 8
        if remote_host is None:
            remote_host = "10.30.1.7"
    else:
        raise azcam.exceptions.AzcamError("bad server configuration")

    # logging
    logfile = os.path.join(azcam.db.datafolder, "logs", "server.log")
    azcam.db.logger.start_logging(logfile=logfile)
    azcam.log(f"90prime mode: {option}")

    # controller
    DETNAME = "90prime"
    DEWNAME = "90prime"
    if ARCHON:
        from azcam.tools.archon.controller_archon import ControllerArchon
        from azcam.tools.archon.exposure_archon import ExposureArchon

        controller = ControllerArchon()
        controller.timing_file = timingfile
        controller.camserver.port = 4242
        controller.camserver.host = "10.30.3.6"  # archon at Bok
        controller.reset_flag = 1  # 0 for soft reset, 1 to upload code
        controller.verbosity = 1
        azcam.db.verbosity = 1
        DETNAME = "90prime2"
        DEWNAME = "90prime2"
    else:
        from azcam.tools.arc.controller_arc import ControllerArc
        from azcam.tools.arc.exposure_arc import ExposureArc

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

    # temperature controller
    if ARCHON:
        from azcam.tools.archon.tempcon_archon import TempConArchon

        tempcon = TempConArchon(description="90prime Archon")
        tempcon.temperature_ids = [0, 2]  # camtemp, dewtemp
        tempcon.heaterx_board = "MOD1"
        tempcon.control_temperature = -95.0
        controller.heater_board_installed = 1

    else:
        from azcam.tools.tempcon_cryocon24 import TempConCryoCon24

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

    # exposure
    if ARCHON:
        exposure = ExposureArchon()
        exposure.filetype = exposure.filetypes["MEF"]
        exposure.image.filetype = exposure.filetypes["MEF"]
        # exposure.update_headers_in_background = 1
        exposure.display_image = 0
        exposure.add_extensions = 1
        exposure.image.focalplane.gains = NUMCHANS * [2.4]
        exposure.image.focalplane.rdnoises = [
            6.6,
            6.7,
            7.9,
            11.4,
            6.7,
            6.7,
            6.5,
            6.3,
        ]
        exposure.shutter_delay = 250

    else:
        exposure = ExposureArc()
        exposure.filetype = exposure.filetypes["MEF"]
        exposure.image.filetype = exposure.filetypes["MEF"]
        exposure.update_headers_in_background = 1
        exposure.display_image = 0

        exposure.image.focalplane.gains = [
            1.5,
            1.7,
            1.4,
            1.6,
            1.6,
            1.6,
            1.5,
            1.5,
            1.3,
            1.4,
            1.4,
            1.5,
            1.6,
            1.4,
            1.4,
            1.5,
        ]
        exposure.image.focalplane.rdnoises = [
            6.6,
            6.7,
            6.9,
            6.3,
            7.8,
            8.2,
            6.7,
            6.9,
            9.9,
            6.3,
            8.0,
            8.6,
            9.5,
            6.0,
            6.1,
            6.8,
        ]

    if remote_host is None:
        exposure.send_image = 1
        exposure.sendimage.set_remote_imageserver("10.30.1.2", 6543, "dataserver")
    else:
        exposure.send_image = 1
        exposure.sendimage.set_remote_imageserver(remote_host, 6543, "dataserver")

    # instrument
    if ARCHON:
        instrument = PrimeFocusInstrumentUpgrade()
    else:
        instrument = PrimeFocusInstrument()

    if remote_host is not None:
        instrument.host = remote_host

    if 1:
        try:
            instrument.initialize()
        except Exception:
            azcam.log("Could not initialize 90prime instrument")

    # telescope
    telescope = BokTCS()
    try:
        telescope.initialize()
    except Exception:
        azcam.log("Could not initialize Bok testescope")

    # focus
    focus = Focus()
    focus.focus_component = "instrument"
    focus.focus_type = "step"
    focus.initialize()

    # system header template
    system = System("90prime", template)
    system.set_keyword("DETNAME", DETNAME, "Detector name")
    system.set_keyword("DEWAR", DEWNAME, "Dewar name")

    # detector
    if "90primeone" in option:
        from azcam_90prime.detector_bok90prime import detector_bok90prime_one

        exposure.set_detpars(detector_bok90prime_one)
        DETNAME = "90primeOne"

    elif "archon" in option:
        from azcam_90prime.detector_bok90prime import detector_bok90prime_archon

        exposure.set_detpars(detector_bok90prime_archon)
        exposure.fileconverter.set_detector_config(detector_bok90prime_archon)

    else:
        from azcam_90prime.detector_bok90prime import detector_bok90prime

        if "overscan" in option:
            detector_bok90prime["format"] = [4032 * 2, 6, 0, 20, 4096 * 2, 0, 0, 20, 0]
        exposure.set_detpars(detector_bok90prime)

    # display
    display = Ds9Display()
    display.initialize()

    # system-specific
    if CSS:
        from azcam_90prime.css import CSS

        css = CSS()
        azcam.db.tools["css"] = css
        exposure.send_image = 1
        if remote_host is None:
            exposure.sendimage.set_remote_imageserver("10.30.6.2", 6543, "azcam")
        else:
            exposure.sendimage.set_remote_imageserver(remote_host, 6543, "azcam")
        exposure.folder = "/home/css"

    # WCS
    sc = 0.000125
    exposure.image.focalplane.wcs.scale1 = NUMCHANS * [-1 * sc]
    exposure.image.focalplane.wcs.scale2 = NUMCHANS * [-1 * sc]
    exposure.image.focalplane.wcs.rot_deg = NUMCHANS * [90.0]

    # parameter file
    azcam.db.parameters.read_parfile(parfile)
    azcam.db.parameters.update_pars()

    # command server
    cmdserver = CommandServer()
    cmdserver.port = cmdport
    azcam.log(f"Starting cmdserver - listening on port {cmdserver.port}")
    azcam.db.api.initialize()
    cmdserver.start()

    # web server
    webserver = WebServer()
    webserver.port = cmdport + 1
    webserver.index = os.path.join(azcam.db.systemfolder, "index_90prime.html")
    webserver.start()

    # azcammonitor
    azcam.db.monitor.register()

    # controller server restart
    if not ARCHON:
        import azcam_90prime.restart_cameraserver

    # GUI
    if GUI:
        if os.name != "posix":
            import azcam_90prime.start_azcamtool

    # finish
    azcam.log("Configuration complete")


# start
setup()
from azcam.cli import *
