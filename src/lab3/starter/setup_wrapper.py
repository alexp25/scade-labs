# setup_wrapper.py
# Run this once to generate Python-callable wrappers for both operators.
#
# Install dependencies first:
#   pip install -r requirements.txt
#
# Then run:
#   py -3 setup_wrapper.py

from pathlib import Path
from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.svc.pywrapper.python_wrapper import PythonWrapper

SCADE_INSTALL = r"C:\Program Files\Ansys Inc\v261\Scade One Student\Scade One"
PROJECT_DIR   = Path(__file__).resolve().parent / "demo.sproj"

app = ScadeOne(install_dir=SCADE_INSTALL)
prj = app.load_project(PROJECT_DIR)
prj.load_jobs()

# Each operator gets its own output name to avoid overwriting each other.
# Generates: limiter_wrapper/limiter_wrapper.py  and  counter_wrapper/counter_wrapper.py
PythonWrapper(prj, "CodeGenerationJob_limiter",   output="limiter_wrapper").generate()
PythonWrapper(prj, "CodeGenerationJob_counter", output="counter_wrapper").generate()

print("Wrappers generated.")
print(f"  limiter → {Path.cwd() / 'limiter_wrapper' / 'limiter_wrapper.py'}")
# print(f"  counter → {Path.cwd() / 'counter_wrapper' / 'counter_wrapper.py'}")
