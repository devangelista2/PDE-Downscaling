# PDE-Downscaling
This code is related to a project dedicated to the downscaling of the surge components on the Northen Adriatic Sea. The data considered is computed by the SHYFEM algorithm, based on the discretization of the Navier-Stokes equation with Finite Element Methods.

## Usage
To use the code, simply clone the Github repository locally. This can be simply done by the following snippet:

```
git clone https://github.com/devangelista2/PDE-Downscaling.git
cd PDE-Downscaling
```

This is however not sufficient to safetely run the code, since it is necessary to add a `data` folder, containing the data. In particular, it is required to create a folder, named `data`, containing two subfolders, respectively named `grid` and `SHYFEM`. Then, the file `.grd` has to be placed inside the `grid` folder, while the `.nc` file has to be placed inside the `SHYFEM` folder. After that, the `.py` files can be saftely run.

### Generate the grid with the coast-line
To generate the grid with the coast-line, simply run the `generate_grid.py` file. Note that, at the first execution, it is necessary to generate the coast nodes. This is done by flagging the corresponding variable to `True`. To choose not to visualize the coastline, simply flag as `False` the corresponding variable.

## Requirements
Basic Python libraries for Numerical Analysis are required, such as `numpy`, `matplotlib`, `scipy`, ...

## Authors
- **Davide Evangelista** (davide.evangelista5@unibo.it)
- **Andrea Asperti** (andrea.asperti@unibo.it)
- **Fabio Merizzi** (fabio.merizzi@unibo.it)