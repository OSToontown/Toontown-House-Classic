@echo off
:start
cd "../dependencies/server" 
"../panda/python/python" "NetworkedBlobServer_WIN.py"
pause
goto start