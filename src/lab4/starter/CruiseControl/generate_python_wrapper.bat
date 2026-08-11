@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

py -3 -m ansys.scadeone.core.cli pycodewrap ^
  --install-dir "C:\Program Files\Ansys Inc\v261\Scade One Student\Scade One" ^
  --job "CodeGenerationJob_CC" ^
  --out "cc_wrapper" ^
  "%SCRIPT_DIR%CruiseControl.sproj"