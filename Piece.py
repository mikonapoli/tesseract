import sdl2.ext
from constants import PIECES, WALL_KICK
from random import random

# TODO: this should be a component, not a System.
# System should be a collision detector


class VirtualPieceChecker(sdl2.ext.Applicator):
    def __init__(self, board):
        super(VirtualPieceChecker, self).__init__()
        self.componenttypes = [VirtualPiece, PieceData]
        self.board_size = board.get_board_size()
        self.board = board

    def _out_of_board(self, piece):

        if (piece.x + piece.bbox[piece.rot][0] < 0 or
            piece.x + piece.bbox[piece.rot][1] >=
            self.board_size[0] or
                piece.y + piece.bbox[piece.rot][2] >=
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
                        self.board.boardstatus.map[piece.y + j]
                        [piece.x + i] != 0):
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
                        vp.x = pd.x + \
                            (rotation_type * test[0])
                        vp.y = pd.y + \
                            (rotation_type * test[1])
                        pd.blocked = self._out_of_board(
                            vp) or self._board_collision(vp)

            if pd.blocked:
                if piece_rotated:
                    # Wall kick
                    kickmap = None
                    if pd.type in WALL_KICK:
                        kickmap = WALL_KICK[pd.type]
                    else:
                        kickmap = WALL_KICK["X"]
                    # Left or right rotation
                    if vp.rot - pd.rot in (1, -3):
                        rotation_type = 1
                        ind = vp.rot
                    else:
                        rotation_type = -1
                        ind = pd.rot
                    # Try each position in the kickmap to find if it fits
                    for test in kickmap[ind]:
                        if pd.blocked:
                            vp.x = pd.x + \
                                (rotation_type * test[0])
                            vp.y = pd.y + \
                                (rotation_type * test[1])
                            pd.blocked = self._out_of_board(
                                vp) or self._board_collision(vp)
                # Virtual piece reset back to actual piece
                vp.x = pd.x
                vp.y = pd.y

                vp.shape = pd.shape
                vp.rot = pd.rot

            else:
                # Piece is free to change position. Actual piece gets position
                # position of virtual piece
                pd.x = vp.x
                pd.y = vp.y
                pd.shape = vp.shape
                pd.rot = vp.rot
                # Find the position of ghost piece moving down the virtual
                # until it is blocked, then move back the virtual piece
                old_y = vp.y
                while not pd.blocked:
                    pd.blocked = self._out_of_board(
                        vp) or self._board_collision(vp)
                    vp.y += 1
                pd.ghost_y = vp.y-1
                vp.y = old_y
                pd.blocked = False


class VirtualPiece(object):
    def __init__(self, rotation, rotation_map, color,
                 piecetype, posx, posy, bounding_box, virtual=False):

        self.rot = rotation
        self.type = piecetype
        self.rotmap = rotation_map
        self.bbox = bounding_box
        self.color_code = color
        self.shape = self.rotmap[self.rot]
        self.x = posx
        self.y = posy


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


class Piece(sdl2.ext.Entity):
    def __init__(self, world, piecetype, posx, posy,
                 rotation, rotationmap, color, rotpos):
        super(Piece, self).__init__()
        self.piecedata = PieceData(
            rotation, rotationmap, color, piecetype, posx, posy, rotpos)
        self.virtualpiece = VirtualPiece(
            rotation, rotationmap, color, piecetype, posx, posy, rotpos)

    def move(self, mx=0, my=0, drop=False):
        if drop:
            self.virtualpiece.y = self.piecedata.ghost_y - 1
        else:
            self.virtualpiece.x += mx
            self.virtualpiece.y += my
        self.piecedata.moved = True

    def move_left(self):
        self.move(mx=-1)

    def move_right(self):
        self.move(mx=1)

    def move_down(self):
        self.move(my=1)

    def drop(self):
        self.move(drop=True)

    def rotate(self, mov=1):
        new_index = (self.virtualpiece.rot +
                     mov) % len(self.virtualpiece.rotmap)

        self.virtualpiece.rot = new_index
        self.virtualpiece.shape = self.virtualpiece.rotmap[
            new_index]

    def rotate_left(self):
        self.rotate(-1)
