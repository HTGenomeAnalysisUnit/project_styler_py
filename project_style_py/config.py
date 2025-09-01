import yaml
import requests
import importlib.resources
import pathlib
from typing import Dict, Any

# Global dictionaries to store the loaded configurations
_PALETTES: Dict[str, Any] = {}
_THEMES: Dict[str, Any] = {}

def load_default_configs():
    """Loads the default YAML files bundled with the package."""
    global _PALETTES, _THEMES
    try:
        with importlib.resources.files('project_style_py').joinpath('resources/palettes.yaml').open('r') as f:
            _PALETTES = yaml.safe_load(f)
        with importlib.resources.files('project_style_py').joinpath('resources/themes.yaml').open('r') as f:
            _THEMES = yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError):
        print("Warning: Could not load default palette or theme configurations.")

def _fetch_config_content(path: str, github_pat: str = None) -> str:
    """Internal helper to fetch content from a local path or a URL."""
    if path.startswith(('http://', 'https://')):
        headers = {}
        if "raw.githubusercontent.com" in path and github_pat:
            headers["Authorization"] = f"token {github_pat}"
            print("Using GitHub PAT for authenticated access.")
        try:
            response = requests.get(path, headers=headers)
            response.raise_for_status()  # Raises an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            raise IOError(f"Failed to fetch remote configuration from {path}: {e}")
    else:
        # It's a local file path
        local_path = pathlib.Path(path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local configuration file not found at: {path}")
        return local_path.read_text()

def load_project_palettes(path: str, github_pat: str = None):
    """
    Load project color palettes from a local YAML file or a URL.
    
    Args:
        path: A local file path or a URL to a YAML file.
        github_pat: A GitHub PAT for accessing private repositories.
    """
    global _PALETTES
    try:
        content = _fetch_config_content(path, github_pat)
        _PALETTES = yaml.safe_load(content)
        print(f"Successfully loaded palettes from: {path}")
    except (IOError, yaml.YAMLError) as e:
        raise RuntimeError(f"Failed to load palettes: {e}")

def load_project_themes(path: str, github_pat: str = None):
    """
    Load project plot themes from a local YAML file or a URL.

    Args:
        path: A local file path or a URL to a YAML file.
        github_pat: A GitHub PAT for accessing private repositories.
    """
    global _THEMES
    try:
        content = _fetch_config_content(path, github_pat)
        _THEMES = yaml.safe_load(content)
        print(f"Successfully loaded themes from: {path}")
    except (IOError, yaml.YAMLError) as e:
        raise RuntimeError(f"Failed to load themes: {e}")
    
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
