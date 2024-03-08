from miscellaneous import utilities
import matplotlib.pyplot as plt
from scipy.io import netcdf
import numpy as np

# ---------------------------------------------
# SHYFEM Simulation
# ---------------------------------------------    

# CONSTANTS
MONTH = 0 # Available months: from 0 to 7
HOUR = 1  # From 0 to 719

MAX_SHAPE = 256 # Maximum shape of the discrete image

GENERATE_MASK = False    # WARNING: Take some time...
GENERATE_MEAN_SL = True

VISUALIZE = True

# Load SHYFEM simulations from .nc file
with netcdf.NetCDFFile(f"./data/SHYFEM/na-bcunige1_basGebco_000{MONTH}.ous.nc", "r") as f:
    latitude = f.variables["latitude"][:]
    longitude = f.variables["longitude"][:]

    u_velocity = f.variables["u_velocity"][:]
    v_velocity = f.variables["v_velocity"][:]
    water_level = f.variables["water_level"][:]

if GENERATE_MEAN_SL:
    # Generate (coarse) image from the grid
    mean_SL = utilities.grid_to_image(latitude, longitude, QOI=water_level,
                                         hour=HOUR, max_shape=MAX_SHAPE, mode='mean')
    
    # Save the generated mask
    np.save("./data/grid/mean_SL.npy", mean_SL)
else:
    # Load sea mask
    mean_SL = np.load("./data/grid/mean_SL.npy")

# Get the shape
nx, ny = mean_SL.shape
print(f"Shape of x: {mean_SL.shape}.")

if GENERATE_MASK:
    # Generate sea mask
    sea_mask = utilities.grid_to_mask(grid_path="./data/grid/basbathy_50m_depth_20231010.grd",
                                    max_shape=MAX_SHAPE)
    
    # Save the generated mask
    np.save("./data/grid/sea_mask.npy", sea_mask)
else:
    # Load sea mask
    sea_mask = np.load("./data/grid/sea_mask.npy")

def find_closest_nonzero(matrix, zero_coords):
    nonzero_coords = np.transpose(np.nonzero(matrix))
    distances = np.linalg.norm(nonzero_coords - zero_coords, axis=1)
    closest_nonzero_index = np.argmin(distances)
    closest_nonzero_coords = tuple(nonzero_coords[closest_nonzero_index])
    return closest_nonzero_coords

# Interpolate zero-valued pixels inside the mask
nonzero_coords = np.transpose(np.nonzero(mean_SL))
for i in range(nx):
    for j in range(ny):
        x = mean_SL[i, j]

        # Interpolate only if its value is 0
        if x < 1e-10 and sea_mask[i, j] == 1:
            distances = np.linalg.norm(nonzero_coords - np.array([[i, j]]), axis=1)
            closest_indices = np.argsort(distances)[:4]
            closest_coordinates = [tuple(nonzero_coords[i]) for i in closest_indices]

            temp = 0
            for s in range(len(closest_coordinates)):
                temp += mean_SL[closest_coordinates[s]]
            mean_SL[i, j] = temp / len(closest_coordinates)

if VISUALIZE:
    # Visualize the result
    plt.imshow(mean_SL, cmap='viridis')
    plt.title("Mean Sea Level")
    plt.tight_layout()
    plt.savefig(f'./results/mean_hour_{HOUR}.png', dpi=350)
    plt.colorbar()
    plt.show()

    plt.imshow(sea_mask, cmap='gray')
    plt.savefig('./results/mask.png', dpi=350)
    plt.tight_layout()
    plt.show()