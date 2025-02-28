# azcam-90prime

## Purpose

This repository contains the *azcam-90prime* azcam environment.  It includes code and data files for the University of Arizona Bok telescope 90prime facility camera system.

## Installation Notes

- Upgrade to required python version
- Download code (usually into the *azcam* root folder such as `c:\azcam`) and install:

```shell
git clone https://github.com/mplesser/azcam
git clone https://github.com/mplesser/azcam-console
git clone https://github.com/mplesser/azcam-90prime
git clone https://github.com/mplesser/azcam-expstatus
git clone https://github.com/mplesser/azcam-tool
pip install pickleshare  # for Ipython
pip install -e azcam
pip install -e azcam-console
pip install -e azcam-90prime
```

- Optionally
  - Install and start xpans and nssm
    - install script is in `/azcam/azcam/support/ds9`
  - Update .ipython_config files from `/azcam/azcam/support/ipython`

## System Setup Notes
- Do Windows updates
- Download and install VS Code
- install python to c:\python3x (e.g. c:\python311)
- install Labview 2014 runtime for azcam-tool
- install SAO ds9
- install and start xpans and nssm from azcam-ds9-winsupport
- winget install --id=Microsoft.PowerShell -e  # to update

### If PC is a controller server
- install ARC Win10 PCI card driver
- install and configure controller server
