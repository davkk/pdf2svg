class Page:
    def __init__(self, _id, num, tmp_dir):
        self._id = _id
        self.num = num

        self.pdf = f"{_id}.pdf"
        self.svg = f"{_id}.svg"

        self.pdf_path = tmp_dir / self.pdf
        self.svg_path = tmp_dir / self.svg

    def __lt__(self, other):
        return self.num < other.num
