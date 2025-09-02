import os
from .config import load_project_palettes, load_project_themes, available_palettes, available_themes
from .palettes import display_project_palette, get_palette, get_mapped_palette
from .styling import set_project_style

# --- Auto-load default configurations on package import ---
try:
    _RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'resources')
    
    _DEFAULT_PALETTES = os.path.join(_RESOURCE_DIR, 'palettes.yaml')
    _DEFAULT_THEMES = os.path.join(_RESOURCE_DIR, 'themes.yaml')

    if os.path.exists(_DEFAULT_PALETTES):
        load_project_palettes(_DEFAULT_PALETTES)
    else:
        print(f"Warning: Default palettes.yaml not found from {_DEFAULT_PALETTES}")

    if os.path.exists(_DEFAULT_THEMES):
        load_project_themes(_DEFAULT_THEMES)
    else:
        print(f"Warning: Default themes.yaml not found from {_DEFAULT_THEMES}")

except Exception as e:
    print(f"Error during project_style_py initialization: {e}")


# --- Expose public functions for easy access ---
__all__ = [
    'load_project_palettes',
    'load_project_themes',
    'display_project_palette',
    'get_palette',
    'get_mapped_palette',
    'set_project_style',
    'available_palettes',
    'available_themes',
]

