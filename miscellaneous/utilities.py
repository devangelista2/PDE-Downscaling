import numpy as np
import networkx as nx


def read_grid(filename):
    # Initialize dictionaries of data
    secA = {"id": [],
            "latitude": [],
            "longitude": [],
            }
    secB = {"id": [],
            "vA": [],
            "vB": [],
            "vC": [],
            "depth": [],
            }
    
    # Open file from filename
    with open(filename) as f:
        # Iterate through the lines
        for i, line in enumerate(f.readlines()):
            # Check if the line is non-empty
            if line.strip():
                section = int(line.split()[0])
                idx = int(line.split()[1])

                # Append to the right data dictionary
                if section == 1:
                    secA["id"].append(idx)
                    secA["latitude"].append(float(line.split()[-2]))
                    secA["longitude"].append(float(line.split()[-1]))

                if section == 2:
                    secB["id"].append(idx)
                    secB["vA"].append(int(line.split()[4]))
                    secB["vB"].append(int(line.split()[5]))
                    secB["vC"].append(int(line.split()[6]))
                    secB["depth"].append(float(line.split()[7]))

    return secA, secB


def get_triangular_connections(vertices, d):
    # Get vertices from input variable
    vA, vB, vC = vertices

    # Get coordinates of vertices using informations in d
    vAc = np.array([[d["latitude"][vA-1], d["longitude"][vA-1]]]).T
    vBc = np.array([[d["latitude"][vB-1], d["longitude"][vB-1]]]).T
    vCc = np.array([[d["latitude"][vC-1], d["longitude"][vC-1]]]).T

    # Concatenate coordinatees to draw triangles
    return np.hstack((vAc, vBc, vCc, vAc))