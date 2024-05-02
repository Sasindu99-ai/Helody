from PyQt5.QtWidgets import QWidget
from Core import Window
from Util import UI

__all__ = ['View']


class View(QWidget):
    parent: Window

    def __init__(self, parent: Window, name: str = None):
        self.parent = parent

        super(View, self).__init__()
        super(View, self).setParent(self.parent)

        if name:
            self.setObjectName(name)

    def dp(self, unit: int) -> int:
        return UI.dp(unit, self.devicePixelRatio())

    def sp(self, unit: int) -> int:
        return UI.sp(unit, self.devicePixelRatio())
