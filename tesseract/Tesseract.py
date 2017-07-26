import sys
import sdl2
import sdl2.ext
import graphics.renderers as GS

import constants as CONST

import Piece as PC

import Board as BD


class Tesseract(object):

    def __init__(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Tesseract", size=(800, 600))
        self.background = self.window.get_surface()
        window = self.window
        self.world = sdl2.ext.World()

        self.board = BD.Board(self.world)
        bsize = self.board.get_board_size()
        self.board_updater = BD.BoardUpdater()

        step = min(30, int((window.size[0] - 20) / ((bsize[0] + 2) * 2)),
                   int((window.size[1] - 20) / (bsize[1])))

        self.board_background = sdl2.ext.subsurface(
            self.background, (10, 10, (bsize[0] + 2) * step,
                              (bsize[1]) * step))

        self.board_surface = sdl2.ext.subsurface(self.board_background,
                                                 (step, step, bsize[0] * step,
                                                  (bsize[1] - 2) * step))
        self.next_piece_surface = sdl2.ext.subsurface(self.background, (int(
            window.size[0] / 2) + 10,
            int(window.size[1] / 2) + 10, 4 * step, 4 * step))

        self.piecefactory = PC.PieceFactory()
        self.virtual_piece_checker = PC.VirtualPieceChecker(self.board)

        self.current_piece = self.piecefactory.spawn_piece(self.world)
        self.board.piece = self.current_piece

        self.world.add_system(self.virtual_piece_checker)
        self.world.add_system(self.board_updater)

        window.show()

        self.boardrenderer = GS.BoardRenderer(self.board_surface, self.board)

        self.np_board = BD.Board(self.world, [[0, 0, 0, 0], [0, 0, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0]])

        self.next_piece_renderer = GS.BoardRenderer(self.next_piece_surface,
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
        sdl2.ext.fill(self.background, CONST.BLACK)
        sdl2.ext.fill(self.board_background, CONST.GREY)

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

if __name__ == "__main__":
    game = Tesseract()
    sys.exit(game.run())
