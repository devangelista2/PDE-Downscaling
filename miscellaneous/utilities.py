import numpy as np


def read_grid(filename):
    # Initialize dictionaries of data
    secA = {
        "id": [],
        "latitude": [],
        "longitude": [],
    }
    secB = {
        "id": [],
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
                    secA["latitude"].append(float(line.split()[-1]))
                    secA["longitude"].append(float(line.split()[-2]))

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
    vAc = np.array([[d["latitude"][vA - 1], d["longitude"][vA - 1]]]).T
    vBc = np.array([[d["latitude"][vB - 1], d["longitude"][vB - 1]]]).T
    vCc = np.array([[d["latitude"][vC - 1], d["longitude"][vC - 1]]]).T

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
        coord = np.array(
            [[secA["latitude"][node_id - 1]], [secA["longitude"][node_id - 1]]]
        )
        if i == 0:
            coord_arr = coord
        else:
            coord_arr = np.hstack((coord_arr, coord))
    return coord_arr


def grid_to_image(
    latitude, longitude, QOI, hour, max_shape=256, mode="mean", verbose=True
):
    # Verbose
    print(f"Generating {mode} Image of water level...")

    lat_m, lat_M = latitude.min(), latitude.max()
    lon_m, lon_M = longitude.min(), longitude.max()

    delta_x = (lat_M - lat_m) / max_shape
    delta_y = (lon_M - lon_m) / max_shape
    delta = max(delta_x, delta_y)
    print(f"Latitude: {lat_m, lat_M}.")
    print(f"Longitude: {lon_m, lon_M}.")
    print(f"Res: {delta}.")

    nx, ny = int(np.ceil((lat_M - lat_m) / delta)), int(
        np.ceil((lon_M - lon_m) / delta)
    )

    coarse_image = np.zeros((nx, ny))
    for i in range(nx):
        for j in range(ny):
            cropped_latitude_id = np.where(
                (latitude > lat_m + i * delta) & (latitude < lat_m + (i + 1) * delta)
            )
            cropped_longitude_id = np.where(
                (longitude > lon_m + j * delta) & (longitude < lon_m + (j + 1) * delta)
            )
            cropped_id = np.intersect1d(cropped_latitude_id, cropped_longitude_id)

            if len(cropped_id) == 0:
                coarse_image[i, j] = 0

            else:
                cropped_water_level = QOI[hour, cropped_id]

                if mode.lower() == "mean":
                    coarse_image[i, j] = cropped_water_level.mean()
                elif mode.lower() == "std":
                    coarse_image[i, j] = cropped_water_level.std()
                elif mode.lower() == "minmax":
                    coarse_image[i, j] = (
                        cropped_water_level.max() - cropped_water_level.min()
                    )
                else:
                    raise NotImplementedError

        if verbose:
            print(f"Processing... {(i+1)/nx * 100:0.3f}%", end="\r")
    print("")

    coarse_image = np.flipud(coarse_image)
    return coarse_image


def grid_to_mask(grid_path, max_shape):
    def is_in(lmbda):
        return np.all(
            (lmbda >= 0) & (lmbda <= 1) & (np.sum(lmbda, axis=0) <= 1), axis=0
        )

    # Verbose
    print("Generating Mask...")

    # Load data grid from .grd file
    secA, secB = read_grid(grid_path)

    latitude, longitude = np.array(secA["latitude"]), np.array(secA["longitude"])
    lat_m, lat_M = latitude.min(), latitude.max()
    lon_m, lon_M = longitude.min(), longitude.max()

    delta_x = (lat_M - lat_m) / max_shape
    delta_y = (lon_M - lon_m) / max_shape
    delta = max(delta_x, delta_y)

    nx, ny = int(np.ceil((lat_M - lat_m) / delta)), int(
        np.ceil((lon_M - lon_m) / delta)
    )

    mask = np.zeros((nx, ny))
    lat_coord = np.linspace(lat_m, lat_M, nx)
    lon_coord = np.linspace(lon_m, lon_M, ny)
    mesh_coord = np.meshgrid(lat_coord, lon_coord)

    P = np.concatenate(
        (
            np.expand_dims(mesh_coord[0].flatten(), -1),
            np.expand_dims(mesh_coord[1].flatten(), -1),
        ),
        axis=1,
    ).T
    for k in range(len(secB["id"])):
        P1 = np.array([[latitude[secB["vA"][k] - 1]], [longitude[secB["vA"][k] - 1]]])
        P2 = np.array([[latitude[secB["vB"][k] - 1]], [longitude[secB["vB"][k] - 1]]])
        P3 = np.array([[latitude[secB["vC"][k] - 1]], [longitude[secB["vC"][k] - 1]]])

        A = np.concatenate((P1 - P3, P2 - P3), axis=1)
        A_inv = np.linalg.inv(A)

        lmbdas = A_inv @ (P - P3)
        pixels = np.where(is_in(lmbdas))
        for p in pixels[0]:
            i = p % nx
            j = p // nx

            mask[i, j] = 1

        perc = (k + 1) / len(secB["id"]) * 100
        print(f"Processing... {perc:0.3f}%", end="\r")
    print("")
    mask = np.flipud(mask)
    return mask
