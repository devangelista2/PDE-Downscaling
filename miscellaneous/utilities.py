import numpy as np


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

def get_coast(secA, secB):
    # Get the list of nodes
    nodes = secA["id"]

    # For any node...
    coast_nodes = []
    for i in range(len(nodes)):
        node = int(nodes[i])

        # Get (as numpy arrays) the column of the vertices of the triangle
        vA = np.array(secB["vA"])
        vB = np.array(secB["vB"])
        vC = np.array(secB["vC"])

        # Count how many edges contains the considered node.
        count = np.sum(vA == node) + np.sum(vB == node) + np.sum(vC == node)
        
        # A node is on the coast if and only if it is connected to
        # AT MOST 4 edges.
        if count <= 4:
            coast_nodes.append(node)

        # Verbose the percentage of nodes processed
        p = i / (len(nodes)) * 100
        print(f"Computing coast nodes... {p:0.2f}%", end="\r")

    return np.array(coast_nodes)

def get_coordinates_from_nodes(secA, nodes_list):
    r"""
    Takes as input the sectionA dictionary and the array containing a list
    of nodes with shape (n, ), and returns an array of shape (2, n)
    where each column contains the coordinates (latitude and longitude)
    of the corresponding node.
    """
    # Iterate through the nodes
    for i in range(len(nodes_list)):
        node_id = int(nodes_list[i])
        
        # The "-1" appears because the node indices in the .grd file 
        # starts from 1, while Python starts counting from 0. 
        coord = np.array([[secA["latitude"][node_id-1]], [secA["longitude"][node_id-1]]])
        if i == 0:
            coord_arr = coord
        else:
            coord_arr = np.hstack((coord_arr, coord))
    return coord_arr