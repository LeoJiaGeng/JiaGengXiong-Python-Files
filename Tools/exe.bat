@echo off
mode con cols=50 lines=50

set MAIN_PY_NAME=appMain.py
set PROJECT_NAME=%~dp0..\Demo
set PY_WORKPATH="%PROJECT_NAME%"

echo %PY_WORKPATH%
pause
call pyinstaller.exe -w %PY_WORKPATH%\%MAIN_PY_NAME%
pause
if %ERRORLEVEL% == 1 goto Failure
echo exe file has been converted 

exit

:Failure
@echo ERR
pause
exit
