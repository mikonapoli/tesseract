from typing import Tuple


class Board():
    def __init__(self, lines: int, columns: int) -> None:
        self.height: int = lines
        self.width: int = columns

    def get_size(self) -> Tuple[int, int]:
        return self.height, self.width
