@echo off

start/min "azcammonitor" python -m azcam_server.monitor.azcammonitor -configfile "/data/90prime/parameters/parameters_monitor_90prime.ini"
