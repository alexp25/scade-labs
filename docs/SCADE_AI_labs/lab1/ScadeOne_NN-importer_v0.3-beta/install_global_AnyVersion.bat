@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title SCADE One Keras Importer - Complete Installation

:: Colors for console output
set "GOLD=[33m"
set "GREY=[90m"
set "GREEN=[92m"
set "MAGENTA=[95m"
set "RED=[91m"
set "EOL=[0m"

set "PYTHON_PACKAGE=Python.Python.3.12"
set "PYTHON_CMD="
set "PYTHON_EXE="
set "DETECTED_SCADE_ONE="
set "DETECTED_VERSION="
set "DETECTED_EDITION="

echo.
echo %GOLD%===============================================================================%EOL%
echo %GOLD%SCADE ONE KERAS IMPORTER - COMPLETE INSTALLATION%EOL%
echo %GOLD%===============================================================================%EOL%
echo Project folder: %CD%
echo.
echo This installer detects SCADE One or SCADE One Student automatically,
echo installs Python 3.12 when needed, and installs the importer for the current user.
echo.

:: -------------------------------------------------------------------------------
:: Detect SCADE One installation
::
:: Supported layouts:
::
:: Commercial:
:: C:\Program Files\ANSYS Inc\vXXX\Scade One\tools\swan_cg.exe
::
:: Student:
:: C:\Program Files\ANSYS Inc\vXXX\Scade One Student\Scade One\tools\swan_cg.exe
::
:: Selection priority:
:: 1. Valid SCADE_ONE_INSTALL environment variable
:: 2. Newest commercial installation
:: 3. Newest Student installation
:: -------------------------------------------------------------------------------

echo ...Searching for SCADE One installations...

:: Use an existing valid environment variable first.
if defined SCADE_ONE_INSTALL (
    if exist "%SCADE_ONE_INSTALL%\tools\swan_cg.exe" (
        set "DETECTED_SCADE_ONE=%SCADE_ONE_INSTALL%"
        set "DETECTED_VERSION=Environment variable"
        set "DETECTED_EDITION=Configured"
        goto :SCADE_FOUND
    )
)

:: First pass: search commercial installations from newest to oldest.
for /f "delims=" %%V in ('dir /b /ad /o:-n "%ProgramFiles%\ANSYS Inc\v*" 2^>nul') do (
    if not defined DETECTED_SCADE_ONE (
        if exist "%ProgramFiles%\ANSYS Inc\%%V\Scade One\tools\swan_cg.exe" (
            set "DETECTED_SCADE_ONE=%ProgramFiles%\ANSYS Inc\%%V\Scade One"
            set "DETECTED_VERSION=%%V"
            set "DETECTED_EDITION=Commercial"
        )
    )
)

:: Second pass: search Student installations from newest to oldest.
if not defined DETECTED_SCADE_ONE (
    for /f "delims=" %%V in ('dir /b /ad /o:-n "%ProgramFiles%\ANSYS Inc\v*" 2^>nul') do (
        if not defined DETECTED_SCADE_ONE (
            if exist "%ProgramFiles%\ANSYS Inc\%%V\Scade One Student\Scade One\tools\swan_cg.exe" (
                set "DETECTED_SCADE_ONE=%ProgramFiles%\ANSYS Inc\%%V\Scade One Student\Scade One"
                set "DETECTED_VERSION=%%V"
                set "DETECTED_EDITION=Student"
            )
        )
    )
)

if not defined DETECTED_SCADE_ONE (
    echo.
    echo %RED%ERROR: No compatible SCADE One installation was found.%EOL%
    echo.
    echo Checked these installation layouts:
    echo.
    echo Commercial:
    echo   %ProgramFiles%\ANSYS Inc\vXXX\Scade One\tools\swan_cg.exe
    echo.
    echo Student:
    echo   %ProgramFiles%\ANSYS Inc\vXXX\Scade One Student\Scade One\tools\swan_cg.exe
    echo.
    echo If SCADE One is installed in another location, define SCADE_ONE_INSTALL
    echo with the folder that directly contains the tools folder.
    goto :EXIT_WITH_ERROR
)

:SCADE_FOUND
set "SCADE_ONE_INSTALL=%DETECTED_SCADE_ONE%"

echo.
echo %GREEN%SCADE One installation found.%EOL%
echo Version: %DETECTED_VERSION%
echo Edition: %DETECTED_EDITION%
echo Path: %SCADE_ONE_INSTALL%
echo Code generator: %SCADE_ONE_INSTALL%\tools\swan_cg.exe

:: Verify the selected installation one final time.
if not exist "%SCADE_ONE_INSTALL%\tools\swan_cg.exe" (
    echo.
    echo %RED%ERROR: SCADE One code generator not found:%EOL%
    echo %SCADE_ONE_INSTALL%\tools\swan_cg.exe
    goto :EXIT_WITH_ERROR
)

:: Store the detected path for future terminals and Python scripts.
setx SCADE_ONE_INSTALL "%SCADE_ONE_INSTALL%" >nul

if errorlevel 1 (
    echo %RED%ERROR: Could not save the SCADE_ONE_INSTALL environment variable.%EOL%
    goto :EXIT_WITH_ERROR
)

:: Optional clean reinstall of standalone Python 3.12.
:: Run "install_global_any_scade_version.bat --reset-python" to enable it.
if /I "%~1"=="--reset-python" goto :RESET_PYTHON
goto :ENSURE_PYTHON

:RESET_PYTHON
echo.
echo %GOLD%Clean reinstall requested for standalone Python 3.12.%EOL%
where winget >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: WinGet is required for --reset-python but was not found.%EOL%
    goto :EXIT_WITH_ERROR
)
winget uninstall --id "%PYTHON_PACKAGE%" -e --scope user --silent --accept-source-agreements >nul 2>&1
if errorlevel 1 echo %GREY%No WinGet-managed user installation of Python 3.12 was removed.%EOL%
if exist "%APPDATA%\Python\Python312" rmdir /s /q "%APPDATA%\Python\Python312"
set "PYTHON_CMD="
set "PYTHON_EXE="
goto :INSTALL_PYTHON

:ENSURE_PYTHON
py -3.12 -c "import sys; print(sys.executable)" >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3.12"
if not defined PYTHON_CMD (
    python -c "import sys; assert sys.version_info[:2] == (3, 12); print(sys.executable)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)
if defined PYTHON_CMD goto :PYTHON_READY

:INSTALL_PYTHON
echo.
echo ...Python 3.12 was not found. Installing it with WinGet...
where winget >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: WinGet was not found.%EOL%
    echo Install Microsoft App Installer, then run this file again.
    goto :EXIT_WITH_ERROR
)
winget install --id "%PYTHON_PACKAGE%" -e --scope user --silent --accept-package-agreements --accept-source-agreements
if errorlevel 1 goto :EXIT_WITH_ERROR
for /f "delims=" %%I in ('dir /b /s "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" 2^>nul') do if not defined PYTHON_EXE set "PYTHON_EXE=%%I"
if defined PYTHON_EXE set PYTHON_CMD="%PYTHON_EXE%"
if not defined PYTHON_CMD (
    py -3.12 -c "import sys; print(sys.executable)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3.12"
)
if not defined PYTHON_CMD (
    echo %RED%ERROR: Python 3.12 installation completed, but python.exe was not found.%EOL%
    goto :EXIT_WITH_ERROR
)

:PYTHON_READY
if not defined PYTHON_EXE for /f "delims=" %%I in ('%PYTHON_CMD% -c "import sys; print(sys.executable)"') do set "PYTHON_EXE=%%I"
echo.
echo Python selected: %PYTHON_EXE%
%PYTHON_CMD% --version || goto :EXIT_WITH_ERROR

echo.
echo ...Checking required project files...
if not exist "s1_api\ansys_scadeone_importers_nn-0.2.1-py3-none-any.whl" (
    echo %RED%ERROR: Importer wheel not found.%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "src\requirements.txt" (
    echo %RED%ERROR: src\requirements.txt not found.%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "src\requirements_app.txt" (
    echo %RED%ERROR: src\requirements_app.txt not found.%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "src\app_keras_importer.py" (
    echo %RED%ERROR: src\app_keras_importer.py not found.%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "keras" (
    echo %RED%ERROR: Keras SWAN library folder not found.%EOL%
    goto :EXIT_WITH_ERROR
)
echo %GREEN%Required files found.%EOL%

echo.
echo ...Updating pip...
%PYTHON_CMD% -m ensurepip --upgrade || goto :EXIT_WITH_ERROR
%PYTHON_CMD% -m pip install --user --upgrade pip || goto :EXIT_WITH_ERROR

echo.
echo ...Installing Keras Importer requirements...
%PYTHON_CMD% -m pip install --user -r "src\requirements.txt" || goto :EXIT_WITH_ERROR

echo.
echo ...Installing Web application requirements...
%PYTHON_CMD% -m pip install --user -r "src\requirements_app.txt" || goto :EXIT_WITH_ERROR

echo.
echo ...Installing ansys-scadeone-importers-nn 0.2.1 and compatible dependencies...
%PYTHON_CMD% -m pip install --user --force-reinstall "s1_api\ansys_scadeone_importers_nn-0.2.1-py3-none-any.whl" || goto :EXIT_WITH_ERROR

echo.
echo ...Installing the optional SWAN syntax-highlighting plugin...
if exist "pygments_plugin\pyproject.toml" (
    %PYTHON_CMD% -m pip install --user "pygments_plugin" || goto :EXIT_WITH_ERROR
) else if exist "pygments_plugin\setup.py" (
    %PYTHON_CMD% -m pip install --user "pygments_plugin" || goto :EXIT_WITH_ERROR
) else (
    echo %GREY%Optional pygments_plugin package not found. Continuing without it.%EOL%
)

echo.
echo ...Verifying the complete Python 3.12 environment...
%PYTHON_CMD% -c "import sys, inspect, importlib.metadata as md; from ansys.scadeone.core import swan, ScadeOne; from ansys.scadeone.core.job import CodeGenerationJob; from ansys.scadeone.importers.nn import ModelCreator; import keras, numpy, networkx, streamlit; assert sys.version_info[:2] == (3, 12); assert md.version('ansys-scadeone-importers-nn') == '0.2.1'; assert hasattr(swan, 'NamedInstance'), 'NamedInstance is missing'; assert hasattr(CodeGenerationJob, 'save'), 'CodeGenerationJob.save is missing'; print('Python:', sys.executable); print('Importer:', md.version('ansys-scadeone-importers-nn')); print('Core:', md.version('ansys-scadeone-core')); print('NamedInstance: OK'); print('ModelCreator:', inspect.getfile(ModelCreator)); print('CodeGenerationJob.save:', inspect.signature(CodeGenerationJob.save)); print('Keras:', keras.__version__); print('Streamlit:', streamlit.__version__)" || goto :EXIT_WITH_ERROR

echo.
echo %GREEN%Installation and verification completed successfully.%EOL%
echo.
echo Python interpreter to select in Visual Studio Code:
echo %GOLD%%PYTHON_EXE%%EOL%
echo.
echo SCADE One installation selected:
echo %GOLD%%SCADE_ONE_INSTALL%%EOL%
echo.
echo Open a new terminal or restart Visual Studio Code before running scripts that
echo read the persistent SCADE_ONE_INSTALL environment variable.
goto :EXIT

:EXIT
echo.
echo %GREEN%... Exiting successfully%EOL%
pause
exit /b 0

:EXIT_WITH_ERROR
echo.
echo %RED%... Installation failed.%EOL%
echo Review the error above. SCADE One product files were not modified.
pause
exit /b 1
