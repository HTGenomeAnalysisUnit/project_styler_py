import yaml
import tempfile
import requests
import importlib.resources
from matplotlib import font_manager
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

def _fetch_binary_content(path: str, github_pat: str = None) -> bytes:
    """Fetches binary content from a local path or a remote URL."""
    if path.startswith(('http://', 'https://')):
        headers = {}
        if ("raw.githubusercontent.com" in path or "github.com" in path) and github_pat:
            headers["Authorization"] = f"token {github_pat}"
            print("Using GitHub PAT for authenticated access.")
        try:
            response = requests.get(path, headers=headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise IOError(f"Failed to fetch remote file from {path}: {e}")
    else:
        local_path = pathlib.Path(path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local file not found at: {path}")
        return local_path.read_bytes()

def _add_font(path: str, github_pat: str = None):
    font_data = _fetch_binary_content(path, github_pat)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as temp_font_file:
        temp_font_file.write(font_data)
        temp_font_path = temp_font_file.name
    print(f"Font saved to temporary file: {temp_font_path}")
    font_manager.fontManager.addfont(temp_font_path)

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

def load_project_themes(path: str, github_pat: str = None, github_pat_fonts: str = None):
    """
    Load project plot themes from a local YAML file or a URL.

    Args:
        path: A local file path or a URL to a YAML file.
        github_pat: A GitHub PAT for accessing private repositories.
    """
    global _THEMES
    try:
        github_pat_fonts = github_pat_fonts or github_pat if github_pat_fonts != "none" else None
        content = _fetch_config_content(path, github_pat)
        _THEMES = yaml.safe_load(content)
        print(f"Successfully loaded themes from: {path}")
        for theme_name, theme_config in _THEMES.items():
            if 'fonts' in theme_config:
                print(f"Loading fonts for theme: {theme_name}")
                # fonts is expected to contain a dictionary font_name: [font_files]
                for font_name, font_paths in theme_config['fonts'].items():
                    for font_path in font_paths:
                        _add_font(font_path, github_pat_fonts)
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

def available_palettes() -> str:
    """ Log a list of available palettes """
    if not _PALETTES:
        return "No palettes available."
    return ", ".join(_PALETTES.keys())

def available_themes() -> str:
    """ Log a list of available themes """
    if not _THEMES:
        return "No themes available."
    return ", ".join(_THEMES.keys())

def inspect_theme(theme_name: str) -> Dict[str, Any]:
    """Returns the configuration dictionary for a specific theme."""
    themes = get_project_themes()
    if theme_name not in themes:
        raise ValueError(f"Theme '{theme_name}' not found. Available: {list(themes.keys())}")
    return themes[theme_name]