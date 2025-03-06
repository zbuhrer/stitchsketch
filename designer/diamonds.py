import matplotlib.pyplot as plt
import numpy as np

# Settings (all units in inches)
VERTICAL_SPACING = 1
THETA_DEGREES = 69
PAGE_WIDTH = 8.5
PAGE_HEIGHT = 11.0
DPI = 300  # Resolution for saving the figure


def create_diamond_grid(vertical_spacing, theta_degrees, page_width, page_height, dpi, filename="diamond_grid_full_page.pdf"):
    """
    Generates a PDF of a diamond grid filling the specified page size.

    Args:
        vertical_spacing: Vertical distance between diamond centers (inches).
        theta_degrees: Acute angle of the diamond (degrees).
        page_width: Page width (inches).
        page_height: Page height (inches).
        dpi: Resolution for saving the PDF.
        filename: name of the output PDF file.
    """

    theta_radians = np.radians(theta_degrees)
    half_vertical = 0.5  # Since vertical diagonal is 1 inch
    side_length = half_vertical / np.cos(theta_radians / 2)
    half_horizontal = side_length * np.sin(theta_radians / 2)
    horizontal_diag = 2 * half_horizontal

    cols = int(np.ceil(page_width / horizontal_diag))
    rows = int(np.ceil(page_height / vertical_spacing))

    fig, ax = plt.subplots(figsize=(page_width, page_height))

    def draw_diamond(ax, center_x, center_y):
        coords = np.array([
            [center_x, center_y + half_vertical],
            [center_x + half_horizontal, center_y],
            [center_x, center_y - half_vertical],
            [center_x - half_horizontal, center_y],
            [center_x, center_y + half_vertical]
        ])
        ax.plot(coords[:, 0], coords[:, 1], 'k')

    for row in range(rows):
        for col in range(cols):
            x = col * horizontal_diag
            y = row * vertical_spacing
            draw_diamond(ax, x, y)

    ax.set_aspect('equal')
    ax.set_xlim(0, page_width)
    ax.set_ylim(0, page_height)
    ax.axis('off')

    plt.savefig(filename, format="pdf", bbox_inches="tight", dpi=dpi)
    plt.close(fig)  # clean up memory


if __name__ == "__main__":
    create_diamond_grid(VERTICAL_SPACING, THETA_DEGREES,
                        PAGE_WIDTH, PAGE_HEIGHT, DPI)
    print("Diamond grid generated successfully!")
