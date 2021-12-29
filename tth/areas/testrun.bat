@echo off
cls
:input
set INPUT=
set /P INPUT=Type input: %=%
python %INPUT%
goto input