from PyQt5.QtCore import QMargins

__all__ = ["Margin"]


class Margin(QMargins):
    """
    Margin(int)
    Margin(vertical: int = None, horizontal: int = None)
    Margin(left: int, top: int, right: int, bottom: int)
    """

    def __init__(self, *__args, **__kwargs):
        super().__init__()

        left: int
        top: int
        right: int
        bottom: int

        if len(__args) == 1:
            a0: int = __args[0]
            left, top, right, bottom = a0, a0, a0, a0
        elif 0 < len(__kwargs.keys()) <= 2:
            horizontal = __kwargs[
                "horizontal"] if "horizontal" in __kwargs.keys() else 0
            vertical = __kwargs["vertical"] if "vertical" in __kwargs.keys(
            ) else 0
            left, right = horizontal, horizontal
            top, bottom = vertical, vertical
        else:
            left = __kwargs["left"] if "left" in __kwargs.keys() else 0
            top = __kwargs["top"] if "top" in __kwargs.keys() else 0
            right = __kwargs["right"] if "right" in __kwargs.keys() else 0
            bottom = __kwargs["bottom"] if "bottom" in __kwargs.keys() else 0

        self.setLeft(left)
        self.setTop(top)
        self.setRight(right)
        self.setBottom(bottom)
