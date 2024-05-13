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
        """
        This method is used to convert the given unit to device-independent pixels.
        dp(self, unit: int) -> int
        :param unit: int
        :return: int
        """
        return UI.dp(unit, self.devicePixelRatio())

    def sp(self, unit: int) -> int:
        """
        This method is used to convert the given unit to scaled pixels.
        sp(self, unit: int) -> int
        :param unit: int
        :return: int
        """
        return UI.sp(unit, self.devicePixelRatio())

    def onCreate(self):  # noqa
        """ onCreate(self) """
        pass

    def onResume(self):  # noqa
        """ onResume(self) """
        pass
