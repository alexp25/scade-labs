@echo off
cd %~dp0

:: Colors for console output
set GOLD=[33m
set GREY=[90m
set GREEN=[92m
set MAGENTA=[95m
set RED=[91m
set EOL=[0m

:: Activate Virtual Environment if found
call :activate_venv .venv  || exit /b 1
call :activate_venv src\.venv  || exit /b 1
call :activate_venv venv  || exit /b 1
call :activate_venv src\venv  || exit /b 1

:set_env_and_run
:: Installing Depencies
echo ...Installing Scade One API...
echo %MAGENTA%python -m pip install ..\s1_api\ansys_scadeone_core-0.8.0-py3-none-any%EOL%
python -m pip install s1_api\ansys_scadeone_importers_nn-0.2.1-py3-none-any.whl || goto :EXIT_WITH_ERROR
echo.
echo ...Installing Requirements for Keras Importer (this might take a while)...
echo %MAGENTA%python -m pip install -r src\requirements.txt%EOL%
python -m pip install -r src\requirements.txt || goto :EXIT_WITH_ERROR
echo.
echo %GREEN%Installed requirements for Keras Importer successfully%EOL%
echo.

:: Launching the App
echo %GREEN%You can now run the %GOLD%Keras Importer%EOL%:
echo %GREY%python src\s1_keras_importer [path-model-h5] -o [output-dir]%EOL%
echo ... or the Lenet example:
echo %GREY%python src\example_import_lenet_to_s1%EOL%
echo ... or the Web-based User Interface:
echo %GREY%launch_app.bat%EOL% (in folder "src")
goto :EXIT

:: -------------------------------------------------
:: Function to Setup and enter Python venv
:activate_venv
set VENV=%1
if exist "%VENV%" (
    echo ...Activating Python Virtual Environment in %VENV%
    echo %MAGENTA%.\%VENV%\Scripts\activate.bat%EOL%
    call .\%VENV%\Scripts\activate.bat
    echo %GREEN%Entered Python virtual environment: %VENV%%EOL%
    echo.
    goto :set_env_and_run
    exit /b 0
)
goto :eof
:: -------------------------------------------------

:: Exit normally
:EXIT
echo.
echo %GREEN%... Exiting%EOL%
timeout /t 10
exit /b 0
goto :eof

::Exit with error
:EXIT_WITH_ERROR
echo.
echo %RED%... Exiting with error...%EOL%
timeout /t 20
exit /b 1
goto :eof
