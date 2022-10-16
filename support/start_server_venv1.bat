@echo off

call C:\azcam\venvs\azcam\Scripts\activate.bat

ipython --profile azcamserver -i -m azcam_90prime.server -- %1 %2 %3 %4 %5 %6
