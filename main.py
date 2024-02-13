from miscellaneous import utilities
import matplotlib.pyplot as plt
import networkx as nx
from scipy.io import netcdf
import numpy as np


# ---------------------------------------------
# GRID
# ---------------------------------------------

# CONSTANTS
VISUALIZE_GRID = True
RECOMPUTE_COAST_NODES = False

# Load data grid from .grd file
secA, secB = utilities.read_grid("./data/grid/basbathy_50m_depth_20231010.grd")

if RECOMPUTE_COAST_NODES:
    # Get and save coast nodes
    coast_nodes = utilities.get_coast(secA, secB)
    np.save("./data/grid/coast_nodes.npy", np.array(coast_nodes))
else:
    # Load coast nodes from memory
    coast_nodes = np.load("./data/grid/coast_nodes.npy")
coord_coast_nodes = utilities.get_grid_from_coast_nodes(secA, coast_nodes)

if VISUALIZE_GRID:
    # Visualize grid
    for i in range(len(secB["id"])):
        if i % 1000 == 0:
            p = i / len(secB["id"]) * 100
            print(f"Generating plot... ({p:0.2f}%).", end="\r")
        G = utilities.get_triangular_connections((secB["vA"][i], secB["vB"][i], secB["vC"][i]), secA)
        plt.plot(G[0], G[1], 'b-')
    plt.scatter(coord_coast_nodes[0], coord_coast_nodes[1], s=13, c="r")
    plt.title("Visualization of the data grid")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.grid()
    plt.show()



# ---------------------------------------------
# SHYFEM Simulation
# ---------------------------------------------    

# CONSTANTS
MONTH = 0 # Available months: from 0 to 7

# Load SHYFEM simulations from .nc file
with netcdf.NetCDFFile(f"./data/SHYFEM/na-bcunige1_basGebco_000{MONTH}.ous.nc", "r") as f:
    print(f.variables.keys())
    print(f.variables["water_level"].shape)