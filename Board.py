import sdl2.ext
import constants as CONST
from Piece import Piece


class BoardStatus(object):
    def __init__(self, map):
        super(BoardStatus, self).__init__()

        self.map = map

        self.columns = len(self.map[0])
        self.rows = len(self.map)
        self.to_update = False


class BoardUpdater(sdl2.ext.Applicator):

    def __init__(self):
        super(BoardUpdater, self).__init__()
        self.componenttypes = [BoardStatus, Piece]

    def _update_board_status(self, piece, boardstatus):
        bbox = piece.piecedata.bbox[piece.piecedata.rot]
        for i in range(bbox[2] + 1):
            for j in range(bbox[0], bbox[1] + 1):
                a = piece.piecedata.shape[i][j]
                pos = piece.piecedata.boardposition
                if a != 0:
                    ccode = piece.piecedata.color_code
                    boardstatus.map[i + pos.y][j + pos.x] = ccode

    def _check_and_delete_rows(self, boardstatus):
        # deleted_rows = 0
        s = (boardstatus.columns, boardstatus.rows)
        for r in range(s[1]):
            to_delete = True
            for x in boardstatus.map[r]:
                to_delete = to_delete and (x != 0)
            if to_delete:

                boardstatus.map.pop(r)
                boardstatus.map.insert(0, [0] * s[0])

    def process(self, world, componentsets):
        for b, p in componentsets:

            if b.to_update:
                self._update_board_status(p, b)
                self._check_and_delete_rows(b)
                b.to_update = False


class Board(sdl2.ext.Entity):
    def __init__(self, world, map=CONST.DEFAULT_BOARD):
        super(Board, self).__init__()
        self.boardstatus = BoardStatus(map)
        self.piece = None

    def get_board_size(self):

        return (self.boardstatus.columns, self.boardstatus.rows)
