import pygame


class Game(object):
    def __init__(self):
        self.screen = self._init_window_system()

    def _init_window_system(self):
        """Initialises the windowing system and returns the main surface"""
        pygame.init()
        pygame.display.set_caption("TESSERACT: A Tetris clone")

        pygame.mouse.set_visible(False)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))
        pygame.display.update()

        return screen

    def get_center(self, surface):
        x = int(surface.get_width() / 2)
        y = int(surface.get_height() / 2)
        return (x, y)

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
