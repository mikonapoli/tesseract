import sdl2.ext
import legacy.graphics.constants as CONST


class BoardRenderer(sdl2.ext.Renderer):
    def __init__(self, board_surface,
                 board_object, hidden_rows=2, center=False):
        super(BoardRenderer, self).__init__(board_surface)
        self.board = board_object
        self.bsize = self.board.get_board_size()
        self.hid = hidden_rows

        self.centered = center

        self.hstep = int(board_surface.w // self.bsize[0])
        self.vstep = int(board_surface.h // (self.bsize[1] - self.hid))

        self.color_code = CONST.COLOR_CODE

        self.clear(color=CONST.BLACK)

    def render_board(self, piece):
        self.clear(color=CONST.BLACK)
        to_fill = []
        bbox = piece.piecedata.bbox[piece.piecedata.rot]
        pos_x = 0
        pos_y = 0
        if self.centered:
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

        for y in range(self.hid, self.bsize[1]):
            for x in range(self.bsize[0]):
                if self.board.boardstatus.map[y][x] != 0:
                    to_fill.append(((x * self.hstep, (y - 2) * self.vstep,
                                     self.hstep, self.vstep),
                                    self.color_code[
                        self.board.boardstatus.map[y][x]
                    ]))

        for x in range(bbox[1] + 1):
            for y in range(bbox[2] + 1):
                s = piece.piecedata.shape[y][x]
                if s != 0:
                    # Render the ghost piece
                    to_fill.append(
                        ((pos_x + (piece.piecedata.x + x) *
                          self.hstep, pos_y +
                          ((piece.piecedata.ghost_y - 3) + y) * self.vstep,
                          self.hstep, self.vstep), 9))
                    # Render the actual piece
                    if piece.piecedata.y + y >= 2:
                        to_fill.append(
                            ((pos_x + (piece.piecedata.x + x) *
                              self.hstep, pos_y +
                              ((piece.piecedata.y - 2) + y) *
                              self.vstep, self.hstep, self.vstep),
                             self.color_code[piece.piecedata.color_code]
                             ))

        for s in to_fill:
            self.fill(s[0], s[1])
            self.draw_rect(s[0], CONST.WHITE)

        self.present()
