import pygame


class Game(object):
    def __init__(self):
        self.screen = self._init_window_system()
        self._setup_main_screen()

    def _init_window_system(self):
        """Initialises the windowing system and returns the main surface"""
        pygame.init()
        pygame.display.set_caption("TESSERACT: A Tetris clone")

        pygame.mouse.set_visible(False)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #screen = pygame.display.set_mode((640, 480))
        screen.fill((0, 0, 0))
        pygame.display.update()

        return screen

    def _setup_main_screen(self):
        title = """TESSERACT: A Tetris clone\nPress [ESC] to exit"""
        self.render_text_on_surface(self.screen, title)

    def get_center(self, surface):
        x = int(surface.get_width() / 2)
        y = int(surface.get_height() / 2)
        return (x, y)

    def write_text(self, text, size):
        font = pygame.font.SysFont("None", size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        return text_surface

    def render_text_on_surface(self, writing_surface, text, size=48):
        x, y = self.get_center(writing_surface)
        text_surface = self.write_text(text, size)
        x -= int(text_surface.get_width() / 2)
        y -= int(text_surface.get_height() / 2)
        writing_surface.blit(text_surface, (x, y))
        pygame.display.flip()

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
