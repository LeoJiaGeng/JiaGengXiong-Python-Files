@echo off
mode con cols=50 lines=50

set UI_PY_NAME=ui_Search.py
set ICO_PY_NAME=ico_rc.py
set PROJECT_NAME=%~dp0..\Demo
set UI_WORKPATH="%PROJECT_NAME%"
set ICO_WORKPATH=%~dp0..\Resource

::echo %UI_WORKPATH%
dir /b %UI_WORKPATH%\*.ui>temp.txt
set /p UI_NAME=<temp.txt & del temp.txt

call pyuic5.exe -o %UI_WORKPATH%\%UI_PY_NAME% %UI_WORKPATH%\%UI_NAME%
if %ERRORLEVEL% == 1 goto MultiFiles
echo ui file has been converted 

::echo %ICO_WORKPATH%
dir /b %ICO_WORKPATH%\*.qrc>temp.txt
set /p ICO_NAME=<temp.txt & del temp.txt

call pyrcc5.exe -o %UI_WORKPATH%\%ICO_PY_NAME% %ICO_WORKPATH%\%ICO_NAME%

if %ERRORLEVEL% == 1 goto MultiFiles
echo qrc file has been converted 

exit

:MultiFiles
@echo ERR
pause
exit
