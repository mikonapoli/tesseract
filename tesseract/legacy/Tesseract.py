import sdl2
from sdl2.ext import init as init_graphic_system
from sdl2.ext import Window, World, subsurface, fill

import legacy.graphics.renderers as GS
import legacy.graphics.constants as CONST
from . import Piece as PC
from . import Board as BD


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

        self.window.show()


class GameWorld():

    def __init__(self):
        self.world = World()
        self.board = BD.Board(self.world)
        self.board_updater = BD.BoardUpdater()

        self.piecefactory = PC.PieceFactory()
        self.virtual_piece_checker = PC.CollisionSystem()
        self.virtual_piece_checker.board = self.board

        self.current_piece = self.piecefactory.spawn_piece(self.world)
        self.board.piece = self.current_piece

        self.world.add_system(self.virtual_piece_checker)
        self.world.add_system(self.board_updater)

        self.np_board = BD.Board(self.world,
                                 [[0, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]])

        self.next_piece = self.piecefactory.get_next_piece(self.world)
        self.np_board.piece = self.next_piece


class GraphicSystem():

    def __init__(self, window_system, game_world):
        self.ws = window_system
        self.gw = game_world

        self.boardrenderer = GS.BoardRenderer(self.ws.board_surface,
                                              self.gw.board)

        self.next_piece_renderer = GS.BoardRenderer(self.ws.next_piece_surface,
                                                    self.gw.np_board, 0, True)

        self.boardrenderer.render_board(self.gw.current_piece)

    def render_background(self):
        fill(self.ws.background, CONST.BLACK)
        fill(self.ws.board_background, CONST.GREY)

    def render_game_world(self):
        self.boardrenderer.render_board(self.gw.current_piece)
        self.next_piece_renderer.render_board(self.gw.next_piece)

    def render(self):
        self.render_background()
        self.render_game_world()

        self.ws.window.refresh()


class InputSystem():
    def __init__(self):
        self.stopped = False

    def process_input(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.stopped = True
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.stopped = True
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.gw.current_piece.move_right()

                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.gw.current_piece.move_left()

                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.gw.current_piece.rotate()

                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.gw.current_piece.drop()
        return not self.stopped


class Tesseract():

    def __init__(self):
        self.gw = GameWorld()

        bsize = self.gw.board.get_size()

        self.ws = WindowSystem(bsize)

        self.gs = GraphicSystem(self.ws, self.gw)

        self.ins = InputSystem()

    def update(self):
        if sdl2.SDL_GetTicks() - self.last_time >= 1000:
            self.gw.current_piece.move_down()

            self.gw.world.process()

            if self.gw.current_piece.piecedata.blocked:
                self.gw.board.boardstatus.to_update = True
                self.gw.world.process()
                self.gw.current_piece.delete()
                self.gw.current_piece = self.gw.piecefactory.spawn_piece(
                    self.gw.world)

                self.gw.board.piece = self.gw.current_piece

                self.gw.next_piece.delete()
                self.gw.next_piece = self.gw.piecefactory.get_next_piece(
                    self.gw.world)
                self.gw.np_board.piece = self.gw.next_piece

            self.gw.world.process()
            self.last_time = sdl2.SDL_GetTicks()

        self.gw.world.process()

    def run(self):
        running = True
        self.last_time = sdl2.SDL_GetTicks()
        while running:
            running = self.ins.process_input()
            self.update()
            self.gs.render()
        return 0
