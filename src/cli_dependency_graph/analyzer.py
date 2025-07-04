"""
analyzer.py: Static analysis for Click/Typer commands using ast
"""
import ast
import os
from typing import List, Dict

def scan_for_commands(path: str) -> List[Dict]:
    """Scan a file or directory for top-level Click/Typer commands."""
    commands = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    commands += _scan_file(os.path.join(root, f))
    else:
        commands += _scan_file(path)
    return commands

def _scan_file(filepath: str) -> List[Dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=filepath)
    except Exception:
        return []
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for deco in node.decorator_list:
                if (
                    isinstance(deco, ast.Call)
                    and isinstance(deco.func, ast.Attribute)
                    and deco.func.attr == "command"
                ):
                    found.append({"name": node.name, "file": filepath})
        if isinstance(node, ast.Assign):
            # Detect Typer() app assignment (very basic)
            if (
                isinstance(node.value, ast.Call)
                and hasattr(node.value.func, "id")
                and node.value.func.id == "Typer"
            ):
                for target in node.targets:
                    if hasattr(target, "id"):
                        found.append({"name": target.id, "file": filepath, "type": "typer_app"})
    return found
