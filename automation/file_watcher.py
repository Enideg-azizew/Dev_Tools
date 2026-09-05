#!/usr/bin/env python3
"""
Watch and synchronize directory changes.
Based on watch_dog.py.
"""
import os
import time
import shutil
import filecmp
from pathlib import Path
from typing import Set, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SyncEventHandler(FileSystemEventHandler):
    """Handles filesystem events and synchronizes changes."""
    
    def __init__(self, source_dir: Path, dest_dir: Path, 
                 ignored_dirs: Set[str] = None):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.ignored_dirs = ignored_dirs or {
            '.git', '__pycache__', '.idea', '.DS_Store', 'node_modules'
        }
    
    def get_relative_path(self, src_path: str) -> str:
        """Get relative path from source directory."""
        return os.path.relpath(src_path, str(self.source_dir))
    
    def get_destination_path(self, src_path: str) -> Path:
        """Get corresponding path in destination directory."""
        rel_path = self.get_relative_path(src_path)
        return self.dest_dir / rel_path
    
    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        path_parts = path.split(os.sep)
        return any(part in self.ignored_dirs for part in path_parts)
    
    def sync_file(self, src_path: str) -> None:
        """Synchronize a single file."""
        if self.should_ignore(src_path):
            return
        
        dst_path = self.get_destination_path(src_path)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file needs copying
        if not dst_path.exists() or not filecmp.cmp(src_path, str(dst_path), shallow=False):
            shutil.copy2(src_path, dst_path)
            print(f"Synced: {self.get_relative_path(src_path)}")
    
    def sync_directory(self, src_path: str) -> None:
        """Synchronize an entire directory."""
        if self.should_ignore(src_path):
            return
        
        dst_path = self.get_destination_path(src_path)
        if not dst_path.exists():
            shutil.copytree(src_path, dst_path)
            print(f"Created directory: {self.get_relative_path(src_path)}")
    
    def remove_in_dest(self, src_path: str) -> None:
        """Remove corresponding path in destination directory."""
        dst_path = self.get_destination_path(src_path)
        if dst_path.exists():
            if dst_path.is_dir():
                shutil.rmtree(dst_path)
            else:
                dst_path.unlink()
            print(f"Removed: {self.get_relative_path(src_path)}")
    
    def on_modified(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            self.sync_directory(event.src_path)
        else:
            self.sync_file(event.src_path)
    
    def on_deleted(self, event):
        self.remove_in_dest(event.src_path)
    
    def on_moved(self, event):
        self.remove_in_dest(event.src_path)
        if event.is_directory:
            self.sync_directory(event.dest_path)
        else:
            self.sync_file(event.dest_path)

class FileWatcher:
    """Monitor directory for changes and sync to destination."""
    
    def __init__(self, source_dir: str, dest_dir: str):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.observer = None
        self.event_handler = None
    
    def initial_sync(self) -> None:
        """Perform initial synchronization."""
        print("Performing initial synchronization...")
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a temporary handler for initial sync
        handler = SyncEventHandler(self.source_dir, self.dest_dir)
        
        for root, dirs, files in os.walk(self.source_dir):
            root = Path(root)
            # Filter ignored directories
            dirs[:] = [d for d in dirs if not handler.should_ignore(str(root / d))]
            
            for dir_name in dirs:
                src_dir = root / dir_name
                if handler.should_ignore(str(src_dir)):
                    continue
                handler.sync_directory(str(src_dir))
            
            for file_name in files:
                src_file = root / file_name
                if handler.should_ignore(str(src_file)):
                    continue
                handler.sync_file(str(src_file))
        
        print("Initial sync complete.")
    
    def start(self) -> None:
        """Start watching for changes."""
        self.initial_sync()
        
        self.event_handler = SyncEventHandler(self.source_dir, self.dest_dir)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, str(self.source_dir), recursive=True)
        self.observer.start()
        
        print(f"Monitoring {self.source_dir} for changes. Press Ctrl+C to stop.")
    
    def stop(self) -> None:
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
    
    def run(self) -> None:
        """Run the watcher."""
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            print("\nStopped watching.")

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python file_watcher.py <source_dir> <dest_dir>")
        sys.exit(1)
    
    watcher = FileWatcher(sys.argv[1], sys.argv[2])
    watcher.run()

if __name__ == "__main__":
    main()
