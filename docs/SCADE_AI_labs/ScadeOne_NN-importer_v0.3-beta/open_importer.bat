@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title SCADE One Keras Importer

:: Colors for console output
set "GOLD=[33m"
set "GREY=[90m"
set "GREEN=[92m"
set "MAGENTA=[95m"
set "RED=[91m"
set "EOL=[0m"

:: Reduce TensorFlow startup messages and disable oneDNN custom operations.
set "TF_CPP_MIN_LOG_LEVEL=2"
set "TF_ENABLE_ONEDNN_OPTS=0"

set "PYTHON_CMD="
set "PYTHON_EXE="

py -3.12 -c "import sys; print(sys.executable)" >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3.12"

if not defined PYTHON_CMD (
    python -c "import sys; assert sys.version_info[:2] == (3, 12); print(sys.executable)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo %RED%ERROR: Python 3.12 was not found.%EOL%
    echo Install Python 3.12 and run install_global.bat.
    goto :EXIT_WITH_ERROR
)

for /f "delims=" %%I in ('%PYTHON_CMD% -c "import sys; print(sys.executable)"') do set "PYTHON_EXE=%%I"

if not exist "src\app_keras_importer.py" (
    echo %RED%ERROR: src\app_keras_importer.py not found.%EOL%
    goto :EXIT_WITH_ERROR
)
if not exist "keras" (
    echo %RED%ERROR: Keras SWAN library folder not found: keras%EOL%
    goto :EXIT_WITH_ERROR
)

echo.
echo %GOLD%===============================================================================%EOL%
echo %GOLD%SCADE ONE KERAS IMPORTER - WEB APPLICATION%EOL%
echo %GOLD%===============================================================================%EOL%
echo Python: %PYTHON_EXE%
echo Project folder: %CD%
echo.

echo ...Checking the Python 3.12 environment...
%PYTHON_CMD% -c "import inspect, importlib.metadata as md; from ansys.scadeone.core import swan; from ansys.scadeone.core.job import CodeGenerationJob; from ansys.scadeone.importers.nn import ModelCreator; import streamlit; assert md.version('ansys-scadeone-importers-nn') == '0.2.1'; assert hasattr(swan, 'NamedInstance'), 'NamedInstance is missing'; assert hasattr(CodeGenerationJob, 'save'), 'CodeGenerationJob.save is missing'; print('Importer:', md.version('ansys-scadeone-importers-nn')); print('NamedInstance: OK'); print('CodeGenerationJob.save: OK'); print('ModelCreator:', inspect.getfile(ModelCreator)); print('Streamlit:', streamlit.__version__)" || goto :NOT_INSTALLED

echo.
echo %GREEN%Launching the Keras Importer...%EOL%
echo %GREY%%PYTHON_CMD% -m streamlit run src\app_keras_importer.py%EOL%
echo.
%PYTHON_CMD% -u -m streamlit run "src\app_keras_importer.py"
if errorlevel 1 goto :EXIT_WITH_ERROR

goto :EXIT

:NOT_INSTALLED
echo.
echo %RED%ERROR: The required Python packages are missing or incompatible.%EOL%
echo Run install_global.bat first.
goto :EXIT_WITH_ERROR

:EXIT
echo.
echo %GREEN%Keras Importer closed.%EOL%
pause
exit /b 0

:EXIT_WITH_ERROR
echo.
echo %RED%The Keras Importer could not be started.%EOL%
pause
exit /b 1
