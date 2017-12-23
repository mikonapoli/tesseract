import sdl2
from sdl2.ext import init as init_graphic_system
from sdl2.ext import Window, subsurface, fill

import legacy.graphics.renderers as GS
import legacy.graphics.constants as CONST
import legacy.Piece as PC
import legacy.Board as BD


class WindowSystem():

    def __init__(self, board_size):
        init_graphic_system()
        self.window = Window("Tesseract", size=(800, 600))
        self.background = self.window.get_surface()

        step = min(30,
                   int((self.window.size[0] - 20) / ((board_size[0] + 2) * 2)),
                   int((self.window.size[1] - 20) / (board_size[1])))

        self.board_background = subsurface(self.background,
                                           (10,
                                            10,
                                            (board_size[0] + 2) * step,
                                            (board_size[1]) * step)
                                           )

        self.board_surface = subsurface(self.board_background,
                                        (step,
                                         step,
                                         board_size[0] * step,
                                         (board_size[1] - 2) * step)
                                        )

        self.next_piece_surface = subsurface(self.background,
                                             (int(self.window.size[0] / 2) +
                                              10,
                                              int(self.window.size[1] / 2) +
                                              10,
                                              4 * step,
                                              4 * step)
                                             )


class Tesseract(object):

    def __init__(self):
        self.world = sdl2.ext.World()
        self.board = BD.Board(self.world)
        self.board_updater = BD.BoardUpdater()
        bsize = self.board.get_board_size()

        self.ws = WindowSystem(bsize)
        self.window, self.background = self.ws.window, self.ws.background

        self.piecefactory = PC.PieceFactory()
        self.virtual_piece_checker = PC.CollisionSystem()
        self.virtual_piece_checker.board = self.board

        self.current_piece = self.piecefactory.spawn_piece(self.world)
        self.board.piece = self.current_piece

        self.world.add_system(self.virtual_piece_checker)
        self.world.add_system(self.board_updater)

        self.window.show()

        self.boardrenderer = GS.BoardRenderer(self.ws.board_surface,
                                              self.board)

        self.np_board = BD.Board(self.world, [[0, 0, 0, 0], [0, 0, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0]])

        self.next_piece_renderer = GS.BoardRenderer(self.ws.next_piece_surface,
                                                    self.np_board, 0, True)

        self.boardrenderer.render_board(self.current_piece)
        self.next_piece = self.piecefactory.get_next_piece(self.world)
        self.np_board.piece = self.next_piece

    def process_input(self):
        events = sdl2.ext.get_events()
        running = True
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.current_piece.move_right()

                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.current_piece.move_left()

                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.current_piece.rotate()

                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.current_piece.drop()
        return running

    def update(self):
        if sdl2.SDL_GetTicks() - self.last_time >= 1000:
            self.current_piece.move_down()

            self.world.process()

            if self.current_piece.piecedata.blocked:
                self.board.boardstatus.to_update = True
                self.world.process()
                self.current_piece.delete()
                self.current_piece = self.piecefactory.spawn_piece(
                    self.world)

                self.board.piece = self.current_piece

                self.next_piece.delete()
                self.next_piece = self.piecefactory.get_next_piece(
                    self.world)
                self.np_board.piece = self.next_piece

            self.world.process()
            self.last_time = sdl2.SDL_GetTicks()

        self.world.process()

    def render(self):
        fill(self.ws.background, CONST.BLACK)
        fill(self.ws.board_background, CONST.GREY)

        self.boardrenderer.render_board(self.current_piece)
        self.next_piece_renderer.render_board(self.next_piece)
        self.window.refresh()

    def run(self):
        running = True
        self.last_time = sdl2.SDL_GetTicks()
        while running:
            running = self.process_input()
            self.update()
            self.render()
        return 0
