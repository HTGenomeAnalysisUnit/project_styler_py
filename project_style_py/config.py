import yaml
import requests
from typing import Dict, Any

# Global dictionaries to store the loaded configurations
_PALETTES: Dict[str, Any] = {}
_THEMES: Dict[str, Any] = {}

def load_project_palettes(path: str):
    """Loads color palettes from a local or remote YAML file."""
    global _PALETTES
    try:
        if path.startswith(('http://', 'https://')):
            response = requests.get(path)
            response.raise_for_status()
            config_text = response.text
        else:
            with open(path, 'r') as f:
                config_text = f.read()
        
        palettes = yaml.safe_load(config_text)
        _PALETTES.clear()
        _PALETTES.update(palettes)
        print(f"Successfully loaded palettes from: {path}")
    except Exception as e:
        print(f"Error loading palettes from {path}: {e}")

def load_project_themes(path: str):
    """Loads plot themes from a local or remote YAML file."""
    global _THEMES
    try:
        if path.startswith(('http://', 'https://')):
            response = requests.get(path)
            response.raise_for_status()
            config_text = response.text
        else:
            with open(path, 'r') as f:
                config_text = f.read()
                
        themes = yaml.safe_load(config_text)
        _THEMES.clear()
        _THEMES.update(themes)
        print(f"Successfully loaded themes from: {path}")
    except Exception as e:
        print(f"Error loading themes from {path}: {e}")

def get_project_palettes() -> Dict[str, Any]:
    """Returns the currently loaded color palettes."""
    if not _PALETTES:
        raise ValueError("No palettes have been loaded.")
    return _PALETTES

def get_project_themes() -> Dict[str, Any]:
    """Returns the currently loaded plot themes."""
    if not _THEMES:
        raise ValueError("No themes have been loaded.")
    return _THEMES
