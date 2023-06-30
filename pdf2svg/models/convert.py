import shortuuid
import subprocess

from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader

from svgutils.compose import Figure, SVG, Line

from pdf2svg.models import Page
from pdf2svg.utils.get_dim import get_dim


class Convert:
    def __init__(self):
        self._id = shortuuid.uuid()

    def load_pdf(self, pdf_path):
        self.pdf_path = pdf_path
        self.file_name = pdf_path.stem

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        tmp_dir = Path("/tmp/pdf2svg") / self._id

        for page in self.pages:
            Path.unlink(tmp_dir / page.pdf)
            Path.unlink(tmp_dir / page.svg)

        tmp_dir.rmdir()
        tmp_dir.parent.rmdir()

    def split_pdf(self, tmp_dir):
        """
        Splits given PDF into multiple pages
        and saves each to temp dir as single PDF and SVG file.
        """
        input_pdf = PdfFileReader(open(self.pdf_path, "rb"))

        pages = []

        for i in range(input_pdf.numPages):
            output = PdfFileWriter()
            output.addPage(input_pdf.getPage(i))

            page = Page(_id=shortuuid.uuid(), num=i, tmp_dir=tmp_dir)

            with open(page.pdf_path, "wb") as output_stream:
                output.write(output_stream)

            subprocess.call(["inkscape", "-l", page.svg_path, page.pdf_path])

            pages.append(page)

        self.pages = sorted(pages)

    def merge_svgs(self):
        save_path = str(self.pdf_path.resolve().parent / f"{self.file_name}.svg")

        width, height = get_dim(self.pages[0].svg_path)
        len_pages = len(self.pages)

        canvas_width = width + 100
        canvas_height = (height * len_pages) - (143 * (len_pages - 1))
        x0 = 50

        Figure(
            str(canvas_width),
            str(canvas_height),
            Line(
                [(0, canvas_height / 2), (canvas_width, canvas_height / 2)],
                canvas_height,
                "white",
            ),
            *[
                SVG(str(page.svg_path)).move(x0, (height - 143) * idx)
                for idx, page in enumerate(self.pages)
            ],
        ).save(str(save_path))
