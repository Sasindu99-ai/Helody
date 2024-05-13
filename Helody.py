import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette

from Components import Menu, Button, Seperator
from Core import Window, Player
from Util import UI, Styles
from Views import HomeView, PlayListsView
from lib import Images, Color

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOTPATH)


class Helody(Window):
    menu: Menu
    player: Player

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
        QMainWindow {background-color: """ + UI.colorHex(Color.theme.background.getRgb()) + """;}
        """)

        self.setUpMenu()
        self.setupPlayer()

        self.navigate(HomeView)

        self.show()

    def setUpMenu(self): # noqa
        self.menu = Menu(self)

        self.menu.menu = Button(Images.menu, "menu", style=Styles.menuButton)

        self.menu.seperator = Seperator(Qt.Horizontal, 6, Color.theme.seperator)
        self.menu.seperator.setMinimumHeight(3)
        self.menu.seperator.setContentsMargins(5, 6, 5, 10)

        self.menu.home = Button(Images.home, "home", style=Styles.menuButton,
                                action=lambda: self.navigate(HomeView))

        self.menu.playlist = Button(Images.playlist, "playlists", style=Styles.menuButton,
                                    action=lambda: self.navigate(PlayListsView))

        self.menu.explore = Button(Images.explore, "explore", style=Styles.menuButton)

        self.menu.settings = Button(Images.settings, "settings", style=Styles.menuButton)

        # [Add Widgets]
        self.menu.layout.addWidget(self.menu.menu)
        self.menu.layout.addWidget(self.menu.seperator)
        self.menu.layout.addWidget(self.menu.home)
        self.menu.layout.addWidget(self.menu.playlist)
        self.menu.layout.addWidget(self.menu.explore)
        self.menu.layout.addStretch()
        self.menu.layout.addWidget(self.menu.settings)

        self.mainLayout.addWidget(self.menu, 2, 1, 1, 1)

    def setupPlayer(self): # noqa
        self.player = Player(self)
