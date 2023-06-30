import re

from pathlib import Path


def get_dim(svg_path: Path):
    pattern = re.compile(r"viewBox=\".*\"", re.IGNORECASE)

    with open(str(svg_path)) as svg_file:
        viewbox = pattern.search(svg_file.read()).group(0)

        *_, width, height = viewbox.split('"')[1].split()

        return float(width), float(height)

    return 800.0, 1130.0
