import random
import numpy as np
import matplotlib.pyplot as plt

# Info:
# This program simulates a light source in a 2D grid with barriers.
# It is used by hikedex to determine the view rating of a summit, using ray casting.
# A "barrier" is just a point in the grid that blocks the simulated light.

# Define grid dimensions
grid_size = 50
initial_clusters = 4

# For random terrain generation
s = 2  # Size multiplier for barrier clusters
f = 1  # Frequency multiplier for barrier clusters

# Create a 2D array representing the grid with barriers
grid = np.zeros((grid_size, grid_size), dtype=bool)

barriers = []


def add_barrier_cluster(x, y, size=5):
    """
    Add a cluster of barriers to the grid.

    Parameters:
    x (int): The x-coordinate of the center of the cluster.
    y (int): The y-coordinate of the center of the cluster.
    size (int): The size of the cluster (default is 5).

    Returns:
    None
    """
    global grid, barriers
    for j in range(size * s):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        x = max(0, min(grid_size - 1, x + dx))
        y = max(0, min(grid_size - 1, y + dy))
        barriers.append((x, y))
        grid[y, x] = True


# Initial barrier clusters
for i in range(initial_clusters * f):
    size = random.choice([3, 5, 30, 15, 9, 2, 5])
    add_barrier_cluster(random.randint(0, grid_size - 1),
                        random.randint(0, grid_size - 1), size=size)


def calculate_shadow(barrier, point):
    """
    Calculates the shadow between a barrier and a point.

    Args:
        barrier (tuple): The coordinates of the barrier.
        point (tuple): The coordinates of the point.

    Returns:
        tuple: A tuple containing a boolean value indicating if there is a shadow, and the distance to the shadow.
    """
    dx = point[0] - barrier[0]
    dy = point[1] - barrier[1]
    distance = max(abs(dx), abs(dy))
    if distance == 0:
        return False, 0
    step_x = dx / distance
    step_y = dy / distance
    x, y = barrier
    for i in range(int(distance)):
        x += step_x
        y += step_y
        x_int, y_int = int(round(x)), int(round(y))
        if grid[x_int, y_int]:
            return True, i
    return False, distance


def click(event):
    """
    Handle the click event on the plot.

    Parameters:
    - event: The click event object.

    Returns:
    None
    """
    x = int(round(event.xdata))
    y = int(round(event.ydata))
    print(f"Adding a cluster of barriers at: ({x}, {y})")
    add_barrier_cluster(x, y)
    ax.clear()
    draw_plot()
    plt.gcf().canvas.draw_idle()


def draw_plot():
    """
    Draws a plot with a grid, shadow grid, and a light marker.

    This function calculates the shadow grid based on the light position and
    draws a plot with the grid, shadow grid, and a marker representing the light.

    Returns:
        None
    """
    global grid, barriers, light_position
    shadow_grid = np.zeros((grid_size, grid_size), dtype=float)
    for j in range(grid_size):
        for i in range(grid_size):
            blocked, length = calculate_shadow(light_position, (i, j))
            if not blocked:
                shadow_grid[i, j] = 1
    ax.imshow(grid, cmap='binary', origin='lower')
    ax.imshow(shadow_grid, cmap='summer', alpha=0.5, origin='lower')
    ax.scatter(*light_position, color='black',
               marker='x', s=100, label='Light')
    ax.grid(True, which='both', color='black', linestyle='--', linewidth=0.5)
    max_area = len(shadow_grid) * len(shadow_grid[0])
    print(f"View rating: {100 * np.sum(shadow_grid) / max_area:.2f}%")


# Matplotlib setup
fig = plt.figure()
ax = fig.add_subplot()

# Define the light position (center of the grid)
light_position = (grid_size // 2, grid_size // 2)

# Draw the plot
draw_plot()

# Connect the click event to the plot
plt.gcf().canvas.mpl_connect('button_press_event', click)

plt.show()
