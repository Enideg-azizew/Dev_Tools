#!/usr/bin/env python3
"""
Environment configuration management.
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    """Manage configuration from .env and config files."""
    
    def __init__(self, env_path: Optional[Path] = None):
        self.env_path = env_path or Path.cwd() / '.env'
        if self.env_path.exists():
            load_dotenv(self.env_path)
        
        self._config_cache = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return os.getenv(key, default)
    
    def get_required(self, key: str) -> str:
        """Get a required configuration value."""
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required configuration key '{key}' not found")
        return value
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value."""
        try:
            return int(self.get(key, default))
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value."""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def load_json(self, path: Path) -> Dict[str, Any]:
        """Load a JSON configuration file."""
        if not path.exists():
            return {}
        
        with open(path, 'r') as f:
            return json.load(f)
    
    def save_json(self, path: Path, data: Dict[str, Any]) -> None:
        """Save data to a JSON configuration file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def from_file(cls, path: Path) -> 'ConfigManager':
        """Create a ConfigManager from a specific .env file."""
        return cls(path)

# Global instance
config = ConfigManager()
