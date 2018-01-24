import sys
from legacy import Tesseract

if __name__ == "__main__":
    game = Tesseract.Game()
    sys.exit(game.run())
