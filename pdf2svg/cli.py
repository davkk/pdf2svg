import typer

from pathlib import Path

from pdf2svg.models import Convert

app = typer.Typer()


@app.command()
def load_pdf(
    pdf_path: Path = typer.Argument(
        ...,
        help="Path to the pdf.",
        exists=True,
        resolve_path=True,
        file_okay=True,
        readable=True,
    )
) -> None:
    with Convert() as convert:
        convert.load_pdf(pdf_path)

        tmp_dir = Path("/tmp/pdf2svg") / convert._id
        tmp_dir.mkdir(parents=True)

        convert.split_pdf(tmp_dir)

        convert.merge_svgs()
