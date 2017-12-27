class GameState():
    def __init__(self):
        pass


class Game():
    state: GameState

    def __init__(self) -> None:
        self.state = GameState()
