from Core.Window import Window


class Player:
    parent: Window

    def __init__(self, parent: Window):
        self.parent = parent
