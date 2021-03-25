@echo off

REM  Copyright (c) 2018-2021, Carnegie Mellon University
REM  See LICENSE for details

set basepath=%~dp0

REM per-remote arguments for forwarder
set localargs=-H hostname -u username -p password

shift
python "%basepath%\..\forward.py" %* %localargs%
