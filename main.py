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
    print(f.variables.keys())
    print(f.variables["water_level"].shape)