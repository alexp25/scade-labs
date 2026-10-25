"""Try creating a S1 project from a Keras model

IMPORTANT: Patch the method Method.__str__ in ansys.scadeone.swan.modules.py as follows:

```python
    def __str__(self) -> str:
        decls = (str(d) for d in chain(self.use_directives, self.declarations))
        return '\n\n'.join(decls)
```
... this will improve the pretty-print of modules
"""

from pathlib import Path

from ansys.scadeone.core import swan
from ansys.scadeone.core.swan import Identifier, Luid, Operator, VarDecl
from s1_api.project import ProjectFolder
from s1_api.s1_api_utils import (
    luid2connection,
    LiteralNumeric,
    identifier2call,
    identifier2expr,
    identifier2path,
    items2array,
    op2iterator,
    str2type,
)

diagram_obj_forward = [
    swan.SectionBlock(
        section=swan.LetSection(
            equations=[
                swan.ExprEquation(
                    lhs=swan.EquationLHS([swan.LHSItem("o")]),
                    expr=identifier2expr("10_i32 + i"),
                )
            ]
        ),
        luid=Luid("11"),
    ),
]

diagram_obj = [
    swan.ExprBlock(identifier2expr("i0"), luid=Luid("0")),
    swan.DefBlock(
        swan.EquationLHS([swan.LHSItem(swan.Identifier("o0"))]), luid=Luid("1")
    ),
    swan.Wire(
        source=luid2connection("0"),
        targets=[luid2connection("1")],
        luid=Luid("2"),
    ),
    swan.ExprBlock(
        swan.ArrayRepetition(identifier2expr("i0"), size=LiteralNumeric(2)),
        luid=Luid("3"),
    ),
    swan.Block(identifier2call("operator1"), luid=Luid("4")),
    swan.Block(identifier2call("operatorSized", sizes=[1, 2]), luid=Luid("5")),
    swan.ExprBlock(
        items2array(
            [items2array([LiteralNumeric(1)]), items2array([LiteralNumeric(2)])]
        ),
        luid=Luid("6"),
    ),
    swan.Wire(
        source=luid2connection("6"),
        targets=[luid2connection(Luid("5"), adaptation="i0")],
        luid=Luid("7"),
    ),
    swan.SectionBlock(
        section=swan.LetSection(
            equations=[
                swan.ExprEquation(
                    lhs=swan.EquationLHS([swan.LHSItem("o1")]),
                    expr=identifier2expr("10_i32"),
                )
            ]
        ),
        luid=Luid("8"),
    ),
    swan.SectionBlock(
        section=swan.LetSection(
            equations=[
                swan.ActivateIf(
                    if_activation=swan.IfActivation(
                        branches=[
                            swan.IfActivationBranch(
                                condition="true",
                                branch=swan.IfteDataDef(swan.Scope([])),
                            ),
                            swan.IfActivationBranch(
                                condition=None, branch=swan.IfteDataDef(swan.Scope([]))
                            ),
                        ],
                    )
                )
            ]
        ),
        luid=Luid("9"),
    ),
    swan.ExprBlock(
        expr=swan.ForwardExpr(
            body=swan.ForwardBody(
                body=[swan.Diagram(diagram_obj_forward)],
                until_expr=swan.BinaryExpr(
                    left="o",
                    operator=swan.BinaryOp.Equal,
                    right="0_i32",
                ),
            ),
            dimensions=[swan.ForwardDim(dim_id="i", expr=LiteralNumeric(10))],
            returns=[
                swan.ForwardReturnArrayClause(
                    array_clause=swan.ForwardArrayClause(
                        return_clause=swan.ForwardItemClause(
                            id="o",
                            last_default=swan.ForwardLastDefault(default="10_i32"),
                        )
                    )
                )
            ],
            state=swan.ForwardState(swan.ForwardState.Resume),
        ),
        luid=Luid("10"),
    ),
]

body = swan.Scope([swan.Diagram(diagram_obj)])

TType = Identifier("T", is_name=True)
TTypeConstraint = swan.TypeConstraint(
    [swan.VariableTypeExpression(TType)], swan.NumericKind.Integer
)
in2 = VarDecl(id=Identifier("i0"), var_type=str2type("'T^2"))
out2 = VarDecl(id=Identifier("o0"), var_type=str2type("int32^2"))
out3 = VarDecl(id=Identifier("o1"), var_type=str2type("int32"))
op = Operator(
    Identifier("my_op"),
    is_node=False,
    has_inline=False,
    inputs=[in2],
    outputs=[out2, out3],
    constraints=[TTypeConstraint],
    body=body,
)

use_decl = [
    swan.UseDirective(identifier2path("keras::layers")),
    swan.UseDirective(identifier2path("module2")),
]
groups_decl = swan.GroupDeclarations(
    [swan.GroupDecl(Identifier("position"), "(x: float32, y:float32)")]
)
const_decl = swan.ConstDeclarations(
    [swan.ConstDecl(Identifier("my_value"), str2type("float32"), LiteralNumeric("2.5"))]
)
op_decl = [op]
mod = swan.ModuleBody(
    identifier2path("my_module"),
    uses=use_decl,
    decls=[groups_decl, const_decl, *op_decl],
)

print("== MODULE ===")
print(mod)
print("=" * 10)

root = Path(__file__).with_name("created")
folder = ProjectFolder(
    root, modules=[mod], source_files=[("my_file.c", '#include "math.h"')]
)
folder.write()
