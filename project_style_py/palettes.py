import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors
from typing import Dict, List, Union, Sequence
from .config import get_project_palettes

def get_palette(palette_name: str) -> List[str]:
    """
    Retrieves a project color palette formatted as a list of colors.

    Args:
        palette_name: The name of the palette to retrieve.

    Returns:
        A list of hex color codes.
    """
    palettes = get_project_palettes()
    if palette_name not in palettes:
        available = ", ".join(palettes.keys())
        raise ValueError(f"Palette '{palette_name}' not found. Available palettes are: {available}")
    
    colors = palettes[palette_name]
    return colors if isinstance(colors, list) else list(colors.values())

def get_mapped_palette(palette_name: str, data_labels: Sequence = [], unseen_color: str = "#808080") -> Dict[str, str]:
    """
    Creates a stable mapping between data labels and colors from a palette.

    This ensures that a specific label (e.g., a cell type) is always assigned
    the same color, regardless of its order in the data.

    When the palette is already a named palette it returns this one unchanged.

    Args:
        data_labels: A sequence (like a pandas Series or list) of the labels to map.
        palette_name: The name of the project palette to use for mapping.

    Returns:
        A dictionary mapping each unique label to a hex color code.
    """
    palettes = get_project_palettes()
    data_labels_set = set(data_labels)
    if palette_name not in palettes:
        available = ", ".join(palettes.keys())
        raise ValueError(f"Palette '{palette_name}' not found. Available palettes are: {available}")
    
    if isinstance(palettes[palette_name], dict):
        # If the palette is a named palette load the dict 
        palette = palettes[palette_name]
        # Assign to all data_labels not in the palette the unseen_color
        for label in data_labels_set:
            if label not in palette:
                palette[label] = unseen_color
        return palette

    if len(data_labels_set) == 0:
        raise ValueError("data_labels must contain at least one label for mapping when the palette is a sequence of colors.")
    
    unique_labels = sorted(list(data_labels_set))
    palette_values = list(palettes[palette_name].values())

    # Create a stable mapping using modulo arithmetic for color cycling
    return {label: palette_values[i % len(palette_values)] for i, label in enumerate(unique_labels)}

def display_project_palette(palette_name: str):
    """
    Displays a color palette as a clean bar plot of color swatches.

    Args:
        palette_name: The name of the palette to display.
    """
    palettes = get_project_palettes()
    if palette_name not in palettes:
        available = ", ".join(palettes.keys())
        raise ValueError(f"Palette '{palette_name}' not found. Available palettes are: {available}")

    colors = palettes[palette_name]
    
    palette_data = colors if isinstance(colors, list) else list(colors.values())
    palette_names = [""] * len(palette_data) if isinstance(colors, list) else list(colors.keys())

    fig, ax = plt.subplots(figsize=(len(palette_data) * 1.5, 2.5))
    
    ax.bar(
        x=range(len(palette_data)),
        height=[1] * len(palette_data),
        color=palette_data,
        tick_label=palette_names,
        width=1
    )

    # Add color hex codes as text on the bars
    for i, color in enumerate(palette_data):
        # Determine text color (black or white) based on background brightness
        r, g, b = mcolors.to_rgb(color)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = 'white' if luminance < 0.5 else 'black'
        ax.text(i, 0.5, color, ha='center', va='center', color=text_color, fontsize=10, weight='bold')

    ax.set_xticks(range(len(palette_data)))
    ax.set_xticklabels(palette_names, rotation=45, ha="right")
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(-0.5, len(palette_data) - 0.5)
    ax.set_ylim(0, 1)
    
    # Remove frame/spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(f"Palette: {palette_name}", pad=20, fontsize=14, weight='bold')
    plt.tight_layout()
    plt.show()

