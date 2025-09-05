import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colormaps as cm
from matplotlib import font_manager
from typing import Optional
from .config import get_project_themes, get_project_palettes
import requests
import zipfile
import io
import os
from urllib.parse import quote_plus

def _download_and_register_font(font_name: str):
    """
    Checks if a font is available to matplotlib, and if not, attempts to
    download it from Google Fonts and register it.
    """
    try:
        # 1. Check if font is already known to matplotlib
        font_manager.findfont(font_name, fallback_to_default=False)
        # print(f"Font '{font_name}' is already available.")
        return
    except ValueError:
        print(f"Font '{font_name}' not found. Attempting to download from Google Fonts...")

    # 2. Construct URL and download
    try:
        url_name = quote_plus(font_name)
        url = f"https://fonts.google.com/download?family={url_name}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"Warning: Could not download '{font_name}' from Google Fonts. Please install it manually.")
        return

    # 3. Unzip and find the regular TTF file
    try:
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        font_filename = None
        # Try to find a 'Regular' or the first TTF file
        for name in zip_file.namelist():
            if 'regular' in name.lower() and name.endswith('.ttf'):
                font_filename = name
                break
        if not font_filename:
             for name in zip_file.namelist():
                if name.endswith('.ttf'):
                    font_filename = name
                    break
        
        if not font_filename:
            print(f"Warning: Could not find a .ttf file for '{font_name}' in the downloaded archive.")
            return

        # 4. Save the font file to matplotlib's cache directory
        font_data = zip_file.read(font_filename)
        font_cache_dir = font_manager.get_font_cache_dir()
        dest_path = os.path.join(font_cache_dir, os.path.basename(font_filename))
        
        with open(dest_path, "wb") as f_obj:
            f_obj.write(font_data)

        # 5. Rebuild matplotlib's font cache
        print("Rebuilding font cache. This may take a moment...")
        font_manager._load_fontmanager(try_read_cache=False)
        print(f"Successfully downloaded and registered '{font_name}'.")

    except Exception as e:
        print(f"Warning: Failed to install font '{font_name}'. Please install it manually. Error: {e}")

def _register_continuous_cmaps():
    """Create and register continuous colormaps from loaded palettes."""
    try:
        palettes = get_project_palettes()
        for name, colors in palettes.items():
            cmap_name = f"project_{name}"
            color_list = list(colors.values()) if isinstance(colors, dict) else colors
            
            cmap = LinearSegmentedColormap.from_list(cmap_name, color_list)
            
            cm.register(cmap)
            cm.register(cmap.reversed())
            
    except ValueError:
        pass # Palettes not yet loaded, which is fine.

def set_project_style(theme_name: str = "default", clean_style: bool = True, **kwargs):
    """
    Applies a predefined theme to matplotlib and seaborn and registers colormaps.

    Args:
        theme_name (str): The name of the theme to apply from the loaded config.
        **kwargs: Additional rcParams to override or add on the fly.
    """
    themes = get_project_themes()
    if theme_name not in themes:
        raise ValueError(f"Theme '{theme_name}' not found. Available: {list(themes.keys())}")
    theme_config = themes[theme_name]

    # Reset rcParams to default before applying new theme
    if clean_style: plt.rcdefaults()

    # If fonts is present in themes, copy this to a separate variable and remove it
    font_dict = theme_config.pop('fonts', {})

    style_dict = theme_config.copy()

    # If font_dict is not empty, register the fonts in style_dict under sans-serif family
    # The first font is added in position zero so it is used as the default
    if font_dict:
        style_dict['font.family'] = 'sans-serif'
        style_dict['font.sans-serif'] = []
        for font_name, font_paths in font_dict.items():
            style_dict['font.sans-serif'].append(font_name)

    style_dict.update(kwargs)
    plt.rcParams.update(style_dict)

    try:
        palettes = get_project_palettes()
        default_palette = palettes.get('default', next(iter(palettes.values())))
        sns.set_palette(list(default_palette.values()) if isinstance(default_palette, dict) else default_palette)
    except (StopIteration, ValueError):
        print("Warning: No color palettes loaded. Seaborn palette not set.")

    _register_continuous_cmaps()
    print(f"Project style '{theme_name}' applied. Continuous colormaps registered.")

    advanced_settings = theme_config.get("advanced_grid_style", {})

    def apply_advanced_style(ax):
        """
        Applies advanced, per-axis styling defined in the theme's
        'advanced_grid_style' block.

        Args:
            ax (matplotlib.axes.Axes): The axis object to style.
        """
        if not isinstance(ax, plt.Axes):
            raise TypeError("Argument must be a matplotlib Axes object.")

        if not advanced_settings:
            return

        # Apply major grid styles if defined
        if 'major' in advanced_settings:
            ax.grid(which='major', **advanced_settings['major'])

        # Apply minor grid styles if defined
        if 'minor' in advanced_settings:
            ax.minorticks_on()  # Ensure minor ticks are visible to draw grid on
            ax.grid(which='minor', **advanced_settings['minor'])
    print("--> Advanced styling function returned. Apply it to your axes object (e.g., style_func(ax)).")

    return apply_advanced_style

