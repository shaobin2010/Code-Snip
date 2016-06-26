@echo off
cd %~dp0

set pydir=C:\Python35
set pyscript=%pydir%\Scripts
set pyenv=%pyscript%\virtualenv.exe
set pypip=%pyscript%\pip.exe  

rem check if the virtualenv is installed or not
%pyenv% --version
rem echo %errorlevel%
if errorlevel 0 goto normal
	goto install_virtual_env

:install_virtual_env
echo "Install virtualenv"
%pypip% install virtualenv

:normal
rem Create venv
%pyenv% venv

rem Enter the virual environment
echo "Enter virtualenv"
call venv\Scripts\activate.bat

rem Install the dependecy library
echo "Install third library"
pip.exe install -r requirements.txt

rem Enter the virual environment
echo "Exit virtualenv"
call venv\Scripts\deactivate.bat


rem  ///////////////////////////////////////////////////////////////////////////////////////////////////
rem  pip.exe freeze > requirements.txt     // Export all the third party library to requirements.txt
rem  pip.exe install -r requirements.txt   // Install all the third party library from requirements.txt
rem  //////////////////////////////////////////////////////////////////////////////////////////////////