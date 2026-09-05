#!/usr/bin/env python3
"""
Reset Django database and migrations.
Based on rmdb.py.
"""
import os
import shutil
from pathlib import Path
from typing import Optional

class DBReinitializer:
    """Reset Django database and migrations."""
    
    @staticmethod
    def reset(project_path: str, app_name: Optional[str] = None) -> None:
        """Reset database and migrations."""
        project = Path(project_path)
        if not project.exists():
            print(f"Project not found: {project_path}")
            return
        
        # Remove database
        db_path = project / "db.sqlite3"
        if db_path.exists():
            db_path.unlink()
            print("Removed database")
        
        # Remove migration files
        for path in project.rglob("*/migrations/*.py"):
            if path.name != "__init__.py":
                path.unlink()
                print(f"Removed: {path}")
        
        # Run migrations
        os.chdir(project)
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")
        
        # Create superuser if requested
        if input("Create superuser? (y/n): ").lower() == 'y':
            os.system("python manage.py createsuperuser")

def main():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    DBReinitializer.reset(path)

if __name__ == "__main__":
    main()
