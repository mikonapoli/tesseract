import pygame


class WindowSystem(object):
    @staticmethod
    def initialise():
        """Initialises the windowing system and returns the main surface"""
        pygame.init()
        pygame.display.set_caption("TESSERACT: A Tetris clone")

        pygame.mouse.set_visible(False)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #screen = pygame.display.set_mode((640, 480))
        screen.fill((0, 0, 0))
        pygame.display.update()

        return screen

    @staticmethod
    def get_center(surface):
        x = int(surface.get_width() / 2)
        y = int(surface.get_height() / 2)
        return (x, y)


class TextRenderer(object):

    @staticmethod
    def get_text_surface(text, size):
        font = pygame.font.SysFont("None", size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        return text_surface

    @classmethod
    def render_message_on_surface(cls, writing_surface, msg, size=64):
        lines = msg.split('\n')
        lines_surfaces = [cls.get_text_surface(line, size) for line in lines]
        text = msg
        cx, cy = WindowSystem.get_center(writing_surface)
        y_offset = int(sum((ts.get_height() for ts in lines_surfaces)) * 0.55)
        y = cy - y_offset
        for text_surface in lines_surfaces:
            x = cx - int(text_surface.get_width() * 0.5)
            writing_surface.blit(text_surface, (x, y))
            y += int(text_surface.get_height() * 1.1)
        pygame.display.flip()


class Tesseract(object):
    def __init__(self):
        self.screen = WindowSystem.initialise()
        self._setup_main_screen()

    def _setup_main_screen(self):
        title = """
        TESSERACT

        Press [ESC] to exit
        """
        TextRenderer.render_message_on_surface(self.screen, title)

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
    Tesseract().run()
