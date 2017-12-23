import sys
from legacy.Tesseract import Tesseract


if __name__ == "__main__":
    game = Tesseract()
    sys.exit(game.run())
