"""API for creation of Scade One Projects"""

import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Optional, Union, cast, overload
from warnings import warn

from ansys.scadeone.core.project import Project  # type: ignore
from ansys.scadeone.core import ScadeOne, swan  # type: ignore
from ansys.scadeone.core.interfaces import IScadeOne
from ansys.scadeone.core.common.storage import ProjectStorage
from ansys.scadeone.core.common.versioning import FormatVersions
from ansys.scadeone.core.svc.swan_creator.project_creator import ProjectCreator
from ansys.scadeone.core.swan import TestModule

from .s1_api_utils import get_valid_id

assert sys.version_info >= (3, 8), "Requires Python 3.8 or above"

PathStr = Union[Path, str]
PathOptionalContent = Union[PathStr, tuple[PathStr, str]]
PathContentDict = dict[Path, Optional[str]]

ResourcesDict = dict["ResourceKind", Union[list[PathStr], dict[str, PathStr]]]


class ResourceKind(Enum):
    """Kind of Project Resource"""

    SOURCE_FILE = "SourceFile"
    HEADER_FILE = "HeaderFile"
    SIMULATION_DATA = "SimulationData"

    def __str__(self) -> str:
        return self.value


class JsonClass:
    """Class that can be exported to JSON"""

    EXTENSION: ClassVar[str] = ".json"

    def to_dict(self) -> dict[str, Any]:
        """Transform into a dictionary for dumping to JSON"""

        def json_serializer(data: Any) -> Any:
            """JSON Serializer"""
            if isinstance(data, JsonClass):
                return data.to_dict()
            if isinstance(data, Path):
                return data.as_posix()
            if isinstance(data, ResourceKind):
                return data.value
            if isinstance(data, list):
                return [json_serializer(v) for v in data]

            return data

        return {k.title(): json_serializer(v) for k, v in self.__dict__.items()}

    @overload
    def to_json(self) -> str: ...

    @overload
    def to_json(self, path: None) -> str: ...

    @overload
    def to_json(self, path: PathStr) -> Path: ...

    def to_json(self, path: Optional[PathStr] = None) -> Union[str, Path]:
        """Dumps to JSON to a file if a path is specified, or string otherwise

        Note: if a path is provided without extension, a default extension is added
        """
        data = json.dumps(self.to_dict(), indent=2)
        if path is None:
            return data

        if not path:
            raise AttributeError("Cannot specify empty string for path")

        output = Path(path)
        if output.suffix == "":
            output = output.with_suffix(self.EXTENSION)
        output.write_text(data, encoding="utf-8")
        return output


@dataclass
class Resource(JsonClass):
    """Resource for project"""

    kind: ResourceKind
    path: PathStr
    key: str = ""

    def __post_init__(self):
        path = Path(self.path)
        resource_name = f"Resource {self.kind.value} '{self.path}'"
        if self.kind == ResourceKind.SIMULATION_DATA:
            if not self.key:
                raise AttributeError(f"{resource_name} shall have a key")
            if path.suffix != ".sd":
                raise AttributeError(f"{resource_name} shall be a .sd file")
        else:
            if self.key:
                warn(f"{resource_name} shall have no key")
            self.key = ""


class ProjectEnhanced(Project):
    """Swan Project with resources and dependencies"""

    def __init__(self, app: IScadeOne, project: ProjectStorage) -> None:
        super().__init__(app, project)
        self._imported_code: PathContentDict = {}

    @property
    def root_dir(self) -> Path:
        """Root directory of the project"""
        project_dir = self.directory
        assert project_dir is not None, "Project directory shall be set"

        return Path(project_dir)

    @property
    def assets_dir(self) -> Path:
        """Directory for assets"""
        return self.root_dir / "assets"

    @property
    def resources_dir(self) -> Path:
        """Directory for resources"""
        return self.root_dir / "resources"

    @property
    def jobs_dir(self) -> Path:
        """Directory for jobs"""
        return self.root_dir / "jobs"

    def get_rel_dir(self, path: PathStr) -> Path:
        """Remove root folder for the resources and dependencies"""
        try:
            return Path(path).absolute().relative_to(self.root_dir.absolute())
        except ValueError:
            return Path(path)

    @classmethod
    def from_project(cls, project: Project) -> "ProjectEnhanced":
        """Create enhanced project from a project"""
        enhanced_project = cls(project.app, project.storage)
        enhanced_project._dependencies = project._dependencies or []
        enhanced_project._jobs = project._jobs
        enhanced_project._data = project._data
        enhanced_project.is_new = project.is_new
        return enhanced_project

    def add_dependencies(self, dependencies: list[PathStr]) -> None:
        """Add dependencies for the project"""
        paths = [(p if p.is_absolute() else self.directory / p) for p in dependencies]
        missing_paths = [p for p in paths if not p.exists()]
        if missing_paths:
            warn(f"Missing dependencies: {missing_paths}")
        with ScadeOne() as app:
            self._dependencies += [app.load_project(p) for p in paths if p.exists()]

    def _get_resources_json(
        self,
        resources: list[PathStr],
        kind: ResourceKind,
    ) -> list[dict[str, str]]:
        """Generic method to get the resources as a JSON file"""
        return [Resource(kind, self.get_rel_dir(p)).to_dict() for p in resources]

    def add_imported_code(
        self,
        path: PathStr,
        content: str = "",
        append: bool = False,
    ):
        """Add (set or append) code to source file or header file"""
        path = Path(path)
        if append:
            if self._imported_code.get(path, None) is None:
                self._imported_code[path] = ""
            self._imported_code[path] += content  # type: ignore  # content is necessary a string
        else:
            self._imported_code[path] = content

    def _get_imported_kind(self, path: Path) -> ResourceKind:
        """Get the kind of resource from the path"""
        if path.suffix == ".h":
            return ResourceKind.HEADER_FILE
        return ResourceKind.SOURCE_FILE

    def build_sproj(self) -> None:
        Path(self._storage.path).parent.mkdir(parents=True, exist_ok=True)

        dependencies = [
            self.get_rel_dir(p.directory).as_posix() for p in self._dependencies
        ]
        resources = [
            Resource(self._get_imported_kind(p), self.get_rel_dir(p)).to_dict()
            for p in self._imported_code
        ]

        json_data = {
            "Version": FormatVersions.version("sproj"),
            "Name": self._storage.path.stem,
            "Dependencies": dependencies,
            "Resources": resources,
        }

        self._storage.set_content(json.dumps(json_data, indent=2))

        # Create imported files
        for resource, content in self._imported_code.items():
            if not content:
                continue
            self.resources_dir.mkdir(parents=True, exist_ok=True)
            path = self.resources_dir / resource
            path.write_text(content, encoding="utf-8")

        swan.LOGGER.info(f"Created: {self._storage.source}")

    def add_module_test(self, name: str) -> TestModule:
        """Add a test module to the model."""
        identifier = swan.PathIdentifier([get_valid_id(name)])
        module = TestModule(identifier)
        self.model.add_harness(module)
        ProjectCreator._set_module_source(cast("Project", self), module)
        return module
