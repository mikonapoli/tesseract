import sdl2.ext  # type: ignore
from . import constants as CONST


class BoardRenderer(sdl2.ext.Renderer):
    def __init__(self, board_surface,
                 board_object, hidden_rows=2, center=False):
        super(BoardRenderer, self).__init__(board_surface)
        self.board = board_object
        self.bsize = self.board.get_size()
        self.hid = hidden_rows

        # If true, the piece will be rendered
        # in the center of the board
        self.draw_in_the_center = center

        self.hstep = int(board_surface.w // self.bsize[0])
        self.vstep = int(board_surface.h // (self.bsize[1] - self.hid))

        self.color_code = CONST.COLOR_CODE

        self.clear(color=CONST.BLACK)

        self.to_draw = []

    def _compute_centered_position(self, piece, bbox):
        if piece.piecedata.type == "o":
            w = 4
        else:
            w = bbox[1] + 1
        if piece.piecedata.type == "i":
            h = 1
        else:
            h = 2
        pos_x = int((self.bsize[0] - w) * self.hstep / 2)
        pos_y = int(h * self.vstep / 2)
        return pos_x, pos_y

    def _draw_block(self, block_rect, block_colour):
        self.fill(block_rect, block_colour)
        self.draw_rect(block_rect, CONST.WHITE)

    def _draw(self):
        self.clear(color=CONST.BLACK)
        for s in self.to_draw:
            self._draw_block(s[0], s[1])
        self.present()
        self.to_draw = []

    def _render_blocks(self, x_offset, y_offset, x, y, code):
        if code != 0:
            self.to_draw.append(((x_offset + x * self.hstep,
                                 y_offset + (y - 2) * self.vstep,
                                 self.hstep, self.vstep),
                                self.color_code[code]))

    def _render_stack(self):
        for y in range(self.hid, self.bsize[1]):
            for x in range(self.bsize[0]):
                self._render_blocks(0, 0, x, y,
                                    self.board.boardstatus.map[y][x])

    def paint_shape(self, piece, ccode=None):
        if ccode is None:
            ccode = piece.piecedata.color_code
        shape = piece.piecedata.shape
        painted_shape = [[i*ccode for i in line] for line in shape]
        return painted_shape

    def render_piece(self, piece, is_ghost=False):
        bbox = piece.piecedata.bbox[piece.piecedata.rot]
        if self.draw_in_the_center:
            pos_x, pos_y = self._compute_centered_position(piece, bbox)
        else:
            pos_x, pos_y = (0, 0)
        if is_ghost:
            shape_to_paint = self.paint_shape(piece, ccode=9)
            piece_y = piece.piecedata.ghost_y - 1
        else:
            shape_to_paint = self.paint_shape(piece)
            piece_y = piece.piecedata.y

        for x in range(bbox[1] + 1):
            for y in range(bbox[2] + 1):
                p_x = piece.piecedata.x + x
                p_y = piece_y + y
                p_code = shape_to_paint[y][x]
                if p_y >= self.hid:
                    self._render_blocks(pos_x, pos_y, p_x, p_y, p_code)

    def render_board(self, piece):
        bbox = piece.piecedata.bbox[piece.piecedata.rot]
        pos_x = 0
        pos_y = 0
        if self.draw_in_the_center:
            pos_x, pos_y = self._compute_centered_position(piece, bbox)

        self._render_stack()

        self.render_piece(piece, is_ghost=True)
        self.render_piece(piece)

        self._draw()
