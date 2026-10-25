from functools import wraps
from typing import Callable
import ansys.scadeone.core.svc.common.renderer as R
from ansys.scadeone.core import swan  # type: ignore
from ansys.scadeone.core.common.versioning import gen_swan_version
from ansys.scadeone.core.svc.swan_printer import PPrinter
from ansys.scadeone.core.svc.swan_visitor import Owner, OwnerProperty

from .s1_api_utils import get_valid_id


class PPrinterTestHarness(PPrinter):
    """Addition of Test Harness in the PPrinter class."""
    def visit_TestModule(
        self,
        swan_obj: swan.TestModule,
        owner: Owner,
        owner_property: OwnerProperty,
    ) -> None:
        """
        Test Module visitor

        Parameters
        ----------
        swan_obj : S.TestModule
            Visited Swan object, it's a Module instance
        owner : Owner
            Owner of the swan_obj, 'None' for the root visited object
        owner_property : OwnerProperty
            Owner property name to know the visit context, 'None' for the root visited object
        """

        # Init data buffer
        swan_obj.pprint_array = {"use_directives": [], "declarations": None}
        # Visit properties
        _decl = R.DBlock()
        _decl << R.DText(gen_swan_version(is_harness=True)) << "@n"  # Only difference is here
        if swan_obj.use_directives:
            for item in swan_obj.use_directives:
                self._visit(item, swan_obj, "use_directives")

            if swan_obj.pprint_array["use_directives"]:
                _decl << R.doc_list(
                    *swan_obj.pprint_array["use_directives"], sep=R.DLineBreak(False)
                )
                _decl << R.DLineBreak(False)
        if swan_obj.declarations:
            _dcl = []
            for item in swan_obj.declarations:
                self._visit(item, swan_obj, "declarations")
                _dcl.append(swan_obj.pprint_array["declarations"])
            if _dcl:
                _decl << R.doc_list(*_dcl, sep=R.DLineBreak(False))
        # Update property
        PPrinter._update_property(owner, owner_property, _decl)
        # Delete data buffer
        if isinstance(owner, PPrinter):
            del swan_obj.pprint_array

    def visit_TestHarness(
        self,
        swan_obj: swan.TestHarness,
        owner: Owner,
        owner_property: OwnerProperty,
    ) -> None:
        """
        Test Harness visitor

        Parameters
        ----------
        swan_obj : S.TestHarness
            Visited Swan object, it's a TestHarness instance
        owner : Owner
            Owner of the swan_obj, 'None' for the root visited object
        owner_property : OwnerProperty
            Owner property name to know the visit context, 'None' for the root visited object
        """
        # Visit base class(es)
        self.visit_OperatorSignatureBase(swan_obj, owner, owner_property)
        _decl = R.DBlock()

        _decl << owner.pprint_array[owner_property]
        # Init data buffer
        swan_obj.pprint_array = {"body": None}
        # Visit properties
        if isinstance(swan_obj.body, (swan.Scope, swan.Equation)):
            self._visit(swan_obj.body, swan_obj, "body")
            _decl << "@n"
            if isinstance(swan_obj.body, swan.Equation):
                _decl << "  "
            _decl << swan_obj.pprint_array["body"]
        else:
            _decl << ";"
        # Update property
        PPrinter._update_property(owner, owner_property, _decl)


PPrinter.visit_TestModule = PPrinterTestHarness.visit_TestModule
PPrinter.visit_TestHarness = PPrinterTestHarness.visit_TestHarness



class TestHarnessAddDiagram(swan.TestHarness):
    """Test Harness with additional methods for adding diagrams."""

    def add_diagram(self) -> None:
        """Add a diagram to the Test Harness."""
        diag = swan.Diagram()
        if not self.body or not self.body.sections:
            scope = swan.Scope([diag])
            scope.owner = self
            self._body = scope
            return diag
        self._body._sections.append(diag)
        return diag


swan.TestHarness.add_diagram = TestHarnessAddDiagram.add_diagram


# Wrapper for a function
def wrap_visit_operator_signature_base(
    func: Callable[..., None],
):
    @wraps(func)
    def wrapper(
        self,
        swan_obj: swan.Signature,
        owner: Owner,
        owner_property: OwnerProperty,
    ) -> None:
        if isinstance(swan_obj, swan.TestHarness):
            swan_obj.pprint_array = {"id": None}
            self._visit(swan_obj.id, swan_obj, "id")
            _decl = R.DBlock() << "_harness " << swan_obj.pprint_array["id"]
            PPrinter._update_property(owner, owner_property, _decl)
            del swan_obj.pprint_array
        else:
            func(self, swan_obj, owner, owner_property)

    return wrapper


PPrinter.visit_OperatorSignatureBase = wrap_visit_operator_signature_base(
    PPrinter.visit_OperatorSignatureBase
)


def add_test_harness(module: swan.Module, name: str) -> swan.TestHarness:
    """Add a Test Harness in a module"""
    harness = swan.TestHarness(get_valid_id(name), body=None)
    module.declarations.append(harness)
    return harness
