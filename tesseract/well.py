from typing import Tuple, List


class Well():
    """
    The logical representation of a well
    containing the stack of dropped pieces.
    """
    def __init__(self, lines: int, columns: int) -> None:
        self.stack: List[List[int]] = [
            [0 for i in range(columns)] for j in range(lines)
                ]

    def get_height(self) -> int:
        return len(self.stack)

    def get_width(self) -> int:
        return len(self.stack[0])

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the board as a tuple (HEIGHT, WIDTH)
        """
        return self.get_height(), self.get_width()

    def is_empty(self) -> bool:
        """
        Checks whether the board contains only zeroes.
        """
        zeroes: int = sum([l.count(0) for l in self.stack])
        s = self.get_size()
        area: int = s[0] * s[1]
        return zeroes == area
