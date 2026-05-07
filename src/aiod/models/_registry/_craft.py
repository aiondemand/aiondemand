"""Quick crafting methods to build an object from string.

craft(spec)
    craft an object or estimator from string

deps(spec)
    retrieves all dependencies required to craft str, in PEP440 format

The ``craft`` function is a pair to ``str`` coercion, the two can be seen as
deserialization/serialization counterparts to each other.

That is,
spec = str(my_est)
new_est = craft(spec)

will have the same effect as new_est = spec.clone()
"""

import re

from aiod.models._registry._cls_lookup import _retrieve


def _extract_var_names(spec):
    """Get all unknown variable names in a python expression.

    Parameters
    ----------
    spec : str
        A python expression as a string.

    Returns
    -------
    names : set of str
        All variable names in the expression that are not keywords or builtins.
    """
    import ast
    import keyword
    import builtins

    tree = ast.parse(spec, mode='exec')

    names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }

    excluded = set(keyword.kwlist) | set(dir(builtins))
    return names - excluded


def craft(spec):
    """Instantiate an object from the specification string.

    Parameters
    ----------
    spec : str
        A string that evaluates to construct an object if all required
        class names are available in scope.

    Returns
    -------
    obj : constructed object
    """
    var_names = _extract_var_names(spec)

    register = {}

    for name in var_names:
        try:
            register[name] = _retrieve(name)
        except Exception as e:
            raise RuntimeError(
                f"class {name} is required to build spec, but get('{name}') failed"
            ) from e

    try:
        obj = eval(spec, globals(), register)
    except Exception:
        from textwrap import indent

        spec_fun = indent(spec, "    ")
        spec_fun = (
            """
def build_obj():
"""
            + spec_fun
        )

        exec(spec_fun, register, register)
        obj = eval("build_obj()", register, register)

    return obj


def deps(spec, include_test_deps=False):
    """Get PEP 440 dependency requirements for a craft spec.

    Parameters
    ----------
    spec : str
        Object specification string.

    include_test_deps : bool, default=False
        Whether to include test dependencies.

    Returns
    -------
    reqs : list of str
        PEP 440 compatible requirement strings.
    """
    dep_strs = []

    for x in _extract_var_names(spec):
        try:
            cls = _retrieve(x)
        except Exception as e:
            raise RuntimeError(
                f"object {x} is required to build spec, but get('{x}') failed"
            ) from e

        def _resolve_disjunctions(dep):
            if isinstance(dep, list):
                return dep[0]
            return dep

        def _coerce_dep_strs(dep):
            if dep is None:
                return []
            if isinstance(dep, str):
                return [dep] if len(dep) > 0 else []
            if isinstance(dep, list):
                return [_resolve_disjunctions(d) for d in dep]
            return dep

        new_deps = cls.get_class_tag("python_dependencies")
        dep_strs += _coerce_dep_strs(new_deps)

        if include_test_deps:
            test_deps = cls.get_class_tag("tests:python_dependencies")
            dep_strs += _coerce_dep_strs(test_deps)

    return list(set(dep_strs))


def imports(spec):
    """Get import code block for a craft spec.

    Parameters
    ----------
    spec : str
        Object specification string.

    Returns
    -------
    import_str : str
        Python import statements required for spec.
    """
    import_strs = []

    for x in _extract_var_names(spec):
        try:
            cls = _retrieve(x)
        except Exception as e:
            raise RuntimeError(
                f"class {x} is required to build spec, but get('{x}') failed"
            ) from e

        import_module = _get_public_import(cls.__module__)
        import_str = f"from {import_module} import {x}"
        import_strs.append(import_str)

    if len(import_strs) == 0:
        return ""

    return "\n".join(sorted(set(import_strs)))


def _get_public_import(module_path: str) -> str:
    """Get the public import path from full import path.

    Removes everything from the first private submodule
    (starting with '_') onwards.
    """
    parts = module_path.split(".")
    for i, part in enumerate(parts):
        if part.startswith("_"):
            return ".".join(parts[:i])
    return module_path
