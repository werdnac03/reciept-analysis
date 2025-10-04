from dataclasses import dataclass
@dataclass
class Word:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float
    # only line_num is useful
    ids: tuple[int, int, int, int]  # (page_num, block_num, par_num, line_num)

    @property
    def right(self): return self.left + self.width
    @property
    def bottom(self): return self.top + self.height

@dataclass
class Phrase:
    text: str
    bbox: tuple[int, int, int, int]  # (x1, y1, x2, y2)