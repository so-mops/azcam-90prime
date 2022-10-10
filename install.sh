#! /bin/bash

# Linux install script for azcam
# Usage:
# mkdir azcam ; cd azcam
# git clone https://github.com/mplesser/azcam-90prime
# source ~/azcam/azcam-90prime/install.sh


# export AZCAM_DATAROOT="~/data"
sudo apt-get install python3-tk

source ~/azcam/venvs/azcam/bin/activate

cd ~/azcam
pip install -e azcam-90prime


# ~>source azcam/venvs/azcam/bin/activate
# ipython --profile azcamserver
# import azcam_90prime.server
# from azcam.cli import *
