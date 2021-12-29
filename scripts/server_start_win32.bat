@echo off
cd ".."
:start
"dependencies/panda/python/python" -m dependencies.server.server -lc
pause
goto start