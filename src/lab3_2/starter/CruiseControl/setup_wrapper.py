from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.svc.pywrapper.python_wrapper import PythonWrapper

SCADE_INSTALL = r"C:\Program Files\Ansys Inc\v261\Scade One Student\Scade One"  # adjust to your install
PROJECT_DIR   = r"CruiseControl.sproj"       # path to your .sproj file

app = ScadeOne(install_dir=SCADE_INSTALL)
prj = app.load_project(PROJECT_DIR)
prj.load_jobs()

# PythonWrapper takes the job name as a string, not a job object
PythonWrapper(prj, "CodeGenerationJob_CC").generate()

print("Wrapper generated.")