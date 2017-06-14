@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
set path_var=%PATH%
set virt_env=%1

:: Check if Python exists in PATH
echo %path_var% | findstr /C:"Python" 1>nul

:: No argument provided - show file Usage
if [%1]==[] goto :usage


:: Python doesn't exist
if errorlevel 1 (
	echo Python not found in the system path
	echo 1. Run the Python Installation exe again
	echo 2. Click Modify
	echo 3. Click Next on Optional Features page
	echo 4. Tick 'Add Python to environment variables' and then click install
	echo Rerun this script after taking above action to verify installation
) ELSE  (

	for %%* in (.) do set cur_dir=%%~nx*

	echo %cur_dir%

	cd ..

	call python %cur_dir%\checkDevNet.py %virt_env%

	echo.
	echo Python script finished execution
	echo.

	:: Get current folder name
	for %%* in (.) do set work_dir=%%~nx*

	if "%work_dir%"=="%virt_env%" (
		@echo Activating Virtual Python Environment
		call "Scripts\activate"
	) else (
		@echo Activating Virtual Python Environment
		call "%virt_env%\Scripts\activate"
	)
)
goto :eof

:: Script usage displayed if no argument is supplied
:usage
@echo Usage: %0 ^<EnvironmentName^>
exit /B 1

:eof
exit /B 1