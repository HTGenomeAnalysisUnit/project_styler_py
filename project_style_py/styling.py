import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm
from typing import Optional
from .config import get_project_themes, get_project_palettes

def _register_continuous_cmaps():
    """Create and register continuous colormaps from loaded palettes."""
    try:
        palettes = get_project_palettes()
        for name, colors in palettes.items():
            cmap_name = f"project_{name}"
            color_list = list(colors.values()) if isinstance(colors, dict) else colors
            
            cmap = LinearSegmentedColormap.from_list(cmap_name, color_list)
            
            cm.ColormapRegistry.register(cmap=cmap)
            cm.ColormapRegistry.register(cmap=cmap.reversed(), name=f"{cmap_name}_r")
            
    except ValueError:
        pass # Palettes not yet loaded, which is fine.

def set_project_style(theme_name: str = "default", **kwargs):
    """
    Applies a predefined theme to matplotlib and seaborn and registers colormaps.

    Args:
        theme_name (str): The name of the theme to apply from the loaded config.
        **kwargs: Additional rcParams to override or add on the fly.
    """
    themes = get_project_themes()
    if theme_name not in themes:
        raise ValueError(f"Theme '{theme_name}' not found. Available: {list(themes.keys())}")
    
    style_dict = themes[theme_name].copy()
    style_dict.update(kwargs)
    
    plt.rcParams.update(style_dict)
    
    try:
        palettes = get_project_palettes()
        default_palette = next(iter(palettes.values()))
        sns.set_palette(list(default_palette.values()) if isinstance(default_palette, dict) else default_palette)
    except (StopIteration, ValueError):
        print("Warning: No color palettes loaded. Seaborn palette not set.")

    _register_continuous_cmaps()
    print(f"Project style '{theme_name}' applied. Continuous colormaps registered.")

