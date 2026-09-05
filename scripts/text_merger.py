#!/usr/bin/env python3
"""
Merge text files into a single output.
Based on mergfiles.py and combine.py.
"""
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime 

class TextMerger:
    """Merge text files from a directory."""
    
    @staticmethod
    def merge(root_dir: str, output_path: str,
              extensions: Optional[List[str]] = None,
              include_filenames: bool = True) -> int:
        """Merge files into one output."""
        root = Path(root_dir)
        output = Path(output_path)
        
        output.parent.mkdir(parents=True, exist_ok=True)
        extensions = set(extensions or ['.pyc', '.sqlite3'])
        merged_count = 0
        
        with open(output, 'w', encoding='utf-8') as out:
            for file_path in sorted(root.rglob('*')):
                if not file_path.is_file():
                    continue
                
                if (file_path.suffix.lower() in extensions):
                    continue
                print(file_path)
                try:
                    rel_path = file_path.relative_to(root)
                    
                    if include_filenames:
                        out.write(f"\n{'='*50}\n")
                        out.write(f"File: {rel_path}\n")
                        out.write(f"{'='*50}\n\n")
                    
                    out.write(file_path.read_text(encoding='utf-8', errors='ignore'))
                    out.write("\n\n")
                    merged_count += 1
                    
                except Exception as e:
                    print(f"Error merging {file_path}: {e}")
        
        print(f"Merged {merged_count} files into {output}")
        return merged_count

def main():
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "." 
    output = sys.argv[2] if len(sys.argv) > 2 else 'merged.txt'
    TextMerger.merge(root, output)

if __name__ == "__main__":
    main()
