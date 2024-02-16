from miscellaneous import utilities
import matplotlib.pyplot as plt
from scipy.io import netcdf
import numpy as np

# ---------------------------------------------
# SHYFEM Simulation
# ---------------------------------------------    

# CONSTANTS
MONTH = 0 # Available months: from 0 to 7

# Load SHYFEM simulations from .nc file
with netcdf.NetCDFFile(f"./data/SHYFEM/na-bcunige1_basGebco_000{MONTH}.ous.nc", "r") as f:
    latitude = f.variables["latitude"][:]
    longitude = f.variables["longitude"][:]

    water_level = f.variables["water_level"][:]

    # print(f.variables.keys())

# cropped_latitude_id = np.where((latitude > 45.50) & (latitude < 45.74))
# cropped_longitude_id = np.where((longitude > 12.93) & (longitude < 13.17))
# cropped_id = np.intersect1d(cropped_latitude_id, cropped_longitude_id)
# 
# cropped_water_level = water_level[:, cropped_id]
# print(cropped_water_level.shape)
# print(f"Min: {cropped_water_level[0].min()}, Max:{cropped_water_level[0].max()}, Std: {cropped_water_level[0].std()}.")
# 
# plt.plot(cropped_water_level.min(axis=1))
# plt.plot(cropped_water_level.max(axis=1))
# plt.legend(["min", "max"])
# plt.grid()
# plt.show()

lat_m, lat_M = latitude.min(), latitude.max()
lon_m, lon_M = longitude.min(), longitude.max()

delta_x = (lat_M - lat_m) / 256
delta_y = (lon_M - lon_m) / 256
delta = max(delta_x, delta_y)
print(f"{delta=:0.4f}.")

nx, ny = int(np.ceil((lat_M - lat_m)/delta)), int(np.ceil((lon_M - lon_m)/delta))

coarse_image = np.zeros((nx, ny, 3))
for i in range(nx):
    for j in range(ny):
        cropped_latitude_id = np.where((latitude > lat_m + i*delta) & (latitude < lat_m + (i+1)*delta))
        cropped_longitude_id = np.where((longitude > lon_m + j*delta) & (longitude < lon_m + (j+1)*delta))
        cropped_id = np.intersect1d(cropped_latitude_id, cropped_longitude_id)

        if len(cropped_id) == 0:
            coarse_image[i, j, 0] = 0
            coarse_image[i, j, 1] = 0
            coarse_image[i, j, 2] = 0
        
        else:
            cropped_water_level = water_level[501, cropped_id]

            coarse_image[i, j, 0] = cropped_water_level.mean()
            coarse_image[i, j, 1] = cropped_water_level.max() - cropped_water_level.min()
            coarse_image[i, j, 2] = cropped_water_level.std()

    print(f"{i=}")

coarse_image = np.flipud(coarse_image)

plt.subplot(2, 2, 1)
plt.imshow(coarse_image[:, :, 0], cmap='viridis')
plt.title("Image")
plt.colorbar()
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(coarse_image[:, :, 1], cmap='viridis')
plt.title("Max - Min")
plt.colorbar()
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(coarse_image[:, :, 2], cmap='viridis')
plt.title("Std")
plt.colorbar()
plt.axis('off')
plt.show()