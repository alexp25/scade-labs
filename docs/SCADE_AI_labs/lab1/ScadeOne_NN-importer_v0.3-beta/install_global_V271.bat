@echo off
setlocal EnableExtensions
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
set "SCADE_ONE_INSTALL=C:\Program Files\ANSYS Inc\v271\Scade One"

echo.
echo %GOLD%===============================================================================%EOL%
echo %GOLD%SCADE ONE KERAS IMPORTER - COMPLETE INSTALLATION%EOL%
echo %GOLD%===============================================================================%EOL%
echo Project folder: %CD%
echo.
echo This installer installs Python 3.12 when it is missing, then installs all
echo required packages for the current Windows user.
echo It does not remove or modify the Python bundled with SCADE One.
echo.

:: Optional clean reinstall of standalone Python 3.12.
:: Run "install_global.bat --reset-python" from a terminal to enable it.
if /I "%~1"=="--reset-python" goto :RESET_PYTHON

goto :ENSURE_PYTHON

:RESET_PYTHON
echo %GOLD%Clean reinstall requested for standalone Python 3.12.%EOL%
where winget >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: WinGet is required for --reset-python but was not found.%EOL%
    goto :EXIT_WITH_ERROR
)

echo.
echo ...Removing WinGet-managed standalone Python 3.12, if present...
winget uninstall --id "%PYTHON_PACKAGE%" -e --scope user --silent --accept-source-agreements >nul 2>&1
if errorlevel 1 echo %GREY%No WinGet-managed user installation of Python 3.12 was removed.%EOL%

:: Remove only stale per-user Python 3.12 package data.
:: Product-bundled Python installations, including SCADE One pytools, are untouched.
if exist "%APPDATA%\Python\Python312" (
    echo ...Removing stale Python 3.12 user packages...
    rmdir /s /q "%APPDATA%\Python\Python312"
)

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

:: Use the standard per-user path immediately, without requiring a new terminal.
for /f "delims=" %%I in ('dir /b /s "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" 2^>nul') do if not defined PYTHON_EXE set "PYTHON_EXE=%%I"

if defined PYTHON_EXE set "PYTHON_CMD="%PYTHON_EXE%""
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
echo ...Checking required project and product files...
if not exist "s1_api\ansys_scadeone_importers_nn-0.2.1-py3-none-any.whl" (
    echo %RED%ERROR: Importer wheel not found:%EOL%
    echo s1_api\ansys_scadeone_importers_nn-0.2.1-py3-none-any.whl
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
    echo %RED%ERROR: Keras SWAN library folder not found: keras%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "%SCADE_ONE_INSTALL%\tools\swan_cg.exe" (
    echo %RED%ERROR: SCADE One v271 code generator not found:%EOL%
    echo %SCADE_ONE_INSTALL%\tools\swan_cg.exe
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
%PYTHON_CMD% -c "import sys, inspect, importlib.metadata as md; from ansys.scadeone.core import swan, ScadeOne; from ansys.scadeone.core.job import CodeGenerationJob; from ansys.scadeone.importers.nn import ModelCreator; import keras, numpy, networkx, streamlit; assert sys.version_info[:2] == (3, 12); assert md.version('ansys-scadeone-importers-nn') == '0.2.1'; assert hasattr(swan, 'NamedInstance'), 'NamedInstance is missing'; assert hasattr(CodeGenerationJob, 'save'), 'CodeGenerationJob.save is missing'; print('Python:', sys.executable); print('Importer:', md.version('ansys-scadeone-importers-nn')); print('Core:', md.version('ansys-scadeone-core')); print('NamedInstance: OK'); print('ModelCreator:', inspect.getfile(ModelCreator)); print('CodeGenerationJob:', inspect.signature(CodeGenerationJob)); print('CodeGenerationJob.save:', inspect.signature(CodeGenerationJob.save)); print('Keras:', keras.__version__); print('Streamlit:', streamlit.__version__)" || goto :EXIT_WITH_ERROR

echo.
echo %GREEN%Installation and verification completed successfully.%EOL%
echo.
echo Python interpreter to select in Visual Studio Code:
echo %GOLD%%PYTHON_EXE%%EOL%
echo.
echo %GREEN%You can now run Steps 1 to 7 and open_importer.bat.%EOL%
goto :EXIT

:EXIT
echo.
echo %GREEN%... Exiting successfully%EOL%
pause
exit /b 0

:EXIT_WITH_ERROR
echo.
echo %RED%... Installation failed.%EOL%
echo Review the error above. SCADE One bundled Python was not modified.
pause
exit /b 1
