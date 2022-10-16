@echo off

call C:\azcam\venvs\azcam\Scripts\activate.bat

ipython --profile azcamconsole -i -m azcam_90prime.console -- %1 %2 %3 %4 %5 %6
