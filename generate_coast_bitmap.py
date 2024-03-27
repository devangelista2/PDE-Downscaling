import matplotlib.pyplot as plt
import numpy as np

from miscellaneous import utilities

# ---------------------------------------------
# GRID
# ---------------------------------------------

# CONSTANTS
VISUALIZE_GRID = True
VISUALIZE_COAST_NODES = True
COMPUTE_COAST_NODES = False

MAX_SHAPE = 256

# Load data grid from .grd file
secA, secB = utilities.read_grid("./data/grid/basbathy_50m_depth_20231010.grd")

# Get values from grid
latitude = np.array(secA["latitude"])
longitude = np.array(secA["longitude"])

# Define grid -> image parameters
lat_m, lat_M = latitude.min(), latitude.max()
lon_m, lon_M = longitude.min(), longitude.max()

delta_x = (lat_M - lat_m) / MAX_SHAPE
delta_y = (lon_M - lon_m) / MAX_SHAPE
delta = max(delta_x, delta_y)
print(f"Latitude: {lat_m, lat_M}.")
print(f"Longitude: {lon_m, lon_M}.")
print(f"Res: {delta}.")

nx, ny = int(np.ceil((lat_M - lat_m) / delta)), int(np.ceil((lon_M - lon_m) / delta))

# Load list of coast nodes
coast_nodes = np.load("./mask/coast_nodes.npy")

# Generate coast mask
coast_mask = np.zeros((nx, ny))
for idx in coast_nodes:
    id_lat, id_lon = latitude[idx - 1], longitude[idx - 1]
    i, j = int((id_lat - lat_m) // delta) - 1, int((id_lon - lon_m) // delta) - 1

    # Put into the mask
    coast_mask[i, j] = 1
# Flip mask
coast_mask = np.flipud(coast_mask)


# Get sea_mask
sea_mask = np.load("./mask/sea_mask.npy")
sea_mask_or = sea_mask + coast_mask - sea_mask * coast_mask

# Save
np.save("./mask/coast_mask.npy", coast_mask)
np.save("./mask/coast_mask_or.npy", sea_mask_or)

# Visualization
plt.imshow(sea_mask_or, cmap="gray")
plt.show()
