"""Improved rendering for nested big arrays"""

# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 ANSYS, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from functools import wraps
from typing import Callable, Generator

import ansys.scadeone.core.svc.common.renderer as R
from ansys.scadeone.core import swan
from ansys.scadeone.core.svc.swan_visitor import Owner, OwnerProperty
from ansys.scadeone.core.svc.swan_printer import PPrinter


def get_array_dimensions(array: swan.ArrayConstructor) -> tuple[int, ...]:
    """Get array dimensions from a Swan API Expression"""
    if not isinstance(array, swan.ArrayConstructor):
        raise AttributeError(f"Expression is not an array: {array}")

    sizes: list[int] = []
    while isinstance(array, swan.ArrayConstructor):
        sizes.append(len(array.group.items))
        array = array.group.items[0].expr

    return tuple(sizes)


def get_max_nb_digits(array: swan.ArrayConstructor) -> int:
    """Get array dimensions from a Swan API Expression"""
    if not isinstance(array, swan.ArrayConstructor):
        raise AttributeError(f"Expression is not an array: {array}")

    def iter_nb_digits(arr: swan.ArrayConstructor) -> Generator[int, None, None]:
        for item in arr.group.items:
            if isinstance(item.expr, swan.ArrayConstructor):
                yield from iter_nb_digits(item.expr)
            elif isinstance(item.expr, swan.Literal):
                yield len(str(item.expr.value))

    return max(iter_nb_digits(array))


def render_array_or_value(swan_obj: swan.SwanItem, max_nb_digits: int = 0) -> None:
    """Simple rendering of an array or one of its value"""
    if isinstance(swan_obj, swan.ArrayConstructor):
        items = [
            render_array_or_value(v.expr, max_nb_digits) for v in swan_obj.group.items
        ]
        decl = R.DBlock()
        decl << "[" << R.doc_list(*items, sep=",") << "]"
    elif isinstance(swan_obj, swan.Literal):
        value = swan_obj.value
        if max_nb_digits:
            value = f"{value:<{max_nb_digits}}"
        decl = R.DText(value)
    else:
        raise AttributeError(
            f"Unsupported object: {swan_obj} (expected Array or Literal)"
        )
    return decl


def render_array_nicely(swan_obj: swan.ArrayConstructor) -> R.DBlock:
    """Render a numeric array of big dimensions more nicely"""
    dimensions = get_array_dimensions(swan_obj)
    if len(dimensions) <= 2:
        return render_array_or_value(swan_obj)

    max_nb_digits = get_max_nb_digits(swan_obj)
    sub_arrays = [
        render_array_or_value(i.expr, max_nb_digits) for i in swan_obj.group.items
    ]
    sep = R.DText(",") << "@n"
    return R.DBlock() << "[" << "@n" << R.doc_list(*sub_arrays, sep=sep) << "@n" << "]"


# Wrapper for a function
def wrap_visit_array_constructor(
    func: Callable[..., None],
):
    @wraps(func)
    def wrapper(
        self,
        swan_obj: swan.ArrayConstructor,
        owner: Owner,
        owner_property: OwnerProperty,
    ) -> None:
        dimensions = get_array_dimensions(swan_obj)
        if len(dimensions) <= 2:
            func(swan_obj, owner, owner_property)

        max_nb_digits = get_max_nb_digits(swan_obj)
        sub_arrays = [
            render_array_or_value(i.expr, max_nb_digits) for i in swan_obj.group.items
        ]
        sep = R.DBlock() << "," << "@n"
        _decl = R.DBlock()
        _decl << "[" << "@n" << R.doc_list(*sub_arrays, sep=sep) << "@n" << "]"
        PPrinter._update_property(owner, owner_property, _decl)

    return wrapper


PPrinter.visit_ArrayConstructor = wrap_visit_array_constructor(
    PPrinter.visit_ArrayConstructor
)

if __name__ == "__main__":
    import sys

    from ansys.scadeone.core.svc.swan_printer import swan_to_str

    from s1_api_utils import str2expr

    array_str = "[[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [84], [185], [159], [151], [60], [36], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [222], [254], [254], [254], [254], [241], [198], [198], [198], [198], [198], [198], [198], [198], [170], [52], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [67], [114], [72], [114], [163], [227], [254], [225], [254], [254], [254], [250], [229], [254], [254], [140], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [17], [66], [14], [67], [67], [67], [59], [21], [236], [254], [106], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [83], [253], [209], [18], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [22], [233], [255], [83], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [129], [254], [238], [44], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [59], [249], [254], [62], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [133], [254], [187], [5], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [9], [205], [248], [58], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [126], [254], [182], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [75], [251], [240], [57], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [19], [221], [254], [166], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [3], [203], [254], [219], [35], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [38], [254], [254], [77], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [31], [224], [254], [115], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [133], [254], [254], [52], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [61], [242], [254], [254], [52], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [121], [254], [254], [219], [40], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [121], [254], [207], [18], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]]"
    array = str2expr(array_str)

    R.Renderer(sys.stdout).render(R.Document() << render_array_nicely(array))

    print("\n" + "=" * 80)

    print(swan_to_str(array))
