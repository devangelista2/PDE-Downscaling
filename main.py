import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Parameters
alpha = 0.01  # Thermal diffusivity
Lx, Ly = 1.0, 1.0  # Domain size
Nx, Ny = 50, 50  # Number of grid points
dx, dy = Lx / (Nx - 1), Ly / (Ny - 1)  # Grid spacing
dt = 0.001  # Time step
T = 0.1  # Total simulation time

# Initial conditions
u = np.zeros((Nx, Ny))
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)
u[:, :] = np.sin(np.pi * X) * np.sin(np.pi * Y)  # Initial temperature distribution
u0 = u.copy()


# Non-homogeneous term function
def f(x, y, t):
    return 0.1 * np.sin(2 * np.pi * x) * np.sin(2 * np.pi * y) * np.exp(-t)


# Main simulation loop
num_steps = int(T / dt)
for n in range(num_steps):
    # Compute Laplacian using central differences
    laplacian = (
        np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
        - 4 * u
    ) / (dx * dy)

    # Update temperature using the explicit Euler method
    u += dt * (alpha * laplacian + f(X, Y, n * dt))

print(np.linalg.norm(u - u0))

# Plot the source
plt.imshow(f(X, Y, 0))
plt.colorbar(label="Temperature")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Source location and value at initial time")
plt.show()

# Plot the final temperature distribution as a heat-map
plt.imshow(u, extent=[0, Lx, 0, Ly], origin="lower", cmap="viridis")
plt.colorbar(label="Temperature")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("2D Non-Homogeneous Heat Equation Simulation")
plt.show()
