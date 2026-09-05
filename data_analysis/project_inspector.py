#!/usr/bin/env python3
"""
Project structure inspector.
Based on project_inspector.py.
"""
import os
import sys
from pathlib import Path
from typing import Optional

class ProjectInspector:
    """Inspect and visualize project directory structure."""
    
    @staticmethod
    def get_structure(root_dir: str, max_depth: int = 5, max_items: int = 50) -> str:
        """Get directory structure as text."""
        root = Path(root_dir)
        lines = []
        lines.append("=" * 70)
        lines.append(f"PROJECT STRUCTURE")
        lines.append(f"Root: {root.absolute()}")
        lines.append("=" * 70)
        lines.append("")
        
        def walk(path: Path, depth: int = 0, prefix: str = ""):
            if depth > max_depth:
                return
            
            try:
                items = sorted([p for p in path.iterdir() if not p.name.startswith('.')])
                items = [p for p in items if p.name not in ['node_modules', '__pycache__']]
                
                for i, item in enumerate(items[:max_items]):
                    is_last = i == len(items) - 1
                    current_prefix = "    " * depth
                    if item.is_dir():
                        lines.append(f"{current_prefix}├── {item.name}/")
                        walk(item, depth + 1)
                    else:
                        size = item.stat().st_size
                        lines.append(f"{current_prefix}├── {item.name} ({size} bytes)")
            except PermissionError:
                lines.append(f"{current_prefix}├── [Permission Denied]")
        
        walk(root)
        return "\n".join(lines)
    
    @staticmethod
    def save_structure(root_dir: str, output_file: str = "structure.txt",
                       max_depth: int = 5) -> None:
        """Save directory structure to file."""
        structure = ProjectInspector.get_structure(root_dir, max_depth)
        Path(output_file).write_text(structure, encoding='utf-8')
        print(f"✅ Structure saved to: {output_file}")

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "structure.txt"
    ProjectInspector.save_structure(root, output)

if __name__ == "__main__":
    main()
