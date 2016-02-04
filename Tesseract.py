import sys
import sdl2
import sdl2.ext
from GraphicSystem import *

from constants import *

from Piece import *

from Board import *
    

        
def run():
    #Initialize graphic system and control systems
    sdl2.ext.init()
    window = sdl2.ext.Window("Tetris", size = (800,600))
    background = window.get_surface()
    world = sdl2.ext.World()

    board = Board(world)
    bsize = board.get_board_size()
    board_updater = BoardUpdater()
    
    step = min(30,int((window.size[0]-20)/(bsize[0]*2)), int((window.size[1]-20)/(bsize[1]-2)))

    board_surface = sdl2.ext.subsurface(background, (10,10,bsize[0]*step,(bsize[1]-2)*step))
    next_piece_surface = sdl2.ext.subsurface(background, (int(window.size[0]/2) + 10, int(window.size[1]/2) +10, 4*step, 4*step))
    
    
    piecefactory = PieceFactory()
    virtual_piece_checker = VirtualPieceChecker(board)
    piece_mover = PieceMovement()


    current_piece = piecefactory.spawn_piece(world)
    board.piece = current_piece
    
    world.add_system(virtual_piece_checker)
    world.add_system(board_updater)

    window.show()
        
    boardrenderer = BoardRenderer(board_surface, board)
    
    np_board = Board(world, [ [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0] ])
    
    
    next_piece_renderer = BoardRenderer(next_piece_surface, np_board, 0, True)
    
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
                    piece_mover.move_right(current_piece)
                    world.process()
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    piece_mover.move_left(current_piece)
                    world.process()
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    piece_mover.rotate(current_piece)
                    world.process()
                if event.key.keysym.sym == sdl2.SDLK_DOWN:
                    while not current_piece.piecedata.blocked:
                        
                        piece_mover.move_down(current_piece)
                        world.process()
    
                    world.process()

                    
        sdl2.ext.fill(background,WHITE)

        if sdl2.SDL_GetTicks() - last_time >= 1000:
            piece_mover.move_down(current_piece)

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
                #print(np_board.piece.piecedata.type)
                

            world.process()
            last_time = sdl2.SDL_GetTicks()

        world.process()

        boardrenderer.render_board(current_piece)
        next_piece_renderer.render_board(next_piece)
        #print(next_piece.piecedata.boardposition.x, next_piece.piecedata.boardposition.y)
        window.refresh()
    return 0

if __name__ == "__main__":
    sys.exit(run())