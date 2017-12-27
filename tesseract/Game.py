class GameState():
    name: str

    def __init__(self, name: str = "Generic State") -> None:
        self.name = name


class RunningState(GameState):
    def __init__(self) -> None:
        super().__init__("RUNNING")
        print(self.name)


class Game():
    state: GameState

    def __init__(self) -> None:
        self.state = RunningState()
