@echo off
cd %~dp0

:: Colors for console output
set GOLD=[33m
set GREEN=[92m
set MAGENTA=[95m
set RED=[91m
set EOL=[0m

:: Activate Virtual Environment if found
call :activate_venv .venv  || exit /b 1
call :activate_venv ..\.venv  || exit /b 1
call :activate_venv venv  || exit /b 1
call :activate_venv ..\venv  || exit /b 1

:set_env_and_run
:: Installing Dependencies
echo ...Installing Scade One API...
echo %MAGENTA%python -m pip install ..\s1_api\ansys_scadeone-0.7.0+56-py3-none-any.whl%EOL%
python -m pip install ..\s1_api\ansys_scadeone-0.7.0+56-py3-none-any.whl || goto :EXIT_WITH_ERROR
echo.
echo ...Installing Requirements for Keras Importer and App (this might take a while)...
echo %MAGENTA%python -m pip install -q -r requirements_app.txt%EOL%
python -m pip install -r requirements_app.txt || goto :EXIT_WITH_ERROR
echo.
echo ...Installing Swan Pygments Plugin...
echo %MAGENTA%python -m pip install ..\pygments_plugin\scade_one_pygments_plugin-1.0.0-py3-none-any.whl%EOL%
python -m pip install ..\pygments_plugin\scade_one_pygments_plugin-1.0.0-py3-none-any.whl || goto :EXIT_WITH_ERROR
echo.
echo %GREEN%Installed requirements for Keras Importer and App successfully%EOL%
echo.

:: Launching the App
echo ...Launching the app of %GOLD%Keras Importer%EOL%
echo %MAGENTA%python -m streamlit run app_keras_importer.py%EOL%
python -m streamlit run app_keras_importer.py || goto :EXIT_WITH_ERROR
@goto :EXIT

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
)
goto :eof
:: -------------------------------------------------

:: Exit normally
:EXIT
@echo off
echo.
echo %GREEN%... Exiting%EOL%
timeout /t 10
exit /b 0
goto :eof

::Exit with error
:EXIT_WITH_ERROR
@echo off
echo.
echo %RED%... Exiting with error...%EOL%
timeout /t 20
exit /b 1
goto :eof
