import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette

from Components.Common.Menu import Menu
from Components.Common.MenuButton import MenuButton
from Components.Common.Seperator import Seperator
from Core import Window
from Util import UI
from Views import HomeView, PlayListsView
from lib import Images, Color

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOTPATH)


class Helody(Window):
    menu: Menu

    def __init__(self):
        super(Helody, self).__init__(row=2, column=2)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Helody")
        self.setWindowIcon(QIcon(UI.pixmap(Images.icon, 32, 32, Qt.KeepAspectRatioByExpanding,
                                           Qt.SmoothTransformation)))
        self.setFocusPolicy(Qt.StrongFocus)
        pal = self.palette()
        pal.setColor(QPalette.Background, Color.theme.background)
        pal.setColor(QPalette.Foreground, Color.theme.foreground)
        self.setPalette(pal)
        self.setFocus()
        self.setStyleSheet("""
        QMainWindow {background-color: """ + UI.colorHex(Color.theme.background.getRgb()) + """;}""")

        self.setUpMenu()

        self.navigate(HomeView)

        self.show()

    def setUpMenu(self): # noqa
        self.menu = Menu(self)

        self.menu.menu = MenuButton(Images.menu, "menu")

        self.menu.seperator = Seperator(Qt.Horizontal, 6, Color.theme.seperator)
        self.menu.seperator.setMinimumHeight(3)
        self.menu.seperator.setContentsMargins(5, 6, 5, 10)

        self.menu.home = MenuButton(Images.home, "home")
        self.menu.home.onClick(lambda: self.navigate(HomeView))

        self.menu.playlist = MenuButton(Images.playlist, "playlists")
        self.menu.playlist.onClick(lambda: self.navigate(PlayListsView))

        self.menu.explore = MenuButton(Images.explore, "explore")

        self.menu.settings = MenuButton(Images.settings, "settings")

        # [Add Widgets]
        self.menu.layout.addWidget(self.menu.menu)
        self.menu.layout.addWidget(self.menu.seperator)
        self.menu.layout.addWidget(self.menu.home)
        self.menu.layout.addWidget(self.menu.playlist)
        self.menu.layout.addWidget(self.menu.explore)
        self.menu.layout.addStretch()
        self.menu.layout.addWidget(self.menu.settings)

        self.mainLayout.addWidget(self.menu, 2, 1, 1, 1)
