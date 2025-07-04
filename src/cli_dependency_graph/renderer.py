"""
renderer.py: Render CLI command tree as ASCII
"""
from typing import List, Dict

def render_ascii_tree(commands: List[Dict]) -> str:
    if not commands:
        return "(no commands found)"
    lines = ["CLI Commands:"]
    for cmd in commands:
        lines.append(f"- {cmd['name']} ({cmd.get('type', 'command')})")
    return "\n".join(lines)
