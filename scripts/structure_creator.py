#!/usr/bin/env python3
"""
Create empty Django project structure.
Based on dirs.py.
"""
from pathlib import Path

class StructureCreator:
    """Create empty directory structures."""
    
    @staticmethod
    def create_django_structure(base_dir: str = "myproject") -> None:
        """Create Django project directory structure."""
        base = Path(base_dir)
        
        directories = [
            'static/css', 'static/js', 'static/images',
            'templates', 'templates/includes',
            'media', 'media/uploads'
        ]
        
        for d in directories:
            (base / d).mkdir(parents=True, exist_ok=True)
        
        # Empty files
        css_files = ['main.css', 'responsive.css']
        for f in css_files:
            (base / 'static/css' / f).touch()
        
        js_files = ['main.js', 'utils.js']
        for f in js_files:
            (base / 'static/js' / f).touch()
        
        templates = ['base.html', 'index.html', 'about.html']
        for f in templates:
            (base / 'templates' / f).touch()
        
        includes = ['header.html', 'footer.html', 'nav.html']
        for f in includes:
            (base / 'templates/includes' / f).touch()
        
        print(f"Created Django structure at: {base}")

def main():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "myproject"
    StructureCreator.create_django_structure(path)

if __name__ == "__main__":
    main()
