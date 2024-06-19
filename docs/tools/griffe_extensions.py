import sys
from ast import AST

from griffe.agents.nodes import ObjectNode
from griffe.dataclasses import Module
from griffe.extensions import Extension
from griffe.agents.inspector import inspect


class DynamicAnalysisExtension(Extension):
    # Define our init method and the options that can be passed from `mkdocs.yml`.
    def __init__(self, modules: list[str]) -> None:
        self.modules = modules

    # Once the static analyzer has finished scanning a module,
    # we do a second pass using dynamic analysis.
    # We don't do it before because the static analysis would overwrite our changes.
    def on_module_members(self, *, node: AST | ObjectNode, mod: Module) -> None:
        # Object nodes mean we're already doing dynamic analysis.
        if isinstance(node, ObjectNode):
            return

        # Skip unselected modules.
        if mod.path not in self.modules:
            return

        # Inspect the module using dynamic analysis.
        inspected_module = inspect(
            mod.name,
            filepath=mod.filepath,
            parent=mod.parent,
            import_paths=list(sys.path),
            docstring_parser="google",
        )

        # Discard all previous existing members obtained through static analysis,
        # and replace them with those obtained through dynamic analysis.
        for name, member in inspected_module.members.items():
            if member in mod.members:
                mod.del_member(name)
            mod.set_member(name, member)
