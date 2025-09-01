# project_style_py: Consistent Plotting Styles for Python

`project_style_py` is a utility package for Python designed to enforce a consistent visual identity across all `matplotlib` and `seaborn` plots generated for a scientific project. By centralizing color palettes and theme definitions in simple, editable `YAML` files, it ensures that every team member produces plots with the same branding.

This package is the Python component of the `projectStyler` ecosystem, with a sister package, `projectStyleR`, available for R users.

## Core Features

- Centralized Configuration: Define all color palettes and plot themes in human-readable `YAML` files.
- Matplotlib & Seaborn Integration: A simple function to set global styles (`rcParams`) and register colormaps.
- Easy to Use: Apply complex styling with simple, one-line functions.
- Dynamic Loading: Load configurations from a local file or a remote URL (e.g., a raw GitHub file), allowing for project-wide updates without changing code.
- Flexible Palettes: Supports both discrete and continuous color scales, automatically registering palettes as `matplotlib` colormaps.
- `scanpy` Integration: Specialized functions for applying palettes to UMAP plots, including stable color-to-label mapping.

## 📦 Installation

You can install the Python package directly from its GitHub repository using pip.

```bash
pip install git+https://github.com/your-organization/project_style_py.git
```

## 🐍 Usage

### 1. Applying a Project Style

The `set_project_style()` function configures matplotlib's `rcParams` and registers your custom colormaps.

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import project_style_py as scp

# Make a demo dataset of random numbers
np.random.seed(42)
data = {
    "flipper_length_mm": np.random.rand(100) * 200,
    "bill_length_mm": np.random.rand(100) * 100,
    "species": np.random.choice(["Adelie", "Chinstrap", "Gentoo"], 100)
}
penguins = pd.DataFrame(data)

sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm")
plt.title("Plot with 'default' Theme")
plt.show()

# Apply the 'default' project style
scp.set_project_style("default")

# You can also override specific parameters on the fly
scp.set_project_style("publication", **{'axes.labelsize': 14})
```

### 2. Using Color Palettes

**Continuous Scales (Colormaps)**

All palettes are automatically registered as `matplotlib` colormaps (e.g., `project_primary`, `project_npg_continuous`).

```python
import numpy as np
data = np.random.rand(10, 12)

# Use a custom continuous colormap
sns.heatmap(data, cmap="project_npg_continuous")
plt.title("Heatmap with a Project Colormap")
plt.show()
```

**Load a discrete scale (scanpy UMAP example)**

If you need to load a discrete scale to pass to your plotting function, you can do this using `get_palette()`. You can also load a precise label to color mapping using `get_mapped_palette()`.

Example

```python
import project_style_py as scp
import numpy as np

# Set the discrete color scale manually
sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species", palette=scp.get_palette("npg"))
```

This is useful for example to set specific colors when plotting UMAP in `scanpy`.

```python
import scanpy as sc
import project_style_py as scp

# Assume 'adata' is your AnnData object
adata = sc.datasets.pbmc3k_processed()

# Option 1: Apply a palette sequentially
sc.pl.umap(adata, color="louvain", palette=scp.get_palette("npg"))

# Option 2 (Recommended): Create a stable color-to-label map
# This ensures 'CD4 T-cell' is ALWAYS the same color in every plot.
cell_type_palette = scp.get_mapped_palette(adata.obs['celltype'], "celltype")
sc.pl.umap(adata, color="celltype", palette=cell_type_palette)
```

### 3. Viewing Palettes

Visualize any available palette.

```python
scp.display_project_palette("vibrant")
```

### 4. Custom Configurations

Point the package to your own configuration files.

```python
# Load palettes from a local file
scp.load_project_palettes("path/to/my_palettes.yaml")

# Load themes from a raw GitHub URL
scp.load_project_themes("https://raw.githubusercontent.com/user/repo/main/configs/project_themes.yaml")

# Re-apply the style to make the new settings take effect
scp.set_project_style("default")
```

## ⚙️ Configuration Files

The `palettes.yaml` and `themes.yaml` files are the heart of this system. 

To achieve consistent styling across your project you can either 

- fork this repository and editing the files in the `project_style_py/resources` directory to match your project's brand identity and then install the package from your forked repository to share the new defaults with your team.
- create dedicated `palettes.yaml` and `themes.yaml` files for your project and ideally host them in the project GitHub repository. Then configure your scripts to always load these files from the centralized project source using the `load_project_palettes()` and `load_project_themes()` functions before setting the style with `set_project_style()`.

## 📝 License

This project is licensed under the MIT License.