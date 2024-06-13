import os
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QFileDialog
from tinytag import TinyTag

from Components.Common.Button import Button
from Components.Common.Menu import Menu
from Components.Common.Seperator import Seperator
from Core import Player, Window
from lib import Color, Images, db
from Models import Playlist, Song
from Util import UI, Styles
from Views import HomeView, PlayListsView

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOTPATH)


class Helody(Window):
    menu: Menu
    player: Player

    def __init__(self):
        super(Helody, self).__init__(row=2, column=2)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Helody")
        self.setWindowIcon(
            QIcon(
                UI.pixmap(Images.icon, 32, 32, Qt.KeepAspectRatioByExpanding,
                          Qt.SmoothTransformation)))
        self.setFocusPolicy(Qt.StrongFocus)
        pal = self.palette()
        pal.setColor(QPalette.Background, Color.theme.background)
        pal.setColor(QPalette.Foreground, Color.theme.foreground)
        self.setPalette(pal)
        self.setFocus()
        self.setStyleSheet("""
        QMainWindow {background-color: """ +
                           UI.colorHex(Color.theme.background.getRgb()) + """;}
        """)

        self.setUpMenu()
        self.setupPlayer()

        self.navigate(HomeView)

        self.show()

    def setUpMenu(self):  # noqa
        self.menu = Menu(self)

        self.menu.menu = Button(Images.menu, "menu", style=Styles.menuButton)

        self.menu.seperator = Seperator(Qt.Horizontal, 6,
                                        Color.theme.seperator)
        self.menu.seperator.setMinimumHeight(3)
        self.menu.seperator.setContentsMargins(5, 6, 5, 10)

        self.menu.home = Button(Images.home,
                                "home",
                                style=Styles.menuButton,
                                action=lambda: self.navigate(HomeView))

        self.menu.playlist = Button(
            Images.playlist,
            "playlists",
            style=Styles.menuButton,
            action=lambda: self.navigate(PlayListsView))

        self.menu.explore = Button(Images.explore,
                                   "explore",
                                   style=Styles.menuButton)

        self.menu.settings = Button(Images.settings,
                                    "settings",
                                    style=Styles.menuButton)

        # [Add Widgets]
        self.menu.layout.addWidget(self.menu.menu)
        self.menu.layout.addWidget(self.menu.seperator)
        self.menu.layout.addWidget(self.menu.home)
        self.menu.layout.addWidget(self.menu.playlist)
        self.menu.layout.addWidget(self.menu.explore)
        self.menu.layout.addStretch()
        self.menu.layout.addWidget(self.menu.settings)

        self.mainLayout.addWidget(self.menu, 2, 1, 1, 1)

    def setupPlayer(self):  # noqa
        self.player = Player(self)

    def openFiles(self, playlist: Playlist, load: bool = False):  # noqa
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open file", "", "mp3 Audio (*.mp3, *.m4a)All files (*.*)")
        if paths:
            self.player.stop()
            for path in paths:
                if path.endswith(".mp3") or path.endswith(".m4a"):
                    tag = TinyTag.get(path)

                    song = Song()
                    song.path = path
                    song.title = tag.title if tag.title else ".".join(
                        ((path.split("/"))[-1]).split(".")[:-1])
                    song.genre = tag.genre if tag.genre else "Unknown"
                    song.album = tag.album if tag.album else "Unknown"
                    song.artist = tag.artist if tag.artist else "Unknown"
                    song.modifiedDate = datetime.fromtimestamp(
                        os.stat(path).st_mtime)

                    song.playlists.append(playlist)

                    db.session.add(song)
            db.session.commit()

            if load:
                self.player.loadPlayList()
