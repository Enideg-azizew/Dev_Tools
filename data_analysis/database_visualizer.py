#!/usr/bin/env python3
"""
Database structure visualizer.
Based on visual.py.
"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Any

class DatabaseVisualizer:
    """Visualize SQLite database structure."""
    
    @staticmethod
    def get_structure(db_path: str) -> Dict[str, Dict[str, Any]]:
        """Get complete database structure."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        structure = {}
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            structure[table_name] = {'columns': [], 'foreign_keys': [], 'indexes': []}
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                structure[table_name]['columns'].append({
                    'name': col[1],
                    'type': col[2],
                    'nullable': not col[3],
                    'primary_key': bool(col[5])
                })
            
            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            for fk in cursor.fetchall():
                structure[table_name]['foreign_keys'].append({
                    'from': fk[3],
                    'to_table': fk[2],
                    'to_column': fk[4]
                })
            
            # Get indexes
            cursor.execute(f"PRAGMA index_list({table_name});")
            for idx in cursor.fetchall():
                structure[table_name]['indexes'].append({
                    'name': idx[1],
                    'unique': bool(idx[2])
                })
        
        conn.close()
        return structure
    
    @staticmethod
    def print_structure(db_path: str) -> None:
        """Print database structure to console."""
        structure = DatabaseVisualizer.get_structure(db_path)
        
        print(f"Database: {db_path}")
        print("=" * 80)
        
        for table_name, info in structure.items():
            print(f"\nTABLE: {table_name}")
            print("-" * 60)
            print(f"{'Column':<25} {'Type':<15} {'Nullable':<10} {'PK'}")
            print("-" * 60)
            
            for col in info['columns']:
                print(f"{col['name']:<25} {col['type']:<15} {col['nullable']!s:<10} {col['primary_key']!s}")
            
            if info['foreign_keys']:
                print(f"\nForeign Keys:")
                for fk in info['foreign_keys']:
                    print(f"  {fk['from']} -> {fk['to_table']}.{fk['to_column']}")
            
            if info['indexes']:
                print(f"\nIndexes:")
                for idx in info['indexes']:
                    print(f"  {idx['name']} ({'UNIQUE' if idx['unique'] else 'NON-UNIQUE'})")
        
        print("\n" + "=" * 80)

def main():
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "db.sqlite3"
    if not Path(db_path).exists():
        print(f"Database not found: {db_path}")
        sys.exit(1)
    DatabaseVisualizer.print_structure(db_path)

if __name__ == "__main__":
    main()
