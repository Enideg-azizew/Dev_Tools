#!/usr/bin/env python3
"""
Unified file operations: copy, merge, and directory tree utilities.
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Union

class FileOperations:
    """File and directory operation utilities."""
    
    @staticmethod
    def should_exclude(path: Union[str, Path], excludes: List[str]) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)
        return any(exclude in path_str for exclude in (excludes or []))
    
    @staticmethod
    def copy_project(source_dir: Union[str, Path], dest_dir: Union[str, Path],
                     excludes: Optional[List[str]] = None) -> int:
        """Copy a directory tree with exclusions."""
        source = Path(source_dir)
        dest = Path(dest_dir)
        excludes = excludes or []
        
        if not source.exists():
            raise ValueError(f"Source directory '{source}' does not exist")
        
        dest.mkdir(parents=True, exist_ok=True)
        copied_count = 0
        
        for file_path in source.rglob('*'):
            if not file_path.is_file() or FileOperations.should_exclude(file_path, excludes):
                continue
            
            rel_path = file_path.relative_to(source)
            dest_path = dest / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(file_path, dest_path)
                copied_count += 1
            except Exception as e:
                print(f"Error copying {rel_path}: {e}")
        
        return copied_count
    
    @staticmethod
    def merge_files(root_dir: Union[str, Path], output_file: Union[str, Path],
                    excludes: Optional[List[str]] = None) -> int:
        """Merge all files in a directory into one output file."""
        root = Path(root_dir)
        output = Path(output_file)
        excludes = excludes or []
        
        output.parent.mkdir(parents=True, exist_ok=True)
        merged_count = 0
        
        with open(output, 'w', encoding='utf-8') as out_f:
            for file_path in sorted(root.rglob('*')):
                if not file_path.is_file() or FileOperations.should_exclude(file_path, excludes):
                    continue
                
                try:
                    rel_path = file_path.relative_to(root)
                    out_f.write(f"\n\n\n--- {rel_path} ---\n")
                    out_f.write(file_path.read_text(encoding='utf-8', errors='ignore'))
                    merged_count += 1
                except Exception as e:
                    print(f"Error merging {file_path}: {e}")
        
        return merged_count
    
    @staticmethod
    def safe_delete(path: Union[str, Path]) -> bool:
        """Safely delete a file or directory."""
        path = Path(path)
        try:
            if not path.exists():
                return True
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting {path}: {e}")
            return False
    
    @staticmethod
    def get_size(path: Union[str, Path]) -> int:
        """Get size of a file or directory."""
        path = Path(path)
        if not path.exists():
            return 0
        if path.is_file():
            return path.stat().st_size
        
        total = 0
        for file_path in path.rglob('*'):
            if file_path.is_file():
                total += file_path.stat().st_size
        return total
    
    @staticmethod
    def get_structure(root_dir: Union[str, Path], max_depth: int = 5) -> str:
        """Get a text representation of directory structure."""
        root = Path(root_dir)
        lines = []
        
        def walk(path: Path, depth: int = 0, prefix: str = ""):
            if depth > max_depth:
                return
            
            try:
                items = sorted([p for p in path.iterdir() if not p.name.startswith('.')])
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "    " * depth
                    if item.is_dir():
                        lines.append(f"{current_prefix}├── {item.name}/")
                        walk(item, depth + 1, current_prefix + "│   ")
                    else:
                        size = item.stat().st_size
                        lines.append(f"{current_prefix}├── {item.name} ({size} bytes)")
            except PermissionError:
                lines.append(f"{current_prefix}├── [Permission Denied]")
        
        walk(root)
        return "\n".join(lines)
