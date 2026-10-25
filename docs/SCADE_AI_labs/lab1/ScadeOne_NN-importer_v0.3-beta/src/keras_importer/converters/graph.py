from datetime import datetime
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from shutil import copytree, rmtree
import shutil
from textwrap import dedent
from typing import Iterable, Optional, Union

from ansys.scadeone.core import ScadeOne, swan  # type: ignore

from keras import Model  # type: ignore

from ..graph.keras_graph import ModelParser
from ..utils.auto_layout import run_auto_layout
from ..utils.harness import add_test_harness
from ..utils.project import PathStr, ProjectEnhanced
from ..utils.s1_api_utils import get_valid_swan_name
from .operator import OperatorCreator, TestsInputsVar

LuidDict = dict[str, swan.Luid]
EdgeInfo = Iterable[tuple[str, str, Optional[int]]]


class ModelCreator(ModelParser):
    """Extension of Model Parser to convert nodes to Swan Operators / Project"""

    def __init__(
        self,
        model: Union[str, Path, Model],
        sproj_or_outdir: PathStr,
        keras_lib_path: PathStr,
        copy_keras_lib: bool = True,
        importer_version: Optional[str] = None,
        exists_ok: bool = False,
    ) -> None:
        """Create a Model Creator from a Keras Model

        Args:
            model: Keras Model or path to a Keras Model
            sproj_or_outdir: Path to the .sproj file or folder where the project will be created
            keras_lib_path: Path to the Keras Library implemented in Scade One
            copy_keras_lib: Copy the Keras Library to the project (default: True)
            importer_version: Version of the importer (default: None)
            exists_ok: If the project exists, delete it (default: False)

        """
        super().__init__(model)

        self.module_name = get_valid_swan_name(self.model.name)

        # We need to ensure that sproj is a file and not a folder
        self.sproj = Path(sproj_or_outdir)
        if self.sproj.suffix != ".sproj":
            # Project name matches the output directory name
            self.sproj = self.sproj / f"{self.sproj.name}.sproj"

        if self.sproj.exists() and exists_ok:
            shutil.rmtree(self.sproj.parent)

        with ScadeOne() as app:
            project = app.new_project(self.sproj)
            self.project = ProjectEnhanced.from_project(project)

        self.module_interface = self.project.add_module_interface(self.module_name)
        self.module_body = self.project.add_module(self.module_name)
        self.module_body.use("keras::layers")
        self.module_body.use("keras::activations")

        self.module_test = self.project.add_module_test(f"test_{self.module_name}")
        self.module_test.use(self.module_name)

        self.constants_source_file = self.project.resources_dir / "constants.c"
        self.project.add_imported_code(self.constants_source_file)

        self.keras_lib_sproj_path: Path = Path("DUMMY:/")
        self.set_keras_lib(keras_lib_path=keras_lib_path, copy_keras_lib=copy_keras_lib)
        self.importer_version = importer_version

        self.creator = OperatorCreator(name=self.module_name, module=self.module_body)

    def set_keras_lib(self, keras_lib_path: PathStr, copy_keras_lib: bool):
        if not keras_lib_path:
            raise AttributeError("Path of Keras Lib not provided")

        keras_lib_path = Path(keras_lib_path)
        if not keras_lib_path.exists():
            raise FileNotFoundError(f"Keras library not found in '{keras_lib_path}'")
        if keras_lib_path.is_dir():
            keras_lib_dir = keras_lib_path
            try:
                keras_lib_proj = next(keras_lib_dir.glob("*.sproj"))
            except StopIteration as exc:
                raise FileNotFoundError(
                    f"No .sproj files found for keras library folder {keras_lib_dir}"
                ) from exc
        elif keras_lib_path.suffix == ".sproj":
            keras_lib_dir = keras_lib_path.parent
            keras_lib_proj = keras_lib_path
        else:
            raise AttributeError(
                f"Path of Keras library shall be either a folder or a .sproj"
                f", but is '{keras_lib_path}'"
            )
        self.keras_lib_original = keras_lib_dir
        if copy_keras_lib:
            self.keras_lib_project = self.project.root_dir / "keras_lib"
        else:
            # If we don't copy the keras lib, we need to either provide a path
            # relative to project folder or absolute because it is used in dependencies
            self.keras_lib_project = keras_lib_dir.absolute()
            # ... BEFORE: self.keras_lib_project = Path("..") / keras_lib_dir

        # We can store the dependencies in the project
        self.keras_lib_sproj_path = self.keras_lib_project / keras_lib_proj.name

    def add_content_to_cst_source_file(self, content: str, append: bool = True):
        """Set or append content to the source file for constants"""
        self.project.add_imported_code(self.constants_source_file, content, append=append)

    def create_module(self) -> None:
        """Populate module body and module interface"""
        # Main Operator
        for _, data in self.graph.nodes(data=True):
            node = data["data"]
            self.creator.node2diagram(node)

        edges_with_adapt: EdgeInfo = self.graph.edges(data="target_idx")  # type: ignore
        edges_by_source: dict[str, dict[str, Optional[int]]] = {
            k: {e[1]: e[2] for e in v}
            for k, v in groupby(edges_with_adapt, itemgetter(0))
        }
        for src, dest in edges_by_source.items():
            self.creator.edges2wire(src, dest)

        seq_signature = self.module_interface.add_signature(
            self.creator.operator.id.value,
            self.creator.operator.is_node,
        )
        seq_signature._inputs = self.creator.operator.inputs
        seq_signature._outputs = self.creator.operator.outputs

        # Constants
        if self.creator.constants:
            version = self.importer_version or "<unknown version>"
            cst_source_header = dedent(
                f"""\
                /* Generated by Scade One Keras Importer - Version {version} */
                /* Generation date: {datetime.now().ctime()} */

                #include "swan_types.h"
                #include "swan_consts.h"

                """
            )
            self.add_content_to_cst_source_file(cst_source_header)

        for constant in self.creator.constants:
            self.add_content_to_cst_source_file(
                constant.get_c_code(module=self.module_name), append=True
            )

    def create_test_harness(self, inputs_var: TestsInputsVar = None) -> None:
        """Create a test harness for the module"""
        if any("softmax" in o.lower() for o in self.outputs):
            self.module_test.use("keras::utils")

        harness = add_test_harness(self.module_test, "test")
        self.creator.create_test_harness_body(
            harness,
            self.module_name,
            inputs=[i.shape for i in self.inputs.values()],
            outputs=list(self.outputs.values()),
            inputs_var=inputs_var,
        )

        # Test Harness

    def write(self, auto_layout: Union[PathStr, bool] = True) -> Path:
        """Create a folder with the project and return the path

        Args:
            auto_layout: apply the auto-layout if not set to False. the argument could be:
                * a path (either as a string or a pathlib.Path)
                * True to apply auto-layout with default path of auto-layout executable
                * False to skip auto-layout
        """
        # We need to add
        if self.keras_lib_project.absolute() != self.keras_lib_original.absolute():
            if self.keras_lib_project.is_dir():
                rmtree(self.keras_lib_project)
            copytree(self.keras_lib_original, self.keras_lib_project)
            print(
                f'Copied Keras Library from "{self.keras_lib_original}"'
                f" to {self.keras_lib_project}"
            )
        self.project.add_dependencies([self.keras_lib_sproj_path])

        self.project.save()
        print(f"Generated S1 Project for '{self.model.name}' in {self.project.root_dir}!")

        if auto_layout:
            auto_layout_exe = auto_layout if isinstance(auto_layout, str) else None
            project = self.sproj
            try:
                _ = run_auto_layout(
                    project, auto_layout_exe=auto_layout_exe, capture_output=True
                )
                print(f"Successfully applied auto-layout to {project}")
            except Exception as e:
                print(f"Skipped auto-layout on {project}: {e}")
                # TODO: print error recorded when running auto-layout

        return self.project.root_dir
