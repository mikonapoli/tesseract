import sdl2.ext  # type: ignore
from .constants import PIECES, WALL_KICK
from random import random

# TODO: this should be a component, not a System.
# System should be a collision detector


class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Piece,
        self.board = None

    def _out_of_board(self, piece):
        vp = piece.virtualstatus
        vbb = piece.get_virtual_bounding_box()
        board_size = self.board.get_size()
        if (vp.x + vbb[0] < 0 or
            vp.x + vbb[1] >=
            board_size[0] or
                vp.y + vbb[2] >=
                board_size[1]):

            return True

        else:
            return False

    def _board_collision(self, piece):
        vp = piece.virtualstatus
        collision = False
        bbox = piece.get_virtual_bounding_box()
        for i in range(bbox[0], bbox[1] + 1):
            for j in range(bbox[2] + 1):
                if (piece.get_virtual_shape()[j][i] != 0 and
                        self.board.boardstatus.map[vp.y + j]
                        [vp.x + i] != 0):
                    collision = True

        return collision

    def _is_movement_blocked(self, piece):
        return self._out_of_board(piece) or self._board_collision(piece)

    def _wall_kick(self, piece):
        vp, pd = piece.virtualstatus, piece.status
        # Wall kick
        kickmap = WALL_KICK["X"]
        if piece.piecedata.type in WALL_KICK:
            kickmap = WALL_KICK[piece.piecedata.type]
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
                vp.x = pd.x + (rotation_type * test[0])
                vp.y = pd.y + (rotation_type * test[1])
                pd.blocked = self._is_movement_blocked(piece)

    def process(self, world, componentsets):
        for pc, in componentsets:
            pd, vp = pc.status, pc.virtualstatus
            pd.blocked = self._is_movement_blocked(pc)

            # Wall kick implementation
            if pd.blocked and pc.is_rotated():
                self._wall_kick(pc)

            if pd.blocked:
                # Virtual piece reset back to actual piece
                pc.reset_virtual_piece()

            else:
                # Piece is free to change position. Actual piece gets
                # position of virtual piece
                pc.accept_virtual_piece()
                # Find the position of ghost piece moving down the virtual
                # until it is blocked, then move back the virtual piece
                old_y = vp.y
                while not pd.blocked:
                    pd.blocked = self._is_movement_blocked(pc)
                    vp.y += 1
                pd.ghost_y = vp.y-1
                vp.y = old_y
                pd.blocked = False


class VirtualStatus:
    def __init__(self, rotation, x, y):
        self.rot = rotation
        self.x = x
        self.y = y

    def copy_status(self, status):
        self.rot = status.rot
        self.x = status.x
        self.y = status.y


class Status(VirtualStatus):
    def __init__(self, rotation, x, y):
        super(Status, self).__init__(rotation, x, y)
        self.blocked = False
        self.moved = False
        self.ghost_y = 0


class PieceData:
    def __init__(self, rotation_map, piece_type, color_code, bbox):
        self.rot_map = rotation_map
        self.color_code = color_code
        self.type = piece_type
        self.b_box = bbox


class Piece(sdl2.ext.Entity):
    def __init__(self, world, piecetype, posx, posy,
                 rotation, rotationmap, color, rotpos):
        super(Piece, self).__init__()
        self.piecedata = PieceData(rotationmap, piecetype, color, rotpos)
        self.status = Status(rotation, posx, posy)
        self.virtualstatus = VirtualStatus(rotation, posx, posy)

    def get_shape(self, status=None):
        if status is None:
            status = self.status
        return self.piecedata.rot_map[status.rot]

    def get_virtual_shape(self):
        return self.get_shape(self.virtualstatus)

    def get_bounding_box(self, status=None):
        if status is None:
            status = self.status
        return self.piecedata.b_box[status.rot]

    def get_virtual_bounding_box(self):
        return self.get_bounding_box(self.virtualstatus)

    def is_rotated(self):
        return (self.virtualstatus.rot != self.status.rot)

    def reset_virtual_piece(self):
        self.virtualstatus.copy_status(self.status)

    def accept_virtual_piece(self):
        self.status.copy_status(self.virtualstatus)

    def move(self, mx=0, my=0):
        self.virtualstatus.x += mx
        self.virtualstatus.y += my
        self.piecedata.moved = True

    def move_left(self):
        self.move(mx=-1)

    def move_right(self):
        self.move(mx=1)

    def move_down(self):
        self.move(my=1)

    def drop(self):
        self.virtualstatus.y = self.status.ghost_y - 1
        self.status.moved = True

    def rotate(self, mov=1):
        new_index = (self.virtualstatus.rot +
                     mov) % len(self.piecedata.rot_map)

        self.virtualstatus.rot = new_index

    def rotate_left(self):
        self.rotate(-1)


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
