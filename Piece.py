import sdl2.ext
from constants import PIECES, WALL_KICK
from random import random


class VirtualPieceChecker(sdl2.ext.Applicator):
    def __init__(self, board):
        super(VirtualPieceChecker, self).__init__()
        self.componenttypes = (VirtualPiece, PieceData)
        self.board_size = board.get_board_size()
        self.board = board

    def _out_of_board(self, piece):

        if (piece.boardposition.x + piece.bbox[piece.rot][0] < 0 or
            piece.boardposition.x + piece.bbox[piece.rot][1] >=
            self.board_size[0] or
                piece.boardposition.y + piece.bbox[piece.rot][2] >=
                self.board_size[1]):

            return True

        else:
            return False

    def _board_collision(self, piece):
        collision = False
        bbox = piece.bbox[piece.rot]
        for i in range(bbox[0], bbox[1] + 1):
            for j in range(bbox[2] + 1):
                if (piece.shape[j][i] != 0 and
                        self.board.boardstatus.map[piece.boardposition.y + j]
                        [piece.boardposition.x + i] != 0):
                    collision = True

        return collision

    def process(self, world, componentsets):
        for vp, pd in componentsets:

            pd.blocked = self._out_of_board(vp) or self._board_collision(vp)
            piece_rotated = (vp.rot != pd.rot)

            # Wall kick implementation
            if pd.blocked and piece_rotated:
                kickmap = None
                if pd.type in WALL_KICK:
                    kickmap = WALL_KICK[pd.type]
                else:
                    kickmap = WALL_KICK["X"]
                if vp.rot - pd.rot in (1, -3):
                    rotation_type = 1
                    ind = vp.rot
                else:
                    rotation_type = -1
                    ind = pd.rot
                for test in kickmap[ind]:
                    if pd.blocked:
                        vp.boardposition.x = pd.boardposition.x + \
                            (rotation_type * test[0])
                        vp.boardposition.y = pd.boardposition.y + \
                            (rotation_type * test[1])
                        pd.blocked = self._out_of_board(
                            vp) or self._board_collision(vp)

            if pd.blocked:

                vp.boardposition.x = pd.boardposition.x
                vp.boardposition.y = pd.boardposition.y

                vp.shape = pd.shape
                vp.rot = pd.rot

            else:

                pd.boardposition.x = vp.boardposition.x
                pd.boardposition.y = vp.boardposition.y
                old_y = vp.boardposition.y
                while not pd.blocked:
                    pd.blocked = self._out_of_board(
                        vp) or self._board_collision(vp)
                    pd.ghost_y = vp.boardposition.y
                    vp.boardposition.y += 1
                pd.blocked = False
                vp.boardposition.y = old_y
                pd.shape = vp.shape
                pd.rot = vp.rot


class PieceMovement:
    def move_left(self, piece):
        piece.virtualpiece.boardposition.x -= 1
        piece.piecedata.moved = True

    def move_right(self, piece):
        piece.virtualpiece.boardposition.x += 1
        piece.piecedata.moved = True

    def move_down(self, piece):
        piece.virtualpiece.boardposition.y += 1
        piece.piecedata.moved = True

    def rotate(self, piece, mov=1):
        new_index = (piece.virtualpiece.rot +
                     mov) % len(piece.virtualpiece.rotmap)

        piece.virtualpiece.rot = new_index
        piece.virtualpiece.shape = piece.virtualpiece.rotmap[new_index]

    def drop(self, piece):
        # piece.piecedata.boardposition.y = piece.piecedata.ghost_y -1
        piece.virtualpiece.boardposition.y = piece.piecedata.ghost_y - 1
        piece.piecedata.moved = True

    def rotate_left(self, piece):
        self.rotate(piece, -1)


class VirtualPiece(object):
    def __init__(self, rotation, rotation_map, color,
                 piecetype, posx, posy, bounding_box):

        self.rot = rotation
        self.type = piecetype
        self.rotmap = rotation_map
        self.bbox = bounding_box
        self.color_code = color
        self.shape = self.rotmap[self.rot]
        # self.w = len(self.shape[0])
        # self.h = len(self.shape)
        self.boardposition = BoardPosition(posx, posy)


class PieceData(VirtualPiece):
    def __init__(self, rotation, rotation_map, color,
                 piecetype, posx, posy, bounding_box):
        super(PieceData, self).__init__(rotation, rotation_map,
                                        color, piecetype, posx, posy,
                                        bounding_box)
        self.blocked = False
        self.moved = False
        self.ghost_y = 0


class PieceFactory:
    def __init__(self):
        self.piece_catalog = PIECES
        self.pieces = ["i", "j", "o", "l", "t", "s", "z"]
        self.piecebag = []
        self.fill_bag()

    def get_next_piece_type(self):
        return self.piecebag[0]

    def fill_bag(self):
        perm = [i for i in range(len(self.pieces))]
        while len(perm) > 0:
            i = int(len(perm) * random())
            self.piecebag.append(self.pieces[perm.pop(i)])

    def get_next_piece(self, world):
        piece = self.spawn_piece(world, self.get_next_piece_type(), 0, 2)
        return piece

    def spawn_piece(self, world, piecetype=None, x_pos=3, y_pos=0):
        if len(self.piecebag) <= 1:
            self.fill_bag()
        if piecetype is None:
            piecetype = self.piecebag.pop(0)
        cat_entry = self.piece_catalog[piecetype]
        piece = Piece(world, cat_entry[0], x_pos, y_pos, 0,
                      cat_entry[1], cat_entry[2], cat_entry[3])
        return piece


class BoardPosition(object):
    def __init__(self, px, py):
        super(BoardPosition, self).__init__()
        self.x = px
        self.y = py


class Piece(sdl2.ext.Entity):
    def __init__(self, world, piecetype, posx, posy,
                 rotation, rotationmap, color, rotpos):

        super(Piece, self).__init__()

        self.piecedata = PieceData(
            rotation, rotationmap, color, piecetype, posx, posy, rotpos)
        self.virtualpiece = VirtualPiece(
            rotation, rotationmap, color, piecetype, posx, posy, rotpos)
