import matplotlib.pyplot as plt
import numpy as np

# Settings
rows = 10      # number of diamond rows
cols = 10      # number of diamond columns
vertical_spacing = 1  # vertical distance between diamond centers (in inches)
theta = 69  # acute angle in degrees

# Calculate half of each diagonal based on setting vertical diagonal = 1 inch
theta_rad = np.radians(theta)
# side length from vertical diagonal of 1 inch
s = 1 / (2 * np.cos(theta_rad / 2))
half_vertical = 0.5  # since vertical diagonal is 1 inch
half_horizontal = s * np.sin(theta_rad / 2)  # half the horizontal diagonal
# full horizontal diagonal
horizontal_diag = 2 * half_horizontal  # approx 0.688 inch

# Create figure: set figure size such that spacing is respected
fig, ax = plt.subplots(
    figsize=(cols * horizontal_diag, rows * vertical_spacing))


def draw_diamond(ax, center_x, center_y):
    # Coordinates of the diamond vertices
    coords = np.array([
        [center_x, center_y + half_vertical],        # Top vertex
        [center_x + half_horizontal, center_y],        # Right vertex
        [center_x, center_y - half_vertical],          # Bottom vertex
        [center_x - half_horizontal, center_y],        # Left vertex
        [center_x, center_y + half_vertical]           # Close the diamond
    ])
    ax.plot(coords[:, 0], coords[:, 1], 'k')


# Draw grid of diamonds:
for row in range(rows):
    for col in range(cols):
        # Horizontally, use the horizontal diagonal as the spacing so diamonds touch.
        x = col * horizontal_diag
        y = row * vertical_spacing
        draw_diamond(ax, x, y)

# Formatting
ax.set_aspect('equal')
# Adjust limits so we see the diamonds properly:
ax.set_xlim(-half_horizontal, cols * horizontal_diag + half_horizontal)
ax.set_ylim(-half_vertical, rows * vertical_spacing + half_vertical)
ax.axis('off')

plt.savefig("diamond_grid.pdf", format="pdf", bbox_inches="tight")
plt.show()
