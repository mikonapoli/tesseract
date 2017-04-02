import sys
import sdl2
import sdl2.ext
import GraphicSystem as GS

import constants as CONST

import Piece as PC

import Board as BD


def run():
    # Initialize graphic system and control systems
    sdl2.ext.init()
    window = sdl2.ext.Window("Tesseract", size=(800, 600))
    background = window.get_surface()
    world = sdl2.ext.World()

    board = BD.Board(world)
    bsize = board.get_board_size()
    board_updater = BD.BoardUpdater()

    step = min(30, int((window.size[0] - 20) / ((bsize[0] + 2) * 2)),
               int((window.size[1] - 20) / (bsize[1])))

    board_background = sdl2.ext.subsurface(
        background, (10, 10, (bsize[0] + 2) * step, (bsize[1]) * step))

    board_surface = sdl2.ext.subsurface(board_background,
                                        (step, step, bsize[0] * step,
                                         (bsize[1] - 2) * step))
    next_piece_surface = sdl2.ext.subsurface(background, (int(
        window.size[0] / 2) + 10,
        int(window.size[1] / 2) + 10, 4 * step, 4 * step))

    piecefactory = PC.PieceFactory()
    virtual_piece_checker = PC.VirtualPieceChecker(board)

    current_piece = piecefactory.spawn_piece(world)
    board.piece = current_piece

    world.add_system(virtual_piece_checker)
    world.add_system(board_updater)

    window.show()

    boardrenderer = GS.BoardRenderer(board_surface, board)

    np_board = BD.Board(world, [[0, 0, 0, 0], [0, 0, 0, 0], [
        0, 0, 0, 0], [0, 0, 0, 0]])

    next_piece_renderer = GS.BoardRenderer(next_piece_surface,
                                           np_board, 0, True)

    boardrenderer.render_board(current_piece)
    next_piece = piecefactory.get_next_piece(world)
    np_board.piece = next_piece

    running = True
    last_time = sdl2.SDL_GetTicks()
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    current_piece.move_right()

                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    current_piece.move_left()

                if event.key.keysym.sym == sdl2.SDLK_UP:
                    current_piece.rotate()

                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    current_piece.drop()

                world.process()

        sdl2.ext.fill(background, CONST.BLACK)
        sdl2.ext.fill(board_background, CONST.WHITE)

        if sdl2.SDL_GetTicks() - last_time >= 1000:
            current_piece.move_down()

            world.process()

            if current_piece.piecedata.blocked:
                board.boardstatus.to_update = True
                world.process()
                current_piece.delete()
                current_piece = piecefactory.spawn_piece(world)

                board.piece = current_piece

                next_piece.delete()
                next_piece = piecefactory.get_next_piece(world)
                np_board.piece = next_piece

            world.process()
            last_time = sdl2.SDL_GetTicks()

        world.process()

        boardrenderer.render_board(current_piece)
        next_piece_renderer.render_board(next_piece)
        window.refresh()
    return 0

if __name__ == "__main__":
    sys.exit(run())
