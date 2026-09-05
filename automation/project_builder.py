#!/usr/bin/env python3
"""
Build projects from a single file containing code blocks with filenames.
Combines projecter.py and split_text.py functionality.
"""
import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

class ProjectBuilder:
    """Build project files from a metafile containing code blocks."""
    
    def __init__(self):
        self.block_count = 0
        self.files_created = []
    
    @staticmethod
    def extract_filename(line: str) -> Optional[str]:
        """Extract filename from a comment line."""
        # Remove comment markers
        cleaned = line.strip()
        # Remove common comment prefixes
        for prefix in ["# ", "<!-- ", "// ", "/* ", "*/ "]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
        # Remove suffix
        if cleaned.endswith(" -->"):
            cleaned = cleaned[:-4]
        return cleaned.strip()
    
    def build_from_file(self, metafile_path: str, output_dir: Optional[str] = None) -> int:
        """Build project from a metafile containing code blocks."""
        metafile_path = Path(metafile_path)
        if not metafile_path.exists():
            raise FileNotFoundError(f"Metafile not found: {metafile_path}")
        
        # Determine output directory
        if output_dir is None:
            output_dir = metafile_path.stem + "_project"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.block_count = 0
        self.files_created = []
        
        content = metafile_path.read_text(encoding='utf-8')
        lines = content.splitlines()
        
        i = 0
        total_lines = len(lines)
        
        while i < total_lines:
            line = lines[i].strip()
            
            # Look for code block start: ```language
            if line.startswith('```') and len(line) > 3:
                # Find filename (look back up to 5 lines)
                filename = None
                for offset in range(1, 6):
                    if i - offset >= 0:
                        candidate = self.extract_filename(lines[i - offset])
                        if candidate and '.' in candidate:
                            filename = candidate
                            break
                
                if filename:
                    content_start = i + 1
                    
                    # Find end marker
                    content_end = None
                    for j in range(content_start, total_lines):
                        if lines[j].strip() == '```':
                            content_end = j
                            break
                    
                    if content_end is not None:
                        # Extract content
                        content_lines = lines[content_start:content_end]
                        file_content = '\n'.join(content_lines)
                        
                        # Write to file
                        dest_path = output_dir / filename
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        dest_path.write_text(file_content, encoding='utf-8')
                        
                        self.files_created.append(dest_path)
                        self.block_count += 1
                        print(f"✓ Created: {dest_path}")
                        
                        i = content_end + 1
                        continue
            
            i += 1
        
        print(f"\n✅ Created {self.block_count} files in {output_dir}")
        return self.block_count
    
    def build_from_text(self, text: str, output_dir: str = "project") -> int:
        """Build project from text containing code blocks."""
        temp_path = Path("/tmp/metafile_temp.txt")
        temp_path.write_text(text, encoding='utf-8')
        try:
            return self.build_from_file(str(temp_path), output_dir)
        finally:
            if temp_path.exists():
                temp_path.unlink()

def main():
    if len(sys.argv) < 2:
        print("Usage: python project_builder.py <metafile_path> [output_dir]")
        sys.exit(1)
    
    builder = ProjectBuilder()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    builder.build_from_file(sys.argv[1], output_dir)

if __name__ == "__main__":
    main()
