import enum
from typing import Any

from PyQt5.QtWidgets import QWidget, QLayout, QVBoxLayout

from Core import Window
from Util import UI

__all__ = ["Menu", "Tabs"]

from Views import HomeView, PlayListsView


class Tabs(enum.Enum):
    HomeView = HomeView
    PlayListsView = PlayListsView


class Menu(QWidget):
    layout: QLayout
    root: Window
    activeTab: Tabs = Tabs.HomeView

    def __init__(self, root: Window):
        super(Menu, self).__init__()

        self.root = root

        self.setFixedWidth(self.dp(16) + 10)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def setCurrentTab(self, tab: Tabs): # noqa
        self.activeTab = tab

    def navigate(self, view: Any):
        if self.activeTab != view:
            self.root.navigate(view)

    def dp(self, unit: int):
        return UI.dp(unit, self.devicePixelRatio())
