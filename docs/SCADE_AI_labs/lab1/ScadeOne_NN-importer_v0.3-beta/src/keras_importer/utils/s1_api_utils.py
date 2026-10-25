import logging
import re
from functools import wraps
from typing import Any, Iterable, Optional, TypeVar, Union, cast

import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore
from ansys.scadeone.core import swan  # type: ignore
from ansys.scadeone.core.common.exception import ScadeOneException  # type: ignore
from ansys.scadeone.core.common.storage import SwanString  # type: ignore
from ansys.scadeone.core.model.loader import SwanParser  # type: ignore
from ansys.scadeone.core.svc.swan_creator.diagram_creator import DiagramFactory
from ansys.scadeone.core.svc.swan_creator.module_creator import DeclarationAdder, DeclarationFactory
from ansys.scadeone.core.swan import Identifier, Luid, ConstDecl  # type: ignore
from ansys.scadeone.core.svc.swan_printer import PPrinter

LOGGER = logging.getLogger("keras_importer.utils")

EasySize = Union[int, str, swan.Expression]
ListEasySize = Union[list[int], list[EasySize]]
IdentifierStr = Union[swan.Identifier, str]


class NullLogger(logging.Logger):
    """Dummy logger to remove all logging"""

    def _log(self, *args, **kwargs) -> None:
        # We disable the logging on purpose
        pass


SWAN_PARSER = SwanParser(logger=NullLogger("null"))

# IMPORTANT: No support of "is_shortcut" in "renaming" :(
TGrRenaming = Union[Union[str, int], tuple[Union[str, int], str]]
TGrAdaptation = Union[swan.GroupAdaptation, TGrRenaming, list[TGrRenaming]]

SCADE_KEYWORDS = [
    "activate",
    "and",
    "as",
    "assume",
    "automaton",
    "block",
    "byname",
    "bypos",
    "case",
    "clock",
    "const",
    "def",
    "default",
    "diagram",
    "else",
    "elsif",
    "emit",
    "end",
    "end",
    "enum",
    "every",
    "expr",
    "flatten",
    "fold",
    "foldi",
    "forward",
    "function",
    "group",
    "guarantee",
    "if",
    "initial",
    "inline",
    "is",
    "land",
    "last",
    "let",
    "lnot",
    "lor",
    "lsl",
    "lsr",
    "lxor",
    "make",
    "map",
    "mapfold",
    "mapfoldi",
    "mapi",
    "match",
    "merge",
    "mod",
    "node",
    "not",
    "of",
    "or",
    "pack",
    "package",
    "pragma",
    "pre",
    "restart",
    "resume",
    "returns",
    "reverse",
    "self",
    "sensor",
    "specialize",
    "state",
    "then",
    "transpose",
    "type",
    "unless",
    "until",
    "us",
    "var",
    "when",
    "where",
    "window",
    "wire",
    "with",
    "xor",
]


def get_valid_swan_name(name: str, role: Optional[str] = None, scope: Any = None) -> str:
    """Returns a valid Swan name that is unique in its scope."""
    if name is None:
        name = role or "unnamed"

    # For the base name, we want to keep the `::` for the module
    base_name = re.sub(r"[^\w:]+|(?<!:):(?!:)|:{3,}", "_", name.strip())
    count = 1
    name = base_name
    keywords = SCADE_KEYWORDS

    _ = scope  # TODO: consider adding scope checking to avoid duplicate names
    # ... if isinstance(scope, swan.Operator):
    #     if role in (
    #         "input",
    #         "output",
    #         "hidden",
    #         "parameter",
    #         "local",
    #         "internal",
    #         "probe",
    #         "signal",
    #     ):
    #         keywords += [e.name for e in chain(scope.inputs, scope.outputs)]
    #     elif role == "diagram" or role == "text_diagram":
    #         keywords += [d.name for d in scope.diagrams]
    #     else:
    #         pass  # TODO: consider missing cases
    # elif isinstance(scope, swan.Module):
    #     if role in ["operator", "constant", "type", "sensor"]:
    #         keywords += [
    #             e.name
    #             for e in scope.operators
    #             + scope.constants
    #             + scope.named_types
    #             + scope.sensors
    #         ]
    #     elif role == "package":
    #         keywords += [e.name for e in scope.packages]
    #     else:
    #         pass  # TODO: consider missing cases
    # else:
    #     pass  # TODO: consider missing cases

    while name in keywords:
        name = f"{base_name}_{count}"
        count += 1

    return name


def get_valid_id(
    name: str, role: Optional[str] = None, scope: Any = None
) -> swan.Identifier:
    """Returns a valid Swan Identifier that is unique in its scope."""
    return swan.Identifier(get_valid_swan_name(name, role, scope))


def repeat_expr(expr: swan.Expression, sizes: Iterable[Optional[int]]) -> swan.Expression:
    """Repeat an expression a given number of times"""
    for size in sizes:
        if size:
            expr = swan.ArrayRepetition(expr, size=swan.Literal(str(size)))
    return expr


class LiteralNumeric(swan.Literal):
    """Class for numeric literal"""

    def __init__(self, value: Union[str, int, float]):
        super().__init__(str(value))

    def repeat(
        self, shapes: Iterable[Optional[int]]
    ) -> Union[swan.Literal, swan.ArrayRepetition]:
        """Repeat the literal a given number of times

        Example: Literal(0).repeat([2, 4, 6]) => 0^2^4^6
        """
        return repeat_expr(self, shapes)


PPrinter.visit_LiteralNumeric = PPrinter.visit_Literal


class LiteralBool(swan.Literal):
    """Class for boolean literal entered as either boolean or string (true/false)"""

    def __init__(self, value: Union[str, bool]):
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, str) and value not in ("true", "false"):
            raise AttributeError(
                "Incorrect boolean value:"
                f" it shall be either `true` or `false` but is: {value}"
            )
        super().__init__(value)


class LiteralChar(swan.Literal):
    """Class for char literal (a single character) entered as int or string"""

    def __init__(self, value: Union[str, int]):
        if isinstance(value, int):
            value = chr(value)
        elif isinstance(value, str):
            if len(value.strip("'")) != 1:
                raise AttributeError(
                    f"Incorrect size: character shall be of length 1 but is: {value}"
                )
            value = value.strip("'")

        super().__init__(f"'{value}'")


def identifier2path(identifier: IdentifierStr) -> swan.PathIdentifier:
    """Create a Path identifier from a single identifier"""
    return swan.PathIdentifier([get_valid_id(identifier)])


def identifier2expr(identifier: IdentifierStr) -> swan.PathIdExpr:
    """Create an expression to Path identifier from a single identifier"""
    return swan.PathIdExpr(identifier2path(identifier))


def identifier2def(
    identifier: Union[IdentifierStr, list[IdentifierStr]],
) -> swan.EquationLHS:
    """Create an expression to Path identifier from a single identifier"""
    if isinstance(identifier, list):
        identifier = [get_valid_id(i) for i in identifier]
    else:
        identifier = [get_valid_id(identifier)]

    return swan.EquationLHS([swan.LHSItem(i) for i in identifier])


def value2size(size: EasySize) -> swan.Expression:
    """Transform a value (int, int as string, or size parameter) into a size"""
    if isinstance(size, swan.Expression):
        return size

    if isinstance(size, int) or size.isdecimal():
        return LiteralNumeric(size)

    return swan.PathIdExpr(identifier2path(size))


def identifier2call(
    identifier: IdentifierStr, sizes: Optional[list[EasySize]] = None
) -> swan.PathIdOpCall:
    """Create a call to Path identifier from a single identifier and optional sizes"""
    sizes_as_expr = [value2size(s) for s in sizes] if sizes else []
    # TODO: consider adding pragmas
    return swan.PathIdOpCall(identifier2path(identifier), sizes=sizes_as_expr, pragmas=[])


def get_underscore_def_block(diag: Optional[swan.Diagram] = None) -> swan.DefBlock:
    block = swan.DefBlock(swan.EquationLHS([swan.LHSItem()]))
    if diag is not None:
        diag._diagram_adder.add_def_block(block)
    return block


def add_block_from_id(
    operator: Union[swan.Operator, str],
    diagram: Optional[swan.Diagram] = None,
    sizes: Optional[ListEasySize] = None,
) -> swan.Block:
    """Add a block from a given ID to a diagram"""
    sizes_expr = [swan.Literal(str(size)) for size in sizes] if sizes else []

    if isinstance(operator, swan.Operator):
        block = DiagramFactory().create_block(diagram, operator)
        if sizes:
            block.instance._sizes = sizes_expr
    else:
        path_id = swan.PathIdentifier.from_string(get_valid_swan_name(operator))
        path_id_op_call = swan.PathIdOpCall(path_id, sizes=sizes_expr, pragmas=[])
        block = swan.Block(path_id_op_call)

    if diagram:
        diagram._diagram_adder.add_block(block)

    return block


def _easy_renaming(renaming: TGrRenaming) -> swan.GroupRenaming:
    """Create a group renaming more easily"""
    renaming_id: Optional[Identifier] = None
    if not isinstance(renaming, tuple):
        source_id = renaming
    else:
        source_id = renaming[0]
        renaming_id = Identifier(renaming[1])
    if isinstance(source_id, int):
        return swan.GroupRenaming(LiteralNumeric(source_id), renaming_id)
    else:
        return swan.GroupRenaming(Identifier(source_id), renaming_id)


def _easy_adaptation(adaptation: TGrAdaptation) -> swan.GroupAdaptation:
    """Create a group adaptation more easily"""
    if isinstance(adaptation, swan.GroupAdaptation):
        return adaptation

    if isinstance(adaptation, list):
        return swan.GroupAdaptation([_easy_renaming(a) for a in adaptation])
    return swan.GroupAdaptation([_easy_renaming(adaptation)])  # single element


def luid2connection(
    luid: Union[int, str, Luid, swan.DiagramObject],
    adaptation: Optional[TGrAdaptation] = None,
) -> swan.Connection:
    """Easier creation of extension from a luid and eventually an adaptation"""
    if isinstance(luid, (int, str)):
        luid = Luid(str(luid))
    elif isinstance(luid, swan.DiagramObject):
        if luid.luid is None:
            raise AttributeError(
                f"Diagram object with no luid, but expecting one: {luid!r}\n{luid}"
            )
        luid = luid.luid

    if adaptation is not None:
        adaptation = _easy_adaptation(adaptation)

    # For type checking
    adaptation = cast(Optional[swan.GroupAdaptation], adaptation)
    return swan.Connection(swan.PortExpr(luid), adaptation=adaptation)  # type: ignore


def _replace_groups(type_group: str) -> str:
    """Replace groups by `<group>` (if any)"""
    if "(" not in type_group:
        return type_group

    return _replace_groups(re.sub(r"\s*\([^()]*\)\s*", " <group> ", type_group))


def deactivate_swan_logger(func):
    """Deactivate Scade One Logger (typically when using Parser)"""
    s1_logger = logging.getLogger("ScadeOneLogger")

    @wraps(func)
    def wrapper(*args, **kwargs):
        s1_logger_level = s1_logger.level
        try:
            s1_logger.setLevel(logging.CRITICAL)  # to hide some errors
            return func(*args, **kwargs)
        finally:
            s1_logger.setLevel(s1_logger_level)

    return wrapper


@deactivate_swan_logger
def str2type(type_as_str: str) -> swan.GroupTypeExpression:
    """Get type as Swan API Expression from a type as a string"""
    try:
        if type_as_str.strip().startswith("("):
            if not type_as_str.rstrip().endswith(")"):
                raise AttributeError(
                    f"Type is a group but does not end with a parenthesis: {type_as_str}"
                )
            group_decl = SWAN_PARSER.declaration(SwanString(f"group G = {type_as_str};"))
            return group_decl.groups[0].type  # type: ignore
        else:
            type_decl = SWAN_PARSER.declaration(SwanString(f"type T = {type_as_str};"))
            return type_decl.types[0].definition  # type: ignore
    except ScadeOneException as exc:
        raise AttributeError(f"ERROR when parsing type {type_as_str}: {exc}") from None


@deactivate_swan_logger
def str2expr(expr_as_str: str) -> swan.Expression:
    """Get a Swan API Expression from a representation in string"""
    try:
        expr = SWAN_PARSER.expression(SwanString(expr_as_str))
        return cast(swan.Expression, expr)
    except ScadeOneException as exc:
        raise AttributeError(
            f"ERROR when parsing expression {expr_as_str}: {exc}"
        ) from None


EasyGroupItem = Union[swan.Expression, tuple[swan.Expression, str]]


def var2str(var: Union[np.ndarray, tf.Variable]) -> str:
    """Get a string representation of the variable, nicely aligned"""
    if isinstance(var, tf.Variable):
        var = var.numpy()  # type: ignore

    var = cast(np.ndarray, var)
    content = ",\n".join(str(a) for a in var.tolist())

    # We will align all the numbers based on the maximum length
    try:
        # ? Do we need to keep the spaces `\s*` around the regex?
        patt_nb = r"\s*[+\-]?\d+(?:\.(?:\d+)?(?:[eE][+\-]?\d+)?)?\s*"
        max_nb_digits = max(len(n) for n in re.findall(patt_nb, content))

        content = re.sub(patt_nb, lambda m: f"{m.group(0):<{max_nb_digits}}", content)
    except ValueError:  # in case the regex does not match a number
        LOGGER.debug(f"Auto-alignment not applied on {var}")

    return f"[\n{content}\n]"


def var2expr(var: Union[np.ndarray, tf.Variable]) -> swan.Expression:
    """Convert a Variable to a Swan Expression of the given value"""
    return str2expr(var2str(var).replace("\n", ""))


def items2array(items: list[EasyGroupItem]) -> swan.ArrayConstructor:
    """Create an array more easily

    Args:
        items: list of expressions, or tuple (expression, label)
    Returns:
        Constructed array
    """

    def parse_item(item: EasyGroupItem) -> swan.GroupItem:
        if isinstance(item, tuple):
            return swan.GroupItem(item[0], Identifier(item[1]))
        return swan.GroupItem(item)

    return swan.ArrayConstructor(swan.Group([parse_item(i) for i in items]))


def op2iterator(
    kind: swan.IteratorKind,
    sizes: Union[EasySize, ListEasySize],
    operator: swan.OperatorBase,
) -> swan.OperatorBase:
    """Create an iterator (map, fold, ...) more easily"""
    if sizes is None:
        return operator

    if not isinstance(sizes, list):
        sizes = [sizes]
    return swan.PrefixOperatorExpression(
        swan.Iterator(kind, operator), sizes=[value2size(s) for s in sizes]
    )


def op2iterators(
    kind: swan.IteratorKind,
    operator: swan.OperatorBase,
    sizes: Optional[ListEasySize] = None,
) -> swan.OperatorBase:
    """Create nested iterators (map, fold, ...) from an operator

    Note: the sizes shall be in the order from the most inside to the most outside
    """
    if not sizes:
        return operator

    operator = op2iterator(kind, sizes.pop(0), operator)
    return op2iterators(kind, operator, sizes)


def op2map(
    operator: swan.OperatorBase, sizes: Optional[ListEasySize]
) -> swan.OperatorBase:
    """Create nested map(s) from an operator

    Note: the sizes shall be in the order from the most inside to the most outside
    """
    return op2iterators(swan.IteratorKind.Map, operator, sizes)


TDecl = TypeVar("TDecl", swan.Signature, swan.ConstDeclarations, swan.TypeDeclarations)


def add_declaration_to_module(module: swan.Module, decl: TDecl) -> TDecl:
    """Add a declaration to a module (body or interface)
    Note: a declaration can be an operator, a constant, a type, or a group
    """
    # As for the module interface, an operator shall have no body (i.e. a Signature)
    # we could either copy the operator or create a new Signature with the same content
    # (except the body): the second method is cleaner
    # Note that other declaration types could be put directly in either type of module
    if isinstance(module, swan.ModuleInterface) and isinstance(decl, swan.Operator):
        decl = swan.Signature(
            id=decl.identifier,
            has_inline=decl.has_inline,
            is_node=decl.is_node,
            inputs=list(decl.inputs),
            outputs=list(decl.outputs),
            sizes=list(decl.sizes),
            constraints=list(decl.constraints),
            specialization=decl.specialization,
            pragmas=list(decl.pragmas),
        )

    # pylint: disable=protected-access
    module._declarations.append(decl)  # type: ignore
    return decl


def add_constant_without_value(module: swan.Module, name: str, type_str: str) -> "swan.ConstDecl":
    """Add a constant to the module without value (i.e. imported constant).

    Parameters
    ----------
    name: str
        Constant name.
    type_str: Str
        Constant type.

    Returns
    -------
    ConstDecl
        Constant object.
    """
    const = DeclarationFactory().create_declaration(f"const {name}: {type_str}")
    DeclarationAdder.add_declaration(module, const)
    return cast(ConstDecl, const)
