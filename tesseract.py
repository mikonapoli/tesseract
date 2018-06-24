import pygame


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TESSERACT: A Tetris clone")

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))
        pygame.mouse.set_visible(False)

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False


if __name__ == "__main__":
    Game().run()
