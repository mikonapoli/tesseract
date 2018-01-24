from typing import Tuple, List


class Board():
    """
    The logical representation of a game board.
    """
    def __init__(self, lines: int, columns: int) -> None:
        self.map: List[List[int]] = [
            [0 for i in range(columns)] for j in range(lines)
                ]

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the board as a tuple (HEIGHT, WIDTH)
        """
        height: int = len(self.map)
        width: int = len(self.map[0])
        return height, width

    def is_empty(self) -> bool:
        """
        Checks whether the board contains only zeroes.
        """
        zeroes: int = sum([l.count(0) for l in self.map])
        s = self.get_size()
        area: int = s[0] * s[1]
        return zeroes == area
