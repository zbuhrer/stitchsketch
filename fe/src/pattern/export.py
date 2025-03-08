import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def export_to_pdf(pattern_data, output_path):
    """
    Export the pattern data to a PDF file.

    Args:
        pattern_data (dict): A dictionary containing the pattern data,
                             including the shapes and their positions.
        output_path (str): The path to save the PDF file.
    """
    try:
        c = canvas.Canvas(output_path)
        c.drawString(inch, 10.5 * inch, "Pattern Export")  # Example text

        # Iterate through the pattern data and draw the shapes
        for shape_id, shape_info in pattern_data.items():
            shape_type = shape_info["type"]
            coordinates = shape_info["coordinates"]

            if shape_type == "line":
                x1, y1, x2, y2 = coordinates
                c.line(x1, y1, x2, y2)
            elif shape_type == "polygon":
                c.polygon(coordinates)
            # Add more shape types as needed

        c.save()
    except IOError as e:
        print(f"IOError during PDF export: {e}")
        # Consider raising the exception or returning an error code


def export_to_svg(pattern_data, output_path):
    """
    Export the pattern data to an SVG file.

    Args:
        pattern_data (dict): A dictionary containing the pattern data,
                             including the shapes and their positions.
        output_path (str): The path to save the SVG file.
    """
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="8in" height="10in" viewBox="0 0 8 10" xmlns="http://www.w3.org/2000/svg">
"""

    # Iterate through the pattern data and create SVG elements
    for shape_id, shape_info in pattern_data.items():
        shape_type = shape_info["type"]
        coordinates = shape_info["coordinates"]

        if shape_type == "line":
            x1, y1, x2, y2 = coordinates
            svg_content += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{
                y2}" stroke="black" stroke-width="0.01" />\n'
        elif shape_type == "polygon":
            points = " ".join([f"{x},{y}" for x, y in coordinates])
            svg_content += f'<polygon points="{
                points}" stroke="black" stroke-width="0.01" fill="none" />\n'
        # Add more shape types as needed

    svg_content += "</svg>"

    try:
        with open(output_path, "w") as f:
            f.write(svg_content)
    except IOError as e:
        print(f"IOError during SVG export: {e}")
        # Consider raising the exception or returning an error code


def export_to_image(pattern_data, output_path, image_format="png"):
    """
    Export the pattern data to an image file (PNG, JPG, etc.).
    Requires reportlab and svglib.

    Args:
        pattern_data (dict): A dictionary containing the pattern data.
        output_path (str): The path to save the image file.
        image_format (str): The format of the image (e.g., "png", "jpg").
    """
    temp_svg_path = "temp_pattern.svg"  # Temporary SVG file

    try:
        # Export to SVG first
        export_to_svg(pattern_data, temp_svg_path)

        # Convert SVG to image using reportlab
        drawing = svg2rlg(temp_svg_path)

        if image_format.lower() == "png":
            renderPM.drawToFile(drawing, output_path, fmt="PNG")
        elif image_format.lower() == "jpg" or image_format.lower() == "jpeg":
            renderPM.drawToFile(drawing, output_path, fmt="JPG")
        else:
            raise ValueError(f"Unsupported image format: {image_format}")

        # Clean up temporary SVG file
        os.remove(temp_svg_path)
    except IOError as e:
        print(f"IOError during image export: {e}")
    except ValueError as e:
        print(f"Value Error during image export {e}")
    except Exception as e:
        print(f"Exception during image export {e}")
