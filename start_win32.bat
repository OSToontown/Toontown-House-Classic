@echo off
title Toontown House: Classic CLI Launcher

:menu
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What do you want to do!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo #1 - Run Toontown House: Classic
echo #2 - Exit
echo. 
choice /C:123 /n /m "Selection: "%1
if errorlevel ==2 EXIT /B
if errorlevel ==1 goto run

:run
cls 
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Server!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
cd scripts
echo Launching the Blob Server...
START server_blob_win32.bat
echo Launching the Server...
START server_start_win32.bat
cd ..
goto game

:game
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Username [!] This does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set /P USER="Username: "
:start
"dependencies/panda/python/python" main.py -svaddr localhost -l en -u %USER% -d
pause
goto start