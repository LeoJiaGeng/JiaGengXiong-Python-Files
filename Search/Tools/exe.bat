@echo off
mode con cols=50 lines=50

:: 需要编译的文件和执行编译的软件位置
set MAIN_PY_NAME=app.py
set SOFT_PATHS="D:\Document\Python_Files\Python_virtual\Scripts"

:: 设置文件夹
set PROJECT_NAME=%~dp0..
set PY_WORKPATH="%PROJECT_NAME%\Demo"
set PY_VERSION="%PY_WORKPATH%\%MAIN_PY_NAME%"
set RELEASE_PATHS="%PROJECT_NAME%\release"

:: 查看是否存在文件夹
cd %PY_WORKPATH%
if not exist %RELEASE_PATHS% (mkdir %RELEASE_PATHS%)

:: 激活虚拟环境
cd %SOFT_PATHS%
call activate.bat

::编译文件
cd %RELEASE_PATHS%
call pyinstaller.exe -Dw %PY_VERSION%

if %ERRORLEVEL% == 1 goto Failure
echo exe file has been converted 
exit

:Failure
@echo ERR
pause
exit
