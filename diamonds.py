import matplotlib.pyplot as plt
import numpy as np

# Settings
vertical_spacing = 1  # vertical distance between diamond centers (in inches)
theta = 69  # acute angle in degrees

# Page size (in inches) - US Letter
page_width = 8.5
page_height = 11.0


# Calculate half of each diagonal based on setting vertical diagonal = 1 inch
theta_rad = np.radians(theta)
# side length from vertical diagonal of 1 inch
s = 1 / (2 * np.cos(theta_rad / 2))
half_vertical = 0.5  # since vertical diagonal is 1 inch
half_horizontal = s * np.sin(theta_rad / 2)  # half the horizontal diagonal
# full horizontal diagonal
horizontal_diag = 2 * half_horizontal  # approx 0.688 inch

# Calculate the number of rows and columns to fill the page
cols = int(np.ceil(page_width / horizontal_diag))
rows = int(np.ceil(page_height / vertical_spacing))

# Create figure:  Set the figure size to exactly match the page size
fig, ax = plt.subplots(figsize=(page_width, page_height))


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

# Adjust limits to tightly fit the diamonds to the page edges:
ax.set_xlim(0, page_width)
ax.set_ylim(0, page_height)

ax.axis('off')

# Save the figure, ensuring the bounding box is tight and dpi is reasonable
plt.savefig("diamond_grid_full_page.pdf", format="pdf",
            bbox_inches="tight", dpi=300)  # dpi for good resolution
plt.show()
