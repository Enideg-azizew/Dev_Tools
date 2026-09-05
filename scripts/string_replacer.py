#!/usr/bin/env python3
"""
Find and replace strings in files.
Based on subn.py.
"""
import re
from pathlib import Path
from typing import Optional, List, Set

class StringReplacer:
    """Find and replace strings in files."""
    
    @staticmethod
    def replace(root_dir: str, search: str, replace: str,
                extensions: Optional[List[str]] = None,
                preview: bool = True) -> int:
        """Replace strings in files."""
        root = Path(root_dir)
        extensions = set(extensions or [])
        total_replacements = 0
        files_processed = 0
        
        for file_path in root.rglob('*'):
            if not file_path.is_file():
                continue
            
            if extensions and file_path.suffix.lower() not in extensions:
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                if search not in content:
                    continue
                
                new_content, count = re.subn(re.escape(search), replace, content)
                
                if count > 0:
                    if preview:
                        print(f"\n{file_path}: {count} replacement(s)")
                        print(f"  Preview: {content[:100]}...")
                        if input("  Apply? (y/n): ").lower() != 'y':
                            continue
                    
                    file_path.write_text(new_content, encoding='utf-8')
                    total_replacements += count
                    files_processed += 1
                    
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        print(f"\nTotal: {files_processed} files, {total_replacements} replacements")
        return total_replacements

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python string_replacer.py <root_dir> <search> <replace> [ext1 ext2 ...]")
        sys.exit(1)
    
    root = sys.argv[1]
    search = sys.argv[2]
    replace = sys.argv[3]
    extensions = sys.argv[4:] if len(sys.argv) > 4 else None
    
    StringReplacer.replace(root, search, replace, extensions)

if __name__ == "__main__":
    main()
