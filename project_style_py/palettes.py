import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Sequence
from .config import get_project_palettes

def display_project_palette(palette_name: str):
    """
    Displays a visualization of a named color palette.
    """
    palettes = get_project_palettes()
    if palette_name not in palettes:
        raise ValueError(f"Palette '{palette_name}' not found. Available: {list(palettes.keys())}")

    colors = palettes[palette_name]
    
    color_values = list(colors.values()) if isinstance(colors, dict) else colors
    color_names = list(colors.keys()) if isinstance(colors, dict) else [f"Color {i+1}" for i in range(len(colors))]

    n = len(color_values)
    fig, ax = plt.subplots(1, 1, figsize=(n * 1.5, 2))
    
    for i, (color, name) in enumerate(zip(color_values, color_names)):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.text(i + 0.5, 0.5, f"{name}\n{color}", color='white' if sum(plt.colors.to_rgb(color)) < 1.5 else 'black',
                ha='center', va='center', fontsize=10, weight='bold')

    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    fig.suptitle(f"Project Palette: '{palette_name}'", fontsize=14)
    plt.show()

def get_palette(palette_name: str) -> List[str]:
    """
    Retrieves a named palette as a simple list of hex codes.
    """
    palettes = get_project_palettes()
    if palette_name not in palettes:
        raise ValueError(f"Palette '{palette_name}' not found. Available: {list(palettes.keys())}")

    colors = palettes[palette_name]
    
    if isinstance(colors, dict):
        return list(colors.values())
    elif isinstance(colors, list):
        return colors
    else:
        raise TypeError(f"Palette '{palette_name}' is not a valid list or dictionary.")

def get_mapped_palette(
    obs_column: pd.Series, 
    palette_name: str
) -> Dict[str, str]:
    """
    Creates a dictionary mapping unique observation labels to specific colors
    from a project palette, ensuring consistent color-label associations.

    Args:
        obs_column (pd.Series): Column containing relevant labels in a pandas dataframe
            (e.g., adata.obs['cell_type']).
        palette_name (str): The name of the project palette to use.

    Returns:
        Dict[str, str]: A dictionary mapping labels to hex color codes.
    """
    if pd.api.types.is_categorical_dtype(obs_column):
        categories = obs_column.cat.categories
    else:
        categories = obs_column.unique()

    color_list = get_palette(palette_name)
    
    color_map = {
        category: color_list[i % len(color_list)]
        for i, category in enumerate(categories)
    }
    
    return color_map

