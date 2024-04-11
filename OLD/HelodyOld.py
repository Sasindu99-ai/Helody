__author__ = "Sasindu Sulochana"
__project__ = "scprt003"
__version__ = "1.7.0.0"
__last_modified_date__ = '07.02.2023'

import os
import sys
import base64
import ctypes
import json
import time
import random
import subprocess
from operator import itemgetter
from tinytag import TinyTag
import eyed3
import urllib.request
from youtube_dl import YoutubeDL
from urllib.parse import quote, unquote
import codecs
from ctypes import wintypes
from mutagen.mp4 import MP4
import io
from PIL.Image import Image, Image
import sqlite3
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QTimer, QThread, pyqtSignal, QObject, QAbstractListModel, QUrl, \
    QPoint, QEvent, QRect
from PyQt5.QtGui import QColor, QCursor, QIcon, QPixmap, QWindow, QScreen, QPalette, QPainter, QImage, QPainterPath, \
    QFontMetrics, QTextLayout, QTextOption, QGradient, QMovie, QFont, QBrush, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QSizePolicy, QHBoxLayout, QMainWindow, \
    QToolButton, QLineEdit, QLabel, QGridLayout, QScrollArea, QScrollBar, QScroller, QAction, QDialog, QFrame, QSlider, \
    QStackedWidget, QFileDialog, QLayout, QStyle, QStyleOption, QMenu, QSpacerItem, QSplitter, QWidgetItem, \
    QGraphicsDropShadowEffect, QGraphicsBlurEffect, QTextEdit, QMessageBox, QStyleOptionSlider, QToolTip, \
    QStyleOptionButton, QTabWidget, QListView
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWinExtras import QtWin
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import logging

""" program data paths """
helodyrealpath = os.getcwd()
home_dir = os.path.expanduser("~")
if "/" in home_dir: home_dir = "\\".join(home_dir.split("/"))
local_user = home_dir.split("\\")[-1]
if '/' in helodyrealpath: helodyrealpath = "\\".join(helodyreapath.split("/"))
resourcedir = "{}\\lib\\resources".format(helodyrealpath)
musicdir = "C:\\Users\\{}\\Music\\Helody".format(local_user)

""" checking Application paths """
try:
    if not os.path.exists(musicdir):
        os.mkdir(musicdir)
except FileNotFoundError:
    musicdir = "C:\\Users\\{}\\onedrive\\Music\\LinkedUP".format(local_user)
    if not os.path.exists(musicdir):
        os.mkdir(musicdir)


def getexistance():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    tasks = [line.decode().rstrip() for line in proc.stdout]
    thcount = tasks.count("Helody")
    print("tasks", tasks, thcount)
    if thcount == 0:  # TODO: chabge to 1 when exceuting
        return True
    else:
        return False


def read_file(rfile):
    with open(r"{}".format(rfile), "rb") as File:
        return (base64.b64decode(File.read()).decode('utf-8'))


def write_file(wfile, txt):
    with open(r"{}".format(wfile), "wb") as File:
        File.write(base64.b64encode(("{}".format(txt)).encode('utf-8')))


def create_file(cfile, data=None):
    file = open(r"{}".format(cfile), "x")
    file.close()
    if data != None:
        write_file(cfile, data)


def encode_text(text):
    code = base64.b64encode(("{}".format(text)).encode('utf-8'))
    return code


def decode_code(code):
    text = (base64.b64decode("{}".format(code)).decode('utf-8'))
    return text


def decode_lyric(lyric_txt=""):
    lyric_list = lyric_txt.split("\n")
    lyric = {}
    start = 0
    for i, x in enumerate(lyric_list):
        if x.startswith("[00"):
            start = i
            break
    for i in range(i, len(lyric_list)):
        try:
            time, text = lyric_list[i].split("]")
            lyric[f"00:{'%02d' % int(time[1:3])}:{'%02d' % int(time[4:6])}"] = text.strip()
        except Exception as e:
            pass
    return lyric


def scover(file):
    try:
        if file.endswith(".mp3"):
            # mp3 = stagger.read_tag(file)
            # im = io.BytesIO(mp3[stagger.id3.APIC][0].data)
            return ""
        if file.endswith(".m4a"):
            m4a = MP4(file)
            return io.BytesIO(m4a.tags.get("covr", [None])[-1])
    except Exception:
        pass


def clearLayout(layout):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)

        if isinstance(item, QWidgetItem):
            item.widget().close()
        elif isinstance(item, QSpacerItem):
            pass
        else:
            pass
        layout.removeItem(item)


def clearLayoutSpaces(layout):
    try:
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            layout.removeItem(item) if isinstance(item, QSpacerItem) else clearLayout(item.layout())
    except AttributeError:
        pass


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", wintypes.POINT),
        ("ptMaxSize", wintypes.POINT),
        ("ptMaxPosition", wintypes.POINT),
        ("ptMinTrackSize", wintypes.POINT),
        ("ptMaxTrackSize", wintypes.POINT),
    ]


class Setting:
    index = 0
    volume = 100
    theme = "light"
    playingList = "playlist"
    overplayvalue = 1
    sorttype = "Name"
    sortside = "Ascending"
    paused = True
    volumebuttonstatus = True
    selectinglist = ""

    defaults = {
        "light": {
            "bg": "#EBEBEB",
            "fg": "#000000"
        },

        "dark": {
            "bg": "#DFDFDF",
            "fg": "#FFFFFF"
        }
    }

    def __init__(self):
        self.setUp()

    def setUp(self):
        settings_cache = controller.getSettings()

    def themeinfo(self, name):
        return self.__class__.defaults[self.theme][name]


class DBController:
    def __init__(self):
        self.DB = sqlite3('helody.db')

    def getSettings(self):
        cursor = self.DB.execute("SELECT * FROM settings")
        return cursor

    def getSong(playingList, index):
        return {"no": 0,
                "song": "J:/My music/Favourite Songs/_Beauty And A Beat_ - Justin Bieber (Alex Goot, Kurt Schneider, and Chrissy Costanza Cover) ( 256kbps cbr ).mp3",
                "name": "\"Beauty And A Beat\" - Justin Bieber (Alex Goot, Kurt Schneider, and Chrissy Costanza Cover)",
                "genre": "Unknown", "album": "Unknown", "artist": "gootmusic", "date": 20181104013932, "lyricsync": 0}


class API:
    def __init__(self):
        pass


class EliderLabel(QLabel):

    def __init__(self, text='', mode=Qt.ElideRight, textAlignment=Qt.AlignLeft, **kwargs):
        super().__init__(**kwargs)

        self._mode = mode
        self.elided = False
        self.textAlignment = textAlignment

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText(text)

    def setText(self, text):
        self._contents = text
        self.update()

    def setAlignment(self, alignment):
        super(EliderLabel, self).setAlignment(alignment)
        self.textAlignment = alignment

    def text(self):
        return self._contents

    def minimumSizeHint(self):
        metrics = QFontMetrics(self.font())
        return QSize(0, metrics.height())

    def paintEvent(self, event):
        super().paintEvent(event)
        did_elide = False
        painter = QPainter(self)
        font_metrics = painter.fontMetrics()

        text_width = font_metrics.horizontalAdvance(self.text())

        text_layout = QTextLayout(self._contents, painter.font())
        text_layout.beginLayout()

        while True:
            line = text_layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(self.width())
            if text_width >= self.width():
                elided_line = font_metrics.elidedText(self._contents, self._mode, self.width())
                if elided_line:
                    painter.drawText(QPoint(0, font_metrics.ascent()), elided_line)
                did_elide = line.isValid()
                break
            else:
                painter.drawText(0, 0, event.rect().width(), event.rect().height(), self.textAlignment, self.text())

        text_layout.endLayout()

        if did_elide != self.elided:
            self.elided = did_elide

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(0, 0, event.rect().width(), event.rect().height(), Qt.AlignCenter, self.text())


class ImageLabel(QWidget):
    def __init__(self, pixmap=None, antialiasing=True):
        super(ImageLabel, self).__init__()

        self.setStyleSheet("""
        ImageLabel {
            background: black;
        }
        """)

        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.image = ImageViewer(pixmap, antialiasing)

        self._layout.addWidget(self.image, alignment=Qt.AlignCenter)

    def setPixmap(self, pixmap):
        self.image.setPixmap(pixmap)

    def setHeight(self, width, height):
        self.image.setHeight(width, height)


class ImageViewer(QLabel):
    pixmap = None
    _sizeHint = QSize()
    ratio = Qt.KeepAspectRatioByExpanding
    transformation = Qt.SmoothTransformation

    def __init__(self, pixmap=None, antialiasing=True):
        super().__init__()
        self.Antialiasing = antialiasing
        self.radius = 0
        self.setPixmap(pixmap)

    def setPixmap(self, pixmap):
        if self.pixmap != pixmap:
            self.pixmap = pixmap
            if isinstance(pixmap, QPixmap):
                self._sizeHint = pixmap.size()
            else:
                self._sizeHint = QSize()
            self.updateGeometry()
            self.updateScaled()

    def setAspectRatio(self, ratio):
        if self.ratio != ratio:
            self.ratio = ratio
            self.updateScaled()

    def setTransformation(self, transformation):
        if self.transformation != transformation:
            self.transformation = transformation
            self.updateScaled()

    def updateScaled(self):
        if self.pixmap:
            self.scaled = self.pixmap.scaled(self.size(), self.ratio, self.transformation)
        self.update()

    def sizeHint(self):
        return self._sizeHint

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateScaled()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        qp = QPainter(self)
        r = self.scaled.rect()
        r.moveCenter(self.rect().center())
        if self.Antialiasing:
            qp.setRenderHint(QPainter.Antialiasing, True)
            qp.setRenderHint(QPainter.HighQualityAntialiasing, True)
            qp.setRenderHint(QPainter.SmoothPixmapTransform, True)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        qp.setClipPath(path)
        qp.drawPixmap(r, self.scaled)
        self.update()

    def setHeight(self, width, height):
        if width <= height:
            size = QSize(width, width)
            self.radius = width // 2
        if width > height:
            size = QSize(height, height)
            self.radius = height // 2
        if self.pixmap:
            self._sizeHint = size
            self.updateGeometry()
            self.scaled = self.pixmap.scaled(size, self.ratio, self.transformation)
            self.update()


class Slider(QSlider):
    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        if self.orientation() == Qt.Vertical:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin, sliderMax - sliderMin,
                                              opt.upsideDown)


class ScrollArea(QScrollArea):
    def wheelEvent(self, event):
        super(ScrollArea, self).wheelEvent(event)
        event.accept()


class TitleBar(QWidget):

    def __init__(self, parent, root):
        global images
        super().__init__()
        self.parent = parent
        self.root = root
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # set size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(32)
        self.setMouseTracking(True)

        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap(images[settings.theme]['helody']))
        self.icon.setContentsMargins(2, 2, 2, 2)
        self.icon.setFixedSize(QSize(106, 32))
        self.icon.setScaledContents(True)

        self.minimizeButton = QToolButton(self)
        self.minimizeButton.setIcon(QIcon(QPixmap(images[settings.theme]['minimizewinimg'])))
        self.minimizeButton.clicked.connect(self.parent.showMinimized)
        self.minimizeButton.setStyleSheet("""
        QToolButton{
            border: none;
            outline: none;
            background-color: #EBEBEB;
            color: black;
            width: 44px;
            font: 10px consolas;
        }
        QToolButton:hover{
           background-color: #DEDEDE;
        }
        """)
        self.minimizeButton.setContentsMargins(0, 0, 0, 0)
        self.minimizeButton.setIconSize(QSize(20, 20))
        self.minimizeButton.setFixedSize(QSize(40, 32))

        self.restoreButton = QToolButton(self)
        self.restoreButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizewinimg'])))
        self.restoreButton.clicked.connect(self.restore)
        self.restoreButton.setStyleSheet("""
        QToolButton{
            border: none;
            outline: none;
            background-color: #EBEBEB;
            color: black;
            width: 44px;
            font: 10px consolas;
        }
        QToolButton:hover{
            background-color: #DEDEDE;
        }
        """)
        self.restoreButton.setContentsMargins(0, 0, 0, 0)
        self.restoreButton.setIconSize(QSize(20, 20))
        self.restoreButton.setFixedSize(QSize(40, 32))

        self.closeButton = QToolButton(self)
        self.closeButton.setIcon(QIcon(QPixmap(images[settings.theme]['closeimg'])))
        self.closeButton.setIconSize(QSize(20, 20))
        self.closeButton.setFixedSize(QSize(40, 32))
        self.closeButton.clicked.connect(self.root.close)
        self.closeButton.setStyleSheet("""
        QToolButton{
            border: none;
            outline: none;
            background-color: #EBEBEB;
            color: black;
            width: 44px;
            font: 10px consolas;
        }

        QToolButton:hover{
            background-color: #F00000;
            color: white;
        }
        """)
        self.closeButton.setContentsMargins(0, 0, 0, 0)

        self.icon.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.icon.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.icon.setAttribute(Qt.WA_TranslucentBackground)

        # set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(settings.themeinfo('bg')))
        self.setPalette(p)

        self._layout.addWidget(self.icon, alignment=Qt.AlignLeft)
        self._layout.addStretch()
        l = QHBoxLayout()
        l.setSpacing(0)
        l.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(l)
        l.addWidget(self.minimizeButton, alignment=Qt.AlignRight)
        l.addWidget(self.restoreButton, alignment=Qt.AlignRight)
        l.addWidget(self.closeButton, alignment=Qt.AlignRight)
        self.setLayout(self._layout)

    def restore(self, e=None):
        if not self.parent.isMaximized():
            self.parent.showMaximized()
            self.restoreButton.setIcon(QIcon(QPixmap(images[settings.theme]['restoreimg'])))
        else:
            self.parent.showNormal()
            self.restoreButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizewinimg'])))


class Window(QWidget):
    BorderWidth = 5
    SESSION = {}
    WIDGETS = {}

    def __init__(self, width=800, height=600):
        super().__init__()
        self.setObjectName("MainWindow")
        # get the available resolutions without taskbar
        self._rect = QApplication.instance().desktop().availableGeometry(self)
        # self.resize(800, 600)
        self.setMinimumSize(QSize(540, 508))
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)

        self.current_screen = None

        # Create a thin frame
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        if QtWin.isCompositionEnabled():
            # Aero Shadow
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
            pass
        else:
            QtWin.resetExtendedFrame(self)

        # Window Widgets
        self._layout = QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.titleBar = TitleBar(self, self)
        self.titleBar.setObjectName("titleBar")

        # main widget is here
        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setHorizontalSpacing(0)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.mainWidget.setAutoFillBackground(True)
        p = self.mainWidget.palette()
        p.setColor(self.mainWidget.backgroundRole(), QColor(settings.themeinfo('bg')))
        self.mainWidget.setPalette(p)

        self.upperShadowWidget = QWidget()
        self.upperShadowLayout = QGridLayout(self.upperShadowWidget)
        self.upperShadowLayout.setSpacing(0)
        self.upperShadowLayout.setContentsMargins(0, 0, 0, 0)
        self.upperShadowWidget.setLayout(self.upperShadowLayout)

        self.setCursor(Qt.ArrowCursor)

        self._layout.addWidget(self.titleBar, 0, 0)
        self._layout.addWidget(self.mainWidget, 1, 0)
        self._layout.addWidget(self.upperShadowWidget, 1, 0)
        self.setLayout(self._layout)

        self.upperShadowWidget.setVisible(False)

        self.setWindowTitle("HELODY")
        self.windowicon = QPixmap()
        self.windowicon.load("lib\\resources\\helody.png")
        self.windowicon.scaled(32, 32, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setWindowIcon(QIcon(self.windowicon))
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.translate = QCoreApplication.translate
        self.lastrefreshSec = 0
        self.miniplayeron = False
        self.lyricSync = 0
        self.lastState = self.windowState()
        self.__class__.SESSION['selected_list'] = []
        self.player = QMediaPlayer()
        self.player.error.connect(self._handle_player_error)
        self.playlist = QMediaPlaylist()

        class playlistCreator(QObject):
            pack = pyqtSignal(dict)

            def __init__(self, root):
                super().__init__()
                self.root = root
                self.lastSec = False

            def setSec(self, sec):
                self.lastSec = sec

            def run(self):
                try:
                    clearLayout(self.root.playinglistWidgetLayout)
                except Exception as e:
                    pass
                self.root.WIDGETS['playlistitems'] = []
                for i, x in enumerate(listOfSongs):
                    if self.root.lastrefreshSec != self.lastSec: break
                    song = controller.getSong(settings.playingList, x)
                    self.pack.emit({"pack": i, "song": song, "sep": False})
                self.pack.emit({"sep": True})
                try:
                    self.root.WIDGETS['playlistitems'][settings.index].playUpdate()
                except (KeyError, IndexError):
                    pass

        self.playlistWorker = playlistCreator(self)
        self.playlistThread = QThread()
        self.playlistWorker.pack.connect(self.pack)
        self.playlistWorker.moveToThread(self.playlistThread)
        self.playlistThread.started.connect(self.playlistWorker.run)

        self.SetupUI()

        index = settings.index
        self.player.setPlaylist(self.playlist)
        self.playlist.setCurrentIndex(index)
        settings.index = index

        self.show()

        self.resize(QSize(width, height))
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.updateGeometry()

    def on_test_button_clicked(self):
        self.updateGeometry()

    def nativeEvent(self, eventType, message):
        retval, result = super().nativeEvent(eventType, message)

        # if you use Windows OS
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())

            # Get the coordinates when the mouse moves.
            # x = win32api.LOWORD(ctypes.c_long(msg.lParam).value) - self.frameGeometry().x()
            # y = win32api.HIWORD(ctypes.c_long(msg.lParam).value) - self.frameGeometry().y()

            x = win32api.LOWORD(ctypes.c_long(msg.lParam).value)
            if x & 32768: x = x | -65536
            y = win32api.HIWORD(ctypes.c_long(msg.lParam).value)
            if y & 32768: y = y | -65536

            x = x - self.frameGeometry().x()
            y = y - self.frameGeometry().y()

            # Determine whether there are other controls(i.e. widgets etc.) at the mouse position.
            if self.childAt(x, y) is not None and self.childAt(x, y) is not self.findChild(QWidget, "titleBar"):
                # passing
                if self.width() - 5 > x > 5 and y < self.height() - 5:
                    return retval, result

            if msg.message == win32con.WM_NCCALCSIZE:
                # Remove system title
                return True, 0
            if msg.message == win32con.WM_GETMINMAXINFO:
                # This message is triggered when the window position or size changes.
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                # Modify the maximized window size to the available size of the main screen.
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                # Modify the x and y coordinates of the placement point to (0,0).
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0

            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                if lx and ty:
                    return True, win32con.HTTOPLEFT
                if rx and by:
                    return True, win32con.HTBOTTOMRIGHT
                if rx and ty:
                    return True, win32con.HTTOPRIGHT
                if lx and by:
                    return True, win32con.HTBOTTOMLEFT
                if ty:
                    return True, win32con.HTTOP
                if by:
                    return True, win32con.HTBOTTOM
                if lx:
                    return True, win32con.HTLEFT
                if rx:
                    return True, win32con.HTRIGHT
                # Title
                return True, win32con.HTCAPTION

        return retval, result

    def moveEvent(self, event):
        if not self.current_screen:
            # print('Initial Screen')
            self.current_screen = self.screen()
        elif self.current_screen != self.screen():
            # print('Changed Screen')
            self.current_screen = self.screen()
            self.updateGeometry()

            win32gui.SetWindowPos(int(self.winId()), win32con.NULL, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER |
                                  win32con.SWP_NOOWNERZORDER | win32con.SWP_FRAMECHANGED | win32con.SWP_NOACTIVATE)

        event.accept()

    def closeEvent(self, event=None):
        global settings
        index = settings.index
        self.stop()
        self.player.stop()
        self.playlist.clear()
        self.player.deleteLater()
        settings.index = index
        dumpsettings()
        dumpplaylists()
        text = "\n".join([str(self.width()), str(self.height())])
        try:
            write_file("{}\\mwd.File".format(resourcedir), text)
        except FileNotFoundError:
            create_file("{}\\mwd.File".format(resourcedir), text)
        event.accept()

    def sec_to_time(self, ms):
        r, s = divmod(ms / 1000, 60)
        h, m = divmod(r, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def bytes_to_txt(self, bi):
        if bi / 1024 < 1024:
            return f"{round(bi / 1024, 2)} KB"
        if bi / (1024 * 1024) < 1024:
            return f"{round(bi / (1024 * 1024), 2)} MB"
        if bi / (1024 * 1024 * 1024) < 1024:
            return f"{round(bi / (1024 * 1024 * 1024), 2)} GB"

    def _handle_player_error(self, *err):
        # print(err)
        pass

    def SetupUI(self):
        self.menuBar = QWidget(self.mainWidget)
        self.menuBar.setFixedWidth(40)
        self.menuLayout = QVBoxLayout(self.menuBar)
        self.menuLayout.setSpacing(0)
        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuBar.setLayout(self.menuLayout)

        self.mainStack = QStackedWidget()

        self.homeWidget = QWidget()
        self.homeLayout = QGridLayout(self.homeWidget)
        self.homeLayout.setSpacing(0)
        self.homeLayout.setContentsMargins(5, 0, 5, 0)
        self.homeLayout.setColumnStretch(0, 1)
        self.homeWidget.setLayout(self.homeLayout)

        self.playlistsWidget = QWidget()
        self.playlistsLayout = QGridLayout(self.playlistsWidget)
        self.playlistsLayout.setSpacing(0)
        self.playlistsLayout.setContentsMargins(0, 0, 0, 0)
        self.playlistsWidget.setLayout(self.playlistsLayout)

        self.exploreWidget = QWidget()
        self.exploreLayout = QGridLayout(self.exploreWidget)
        self.exploreLayout.setSpacing(0)
        self.exploreLayout.setContentsMargins(0, 0, 0, 0)
        self.exploreWidget.setLayout(self.exploreLayout)

        self.menumenuButton = QToolButton()
        self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['menuimg'])))
        self.menumenuButton.setStyleSheet("""
        QToolButton {
            background-color: #737373;
            margin: 5px;
            border: none;
        }
        QToolButton:hover {
            background: #000000;
        }
        """)
        self.menumenuButton.setIconSize(QSize(30, 30))
        self.menumenuButton.setFixedSize(QSize(40, 40))

        self.menumenuSeperator = QFrame()
        self.menumenuSeperator.setFrameShape(QFrame.HLine)
        self.menumenuSeperator.setFrameShadow(QFrame.Plain)
        self.menumenuSeperator.setLineWidth(0)
        self.menumenuSeperator.setMidLineWidth(3)
        self.menumenuSeperator.setContentsMargins(5, 6, 5, 6)
        pal = self.menumenuSeperator.palette()
        pal.setColor(QPalette.WindowText, QColor('#BBBBBB'))
        self.menumenuSeperator.setPalette(pal)
        self.menumenuSeperator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.menuhomeButton = QToolButton()
        self.menuhomeButton.setIcon(QIcon(QPixmap(images[settings.theme]['homeimg'])))
        self.menuhomeButton.setStyleSheet("""
        QToolButton {
            background-color: #737373;
            margin-top: 10px;
            margin-left: 5px;
            margin-right: 5px;
            margin-bottom: 10px;
            border: none;
        }
        QToolButton:hover {
            background: #000000;
        }
        """)
        self.menuhomeButton.setIconSize(QSize(30, 30))
        self.menuhomeButton.setFixedSize(QSize(40, 50))
        self.menuhomeButton.setToolTip("Home")
        self.menuhomeButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "home", 'childpage': "main"}))

        self.menuplaylistButton = QToolButton()
        self.menuplaylistButton.setIcon(QIcon(QPixmap(images[settings.theme]['playlistimg'])))
        self.menuplaylistButton.setStyleSheet("""
        QToolButton {
            background-color: #737373;
            margin-top: 10px;
            margin-left: 5px;
            margin-right: 5px;
            margin-bottom: 10px;
            border: none;
        }
        QToolButton:hover {
            background: #000000;
        }
        """)
        self.menuplaylistButton.setIconSize(QSize(30, 30))
        self.menuplaylistButton.setFixedSize(QSize(40, 50))
        self.menuplaylistButton.setToolTip("Playlists")
        self.menuplaylistButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "playlists", 'childpage': "main"}))

        self.menuexploreButton = QToolButton()
        self.menuexploreButton.setIcon(QIcon(QPixmap(images[settings.theme]['exploreimg'])))
        self.menuexploreButton.setStyleSheet("""
        QToolButton {
            background-color: #737373;
            margin-top: 10px;
            margin-left: 5px;
            margin-right: 5px;
            margin-bottom: 10px;
            border: none;
        }
        QToolButton:hover {
            background: #000000;
        }
        """)
        self.menuexploreButton.setIconSize(QSize(30, 30))
        self.menuexploreButton.setFixedSize(QSize(40, 50))
        self.menuexploreButton.setToolTip("Explore")
        self.menuexploreButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "explore", 'childpage': "main"}))

        self.menusettingButton = QToolButton()
        self.menusettingButton.setIcon(QIcon(QPixmap(images[settings.theme]['settingimg'])))
        self.menusettingButton.setStyleSheet("""
        QToolButton {
            background-color: #737373;
            margin: 5px;
            border: none;
        }
        QToolButton:hover {
            background: #000000;
        }
        """)
        self.menusettingButton.setIconSize(QSize(30, 30))
        self.menusettingButton.setFixedSize(QSize(40, 40))
        self.menusettingButton.setToolTip("Settings")

        self.menuLayout.addWidget(self.menumenuButton, alignment=Qt.AlignTop)
        self.menuLayout.addWidget(self.menumenuSeperator, alignment=Qt.AlignTop)
        self.menuLayout.addWidget(self.menuhomeButton, alignment=Qt.AlignTop)
        self.menuLayout.addWidget(self.menuplaylistButton, alignment=Qt.AlignTop)
        self.menuLayout.addWidget(self.menuexploreButton, alignment=Qt.AlignTop)
        self.menuLayout.addStretch()
        self.menuLayout.addWidget(self.menusettingButton, alignment=Qt.AlignBottom)

        self.homesongtitleLabel = EliderLabel(self.homeWidget, mode=Qt.ElideMiddle, textAlignment=Qt.AlignCenter)
        self.homesongtitleLabel.setText("Feel The Music")
        self.homesongtitleLabel.setStyleSheet("""
        background: transparent;
        font: 18px Segoe UI;
        color: #000000;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        margin-left: 20px;
        margin-right: 20px;
        """)

        self.homesongartistLabel = EliderLabel(self.homeWidget, mode=Qt.ElideMiddle, textAlignment=Qt.AlignCenter)
        self.homesongartistLabel.setText("Unknown")
        self.homesongartistLabel.setStyleSheet("""
        background: transparent;
        font: 12px Segoe UI;
        color: #000000;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        margin-left: 20px;
        margin-right: 20px;
        """)

        self.homecentralWidget = QStackedWidget()
        self.homecentralWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.homesongwallimageLabel = ImageLabel(QPixmap(images[settings.theme]['songimg']))
        self.homesongwallimageLabel.setAttribute(Qt.WA_NoSystemBackground)
        self.homesongwallimageLabel.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.homesonglyricWidget = QWidget(self)  # Lyric(self)
        self.homesonglyricWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.homesongdownloadWidget = QWidget(self)  # DownloadWidget(self)
        self.homesongdownloadWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.homecentralWidget.addWidget(self.homesongwallimageLabel)
        self.homecentralWidget.addWidget(self.homesonglyricWidget)
        self.homecentralWidget.addWidget(self.homesongdownloadWidget)
        self.homecentralWidget.setCurrentWidget(self.homesongwallimageLabel)

        self.homeactionWidget = QWidget(self.homeWidget)
        self.homeactionLayout = QHBoxLayout(self.homeactionWidget)
        self.homeactionLayout.setSpacing(0)
        self.homeactionLayout.setContentsMargins(0, 0, 10, 0)
        self.homeactionWidget.setLayout(self.homeactionLayout)

        minibuttondefaltstyle = """
        QToolButton {
            background: #737373;
            border: none;
            margin-left: 5px;
            margin-right: 5px;
        }
        
        QToolButton:hover {
            background: #000000;
        }
        """

        self.homeactionsortButton = QToolButton(self.homeactionWidget)
        self.homeactionsortButton.setIcon(QIcon(QPixmap(images[settings.theme]['sortimg'])))
        self.homeactionsortButton.setIconSize(QSize(25, 25))
        self.homeactionsortButton.setFixedSize(QSize(35, 25))
        self.homeactionsortButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactionsortButton.clicked.connect(self.popupSortType)
        self.homeactionsortButton.setToolTip("Sort")
        self.homeactionsortButton.setCursor(Qt.PointingHandCursor)

        self.homeactionsonginfoButton = QToolButton(self.homeactionWidget)
        self.homeactionsonginfoButton.setIcon(QIcon(QPixmap(images[settings.theme]['songinfoimg'])))
        self.homeactionsonginfoButton.setIconSize(QSize(25, 25))
        self.homeactionsonginfoButton.setFixedSize(QSize(35, 25))
        self.homeactionsonginfoButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactionsonginfoButton.clicked.connect(self.showSongInfo)
        self.homeactionsonginfoButton.setToolTip("Info")
        self.homeactionsonginfoButton.setCursor(Qt.PointingHandCursor)

        self.homeactiontolyricButton = QToolButton(self.homeactionWidget)
        self.homeactiontolyricButton.setIcon(QIcon(QPixmap(images[settings.theme]['tolyricimg'])))
        self.homeactiontolyricButton.setIconSize(QSize(25, 25))
        self.homeactiontolyricButton.setFixedSize(QSize(35, 25))
        self.homeactiontolyricButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactiontolyricButton.setCursor(Qt.PointingHandCursor)

        self.homeactionshuffleButton = QToolButton(self.homeactionWidget)
        self.homeactionshuffleButton.setIcon(QIcon(QPixmap(images[settings.theme]['shuffleimg'])))
        self.homeactionshuffleButton.setIconSize(QSize(25, 25))
        self.homeactionshuffleButton.setFixedSize(QSize(35, 25))
        self.homeactionshuffleButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactionshuffleButton.clicked.connect(self.shuffleButton)
        self.homeactionshuffleButton.setToolTip("Shuffle")
        self.homeactionshuffleButton.setCursor(Qt.PointingHandCursor)

        self.homeactionoverplayButton = QToolButton(self.homeactionWidget)
        self.homeactionoverplayButton.setIcon(QIcon(QPixmap(images[settings.theme]['overplay1img'])))
        self.homeactionoverplayButton.setIconSize(QSize(25, 25))
        self.homeactionoverplayButton.setFixedSize(QSize(35, 25))
        self.homeactionoverplayButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactionoverplayButton.clicked.connect(self.overplayButton)
        self.homeactionoverplayButton.setToolTip("Loop")
        self.homeactionoverplayButton.setCursor(Qt.PointingHandCursor)

        self.homeactionfullscreenButton = QToolButton(self.homeactionWidget)
        self.homeactionfullscreenButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizeimg'])))
        self.homeactionfullscreenButton.setIconSize(QSize(25, 25))
        self.homeactionfullscreenButton.setFixedSize(QSize(35, 25))
        self.homeactionfullscreenButton.setStyleSheet(minibuttondefaltstyle)
        self.homeactionfullscreenButton.clicked.connect(self.fullscreenButton)
        self.homeactionfullscreenButton.setCursor(Qt.PointingHandCursor)

        self.homeactionLayout.addWidget(self.homeactionsortButton, alignment=Qt.AlignLeft)
        self.homeactionLayout.addWidget(self.homeactionsonginfoButton, alignment=Qt.AlignLeft)
        self.homeactionLayout.addWidget(self.homeactiontolyricButton, alignment=Qt.AlignLeft)
        self.homeactionLayout.addStretch()
        self.homeactionLayout.addWidget(self.homeactionshuffleButton, alignment=Qt.AlignRight)
        self.homeactionLayout.addWidget(self.homeactionoverplayButton, alignment=Qt.AlignRight)
        self.homeactionLayout.addWidget(self.homeactionfullscreenButton, alignment=Qt.AlignRight)

        self.hometimeSlider = Slider(Qt.Horizontal, self.homeWidget)
        self.hometimeSlider.setStyleSheet("""
        QSlider {
            background-color: transparent;
            margin-left: 10px;
            margin-right: 10px;
        }
        QSlider::groove:horizontal {
            background: black;
            height: 2px;
            border-radius: 1px;
            margin: 0px;
        }
        QSlider::handle:horizontal {
            background-color: white;
            border: 1px solid black;
            height: 10px;
            width: 10px;
            border-radius: 5px;
            margin: -5px 0px;
        }
        QSlider::add-page:horizontal {
            background: black;
        }
        
        QSlider::sub-page:horizontal {
            background: red;
        }
        """)
        self.hometimeSlider.setCursor(Qt.PointingHandCursor)
        self.hometimeSlider.valueChanged.connect(self.player.setPosition)

        self.hometimeWidget = QWidget(self.homeWidget)
        self.hometimeLayout = QHBoxLayout(self.hometimeWidget)
        self.hometimeLayout.setSpacing(0)
        self.hometimeLayout.setContentsMargins(0, 0, 0, 0)
        self.hometimeWidget.setLayout(self.hometimeLayout)

        self.hometimecurrentLabel = QLabel(self.hometimeWidget)
        self.hometimecurrentLabel.setText("00:00:00")
        self.hometimecurrentLabel.setStyleSheet("""
        font: 14px Segoe UI;
        color: #000000;
        margin-left: 20px;
        margin-right: 5px;
        """)

        self.hometimevolumeSlider = Slider(Qt.Horizontal, self.hometimeWidget)
        self.hometimevolumeSlider.setStyleSheet("""
        QSlider {
            background-color: transparent;
            margin-left: 10px;
        }
        QSlider::groove:horizontal {
            background: black;
            height: 2px;
            border-radius: 1px;
            margin: 0px;
        }
        QSlider::handle:horizontal {
            background-color: white;
            border: 1px solid black;
            height: 10px;
            width: 10px;
            border-radius: 5px;
            margin: -5px 0px;
        }
        QSlider::add-page:horizontal {
            background: black;
        }
        
        QSlider::sub-page:horizontal {
            background: red;
        }
        """)
        self.hometimevolumeSlider.setMaximumWidth(300)
        self.hometimevolumeSlider.setMinimumWidth(200)
        self.hometimevolumeSlider.setRange(0, 100)
        self.hometimevolumeSlider.valueChanged.connect(self.setVolume)
        self.hometimevolumeSlider.setCursor(Qt.PointingHandCursor)

        self.hometimevolumeLabel = QLabel(self.hometimeWidget)
        self.hometimevolumeLabel.setText("100%")
        self.hometimevolumeLabel.setStyleSheet("""
        font: 16px Segoe UI;
        color: #000000;
        margin-left: 10px;
        margin-right: 5px;
        """)

        self.hometimelengthLabel = QLabel(self.hometimeWidget)
        self.hometimelengthLabel.setText("00:00:00")
        self.hometimelengthLabel.setStyleSheet("""
        font: 14px Segoe UI;
        color: #000000;
        margin-right: 20px;
        """)

        self.hometimeLayout.addWidget(self.hometimecurrentLabel, alignment=Qt.AlignLeft)
        self.hometimeLayout.addStretch()
        self.hometimeLayout.addWidget(self.hometimevolumeSlider)
        self.hometimeLayout.addWidget(self.hometimevolumeLabel)
        self.hometimeLayout.addStretch()
        self.hometimeLayout.addWidget(self.hometimelengthLabel, alignment=Qt.AlignRight)

        self.homebuttonWidget = QWidget(self.homeWidget)
        self.homebuttonLayout = QHBoxLayout(self.homebuttonWidget)
        self.homebuttonLayout.setSpacing(0)
        self.homebuttonLayout.setContentsMargins(0, 0, 0, 0)
        self.homebuttonWidget.setLayout(self.homebuttonLayout)

        buttondefaltstyle = """
        QToolButton {
            background-color: #737373;
            border: none;
            margin: 10px;
        }
        QToolButton:hover {
            background-color: #000000;
        }
        """

        self.homebuttonvolumeButton = QToolButton(self.homebuttonWidget)
        self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume2img'])))
        self.homebuttonvolumeButton.setIconSize(QSize(40, 40))
        self.homebuttonvolumeButton.setFixedSize(QSize(60, 60))
        self.homebuttonvolumeButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonvolumeButton.clicked.connect(self.volumeButton)
        self.homebuttonvolumeButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonopenButton = QToolButton(self.homebuttonWidget)
        self.homebuttonopenButton.setIcon(QIcon(QPixmap(images[settings.theme]['openimg'])))
        self.homebuttonopenButton.setIconSize(QSize(40, 40))
        self.homebuttonopenButton.setFixedSize(QSize(60, 60))
        self.homebuttonopenButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonopenButton.clicked.connect(self.open)
        self.homebuttonopenButton.setToolTip("Open")
        self.homebuttonopenButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonpreviousButton = QToolButton(self.homebuttonWidget)
        self.homebuttonpreviousButton.setIcon(QIcon(QPixmap(images[settings.theme]['previousimg'])))
        self.homebuttonpreviousButton.setIconSize(QSize(40, 40))
        self.homebuttonpreviousButton.setFixedSize(QSize(60, 60))
        self.homebuttonpreviousButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonpreviousButton.clicked.connect(self.playlist.previous)
        self.homebuttonpreviousButton.setToolTip("Previous")
        self.homebuttonpreviousButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonplaypauseButton = QToolButton(self.homebuttonWidget)
        self.homebuttonplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
        self.homebuttonplaypauseButton.setIconSize(QSize(40, 40))
        self.homebuttonplaypauseButton.setFixedSize(QSize(60, 60))
        self.homebuttonplaypauseButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonplaypauseButton.clicked.connect(self.play)
        self.homebuttonplaypauseButton.setCursor(Qt.PointingHandCursor)
        self.homebuttonplaypauseButton.setToolTip("Play")

        self.homebuttonnextButton = QToolButton(self.homebuttonWidget)
        self.homebuttonnextButton.setIcon(QIcon(QPixmap(images[settings.theme]['nextimg'])))
        self.homebuttonnextButton.setIconSize(QSize(40, 40))
        self.homebuttonnextButton.setFixedSize(QSize(60, 60))
        self.homebuttonnextButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonnextButton.clicked.connect(self.next)
        self.homebuttonnextButton.setToolTip("Next")
        self.homebuttonnextButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonstopButton = QToolButton(self.homebuttonWidget)
        self.homebuttonstopButton.setIcon(QIcon(QPixmap(images[settings.theme]['stopimg'])))
        self.homebuttonstopButton.setIconSize(QSize(40, 40))
        self.homebuttonstopButton.setFixedSize(QSize(60, 60))
        self.homebuttonstopButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonstopButton.clicked.connect(self.stop)
        self.homebuttonstopButton.setToolTip("Stop")
        self.homebuttonstopButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonplaylistButton = QToolButton(self.homebuttonWidget)
        self.homebuttonplaylistButton.setIcon(QIcon(QPixmap(images[settings.theme]['playlistimg'])))
        self.homebuttonplaylistButton.setIconSize(QSize(40, 40))
        self.homebuttonplaylistButton.setFixedSize(QSize(60, 60))
        self.homebuttonplaylistButton.setStyleSheet(buttondefaltstyle)
        self.homebuttonplaylistButton.setToolTip("Playlist")
        self.homebuttonplaylistButton.setCursor(Qt.PointingHandCursor)

        self.homebuttonLayout.addWidget(self.homebuttonvolumeButton, alignment=Qt.AlignLeft)
        self.homebuttonLayout.addStretch()
        self.homebuttonLayout.addWidget(self.homebuttonopenButton, alignment=Qt.AlignCenter)
        self.homebuttonLayout.addWidget(self.homebuttonpreviousButton, alignment=Qt.AlignCenter)
        self.homebuttonLayout.addWidget(self.homebuttonplaypauseButton, alignment=Qt.AlignCenter)
        self.homebuttonLayout.addWidget(self.homebuttonnextButton, alignment=Qt.AlignCenter)
        self.homebuttonLayout.addWidget(self.homebuttonstopButton, alignment=Qt.AlignCenter)
        self.homebuttonLayout.addStretch()
        self.homebuttonLayout.addWidget(self.homebuttonplaylistButton, alignment=Qt.AlignRight)

        self.homeLayout.addWidget(self.homesongtitleLabel, 0, 0, 1, 1)
        self.homeLayout.addWidget(self.homesongartistLabel, 1, 0, 1, 1)
        self.homeLayout.addWidget(self.homecentralWidget, 3, 0, 1, 1)
        self.homeLayout.addWidget(self.homeactionWidget, 4, 0, 1, 1, alignment=Qt.AlignBottom)
        self.homeLayout.addWidget(self.hometimeSlider, 5, 0, 1, 1, alignment=Qt.AlignBottom)
        self.homeLayout.addWidget(self.hometimeWidget, 6, 0, 1, 1, alignment=Qt.AlignBottom)
        self.homeLayout.addWidget(self.homebuttonWidget, 7, 0, 1, 1, alignment=Qt.AlignBottom)

        self.playlistsStack = QStackedWidget(self.playlistsWidget)
        self.playlistsLayout.addWidget(self.playlistsStack)

        self.playlistsScroll = ScrollArea()
        self.playlistsScroll.setWidgetResizable(True)
        self.playlistsScroll.setStyleSheet(""" border: none; background-color: transparent; """)
        self.playlistsScrollBar = self.playlistsScroll.verticalScrollBar()
        self.playlistsScrollBar.setCursor(Qt.PointingHandCursor)
        self.playlistsScroll.horizontalScrollBar().hide()
        self.playlistsScrollBar.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background: #EBEBEB;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #BEB0C1;
            border-radius: 6px;
            min-height: 12px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #BEB0C1;
        }
        QScrollBar::handle:vertical:pressed {
            background-color: #BEB0C1;
        }
        QScrollBar::sub-line:vertical {
            border: none;
            background-color: none;
        }
        QScrollBar::sub-line:vertical:hover {
            background-color: none;
        }
        QScrollBar::sub-line:vertical:pressed {
            background-color: none;
        }
        QScrollBar::add-line:vertical {
            border: none;
            background-color: none;
        }
        QScrollBar::add-line:vertical:hover {
            background-color: none;
        }
        QScrollBar::add-line:vertical:pressed { 
            background-color: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }       
        """)

        self.playlistsBox = QWidget(self.playlistsScroll)
        self.playlistsboxLayout = QGridLayout(self.playlistsBox)
        self.playlistsboxLayout.setSpacing(0)
        self.playlistsboxLayout.setContentsMargins(0, 0, 0, 0)
        self.playlistsBox.setLayout(self.playlistsboxLayout)
        self.playlistsScroll.setWidget(self.playlistsBox)

        # if 'playlists' not in self.__class__.WIDGETS: self.__class__.WIDGETS['playlists'] = {}
        # for i, x in enumerate(list(listofplay.keys())):
        #     w = PlaylistsItem(i, x, self)
        #     self.__class__.WIDGETS['playlists'][x] = w
        #     self.playlistsboxLayout.addWidget(self.__class__.WIDGETS['playlists'][x], 0, i)
        #     self.__class__.WIDGETS['playlists'][x].adjustPosition(self.width() - 60, self.height() - 233)
        i = 0  # len(list(listofplay.keys()))
        self.playlistboxCreate = QWidget(self)  # CreatePlayList(self, i)
        # self.playlistboxCreate.adjustPosition(self.width() - 60, self.height() - 233)
        self.playlistsboxLayout.addWidget(self.playlistboxCreate, 0, i)
        self.playlistsboxLayout.setRowStretch(0, 1)  # len(list(listofplay.keys())), 1)
        self.playlistsboxLayout.setColumnStretch((self.width() - 60) // 200 + 1, 1)
        self.playlistsBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        self.playlistsStack.addWidget(self.playlistsScroll)
        self.playlistsStack.setCurrentWidget(self.playlistsScroll)

        self.exploreStack = QStackedWidget()
        self.exploreLayout.addWidget(self.exploreStack)

        self.exploreYTWidget = QWidget(self)  # YT(self)

        self.exploreDownloadsWidget = QWidget(self)  # YTDownloads(self)

        self.exploreStack.addWidget(self.exploreYTWidget)
        self.exploreStack.addWidget(self.exploreDownloadsWidget)
        self.exploreStack.setCurrentWidget(self.exploreYTWidget)

        self.mainStack.addWidget(self.homeWidget)
        self.mainStack.addWidget(self.playlistsWidget)
        self.mainStack.addWidget(self.exploreWidget)
        self.mainStack.setCurrentWidget(self.homeWidget)

        self.miniplayerWidget = QWidget()
        self.miniplayerWidget.setMaximumHeight(130)
        self.miniplayerLayout = QHBoxLayout(self.miniplayerWidget)
        self.miniplayerLayout.setSpacing(0)
        self.miniplayerLayout.setContentsMargins(10, 0, 0, 0)
        self.miniplayerWidget.setLayout(self.miniplayerLayout)

        self.miniplayersongimageLabel = ImageViewer()
        self.miniplayersongimageLabel.setPixmap(QPixmap(images[settings.theme]['songimg']))
        self.miniplayersongimageLabel.setScaledContents(True)
        self.miniplayersongimageLabel.setStyleSheet("""
        background: transparent;
        """)
        self.miniplayersongimageLabel.setFixedSize(QSize(100, 100))
        self.miniplayersongimageLabel.setHeight(100, 100)

        self.miniplayercontainerWidget = QWidget(self.miniplayerWidget)
        self.miniplayercontainerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.miniplayercontainerLayout = QVBoxLayout(self.miniplayercontainerWidget)
        self.miniplayercontainerLayout.setSpacing(0)
        self.miniplayercontainerLayout.setContentsMargins(10, 5, 0, 0)
        self.miniplayercontainerWidget.setLayout(self.miniplayercontainerLayout)

        self.miniplayersongtitleLabel = EliderLabel(self.miniplayercontainerWidget, mode=Qt.ElideRight,
                                                    textAlignment=Qt.AlignLeft)
        self.miniplayersongtitleLabel.setText("Feel The Music")
        self.miniplayersongtitleLabel.setStyleSheet("""
        margin-top: 5px;
        margin-bottom: 5px;
        margin-right: 30px;
        font: 16px Segoe UI;
        """)

        self.miniplayerstatusWidget = QWidget(self.miniplayercontainerWidget)
        self.miniplayerstatusLayout = QHBoxLayout(self.miniplayerstatusWidget)
        self.miniplayerstatusLayout.setSpacing(0)
        self.miniplayerstatusLayout.setContentsMargins(0, 0, 0, 0)
        self.miniplayerstatusWidget.setLayout(self.miniplayerstatusLayout)

        self.miniplayersongtimeLabel = QLabel(self.miniplayerstatusWidget)
        self.miniplayersongtimeLabel.setText("00:00:00 / 00:00:00")
        self.miniplayersongtimeLabel.setStyleSheet("""
        margin-bottom: 5px;
        margin-right: 10px;
        font: 12px Segoe UI;
        """)

        self.miniplayersongvolumeLabel = QLabel(self.miniplayerstatusWidget)
        self.miniplayersongvolumeLabel.setText("Volume : 75%")
        self.miniplayersongvolumeLabel.setStyleSheet("""
        margin-bottom: 5px;
        margin-right: 10px;
        font: 12px Segoe UI;
        """)

        self.miniplayersongartistLabel = EliderLabel(self.miniplayerstatusWidget, mode=Qt.ElideRight,
                                                     textAlignment=Qt.AlignLeft)
        self.miniplayersongartistLabel.setText("Unknown")
        self.miniplayersongartistLabel.setStyleSheet("""
        margin-bottom: 5px;
        margin-right: 10px;
        font: 12px Segoe UI;
        """)

        self.miniplayerstatusLayout.addWidget(self.miniplayersongtimeLabel, alignment=Qt.AlignLeft)
        self.miniplayerstatusLayout.addWidget(self.miniplayersongvolumeLabel, alignment=Qt.AlignLeft)
        self.miniplayerstatusLayout.addWidget(self.miniplayersongartistLabel)

        self.miniplayertimeSlider = Slider(Qt.Horizontal, self.miniplayercontainerWidget)
        self.miniplayertimeSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.miniplayertimeSlider.setStyleSheet("""
        QSlider {
            background-color: transparent;
            margin-right: 10px;
        }
        QSlider::groove:horizontal {
            background: black;
            height: 2px;
            border-radius: 1px;
            margin: 0px;
        }
        QSlider::handle:horizontal {
            background-color: white;
            border: 1px solid black;
            height: 10px;
            width: 10px;
            border-radius: 5px;
            margin: -5px 0px;
        }
        QSlider::add-page:horizontal {
            background: black;
        }
        
        QSlider::sub-page:horizontal {
            background: red;
        }
        """)
        self.miniplayertimeSlider.setCursor(Qt.PointingHandCursor)
        self.miniplayertimeSlider.valueChanged.connect(self.player.setPosition)

        self.miniplayertoolcontainerWidget = QWidget(self.miniplayercontainerWidget)
        self.miniplayertoolcontainerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.miniplayertoolcontainerLayout = QHBoxLayout(self.miniplayertoolcontainerWidget)
        self.miniplayertoolcontainerLayout.setSpacing(0)
        self.miniplayertoolcontainerLayout.setContentsMargins(10, 0, 0, 0)
        self.miniplayertoolcontainerWidget.setLayout(self.miniplayertoolcontainerLayout)

        miniplayerbuttondefaultstyle = """
        QToolButton {
            background: #737373;
            border: none;
            margin: 5px;
        }
        
        QToolButton:hover {
            background: #000000;
        }
        """

        self.miniplayerpreviousButton = QToolButton(self.miniplayertoolcontainerWidget)
        self.miniplayerpreviousButton.setIcon(QIcon(QPixmap(images[settings.theme]['previousimg'])))
        self.miniplayerpreviousButton.setIconSize(QSize(40, 40))
        self.miniplayerpreviousButton.setFixedSize(QSize(50, 50))
        self.miniplayerpreviousButton.clicked.connect(self.playlist.previous)
        self.miniplayerpreviousButton.setCursor(Qt.PointingHandCursor)
        self.miniplayerpreviousButton.setStyleSheet(miniplayerbuttondefaultstyle)

        self.miniplayerplaypauseButton = QToolButton(self.miniplayertoolcontainerWidget)
        self.miniplayerplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
        self.miniplayerplaypauseButton.setIconSize(QSize(40, 40))
        self.miniplayerplaypauseButton.setFixedSize(QSize(50, 50))
        self.miniplayerplaypauseButton.setStyleSheet(miniplayerbuttondefaultstyle)
        self.miniplayerplaypauseButton.setCursor(Qt.PointingHandCursor)
        self.miniplayerplaypauseButton.clicked.connect(self.play)

        self.miniplayernextButton = QToolButton(self.miniplayertoolcontainerWidget)
        self.miniplayernextButton.setIcon(QIcon(QPixmap(images[settings.theme]['nextimg'])))
        self.miniplayernextButton.setIconSize(QSize(40, 40))
        self.miniplayernextButton.setFixedSize(QSize(50, 50))
        self.miniplayernextButton.clicked.connect(self.playlist.next)
        self.miniplayernextButton.setCursor(Qt.PointingHandCursor)
        self.miniplayernextButton.setStyleSheet(miniplayerbuttondefaultstyle)

        self.miniplayervolumeSlider = Slider(Qt.Horizontal, self.miniplayertoolcontainerWidget)
        self.miniplayervolumeSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.miniplayervolumeSlider.setStyleSheet("""
        QSlider {
            background-color: transparent;
            margin-left: 10px;
        }
        QSlider::groove:horizontal {
            background: black;
            height: 2px;
            border-radius: 1px;
            margin: 0px;
        }
        QSlider::handle:horizontal {
            background-color: white;
            border: 1px solid black;
            height: 10px;
            width: 10px;
            border-radius: 5px;
            margin: -5px 0px;
        }
        QSlider::add-page:horizontal {
            background: black;
        }
        
        QSlider::sub-page:horizontal {
            background: red;
        }
        """)
        self.miniplayervolumeSlider.valueChanged.connect(self.setVolume)
        self.miniplayervolumeSlider.setCursor(Qt.PointingHandCursor)
        self.miniplayervolumeSlider.setRange(0, 100)
        self.miniplayervolumeSlider.setMinimumWidth(200)
        self.miniplayervolumeSlider.setMaximumWidth(300)

        self.miniplayertoolcontainerLayout.addWidget(self.miniplayerpreviousButton, alignment=Qt.AlignLeft)
        self.miniplayertoolcontainerLayout.addWidget(self.miniplayerplaypauseButton, alignment=Qt.AlignLeft)
        self.miniplayertoolcontainerLayout.addWidget(self.miniplayernextButton, alignment=Qt.AlignLeft)
        self.miniplayertoolcontainerLayout.addWidget(self.miniplayervolumeSlider)
        self.miniplayertoolcontainerLayout.addStretch()

        self.miniplayercontainerLayout.addWidget(self.miniplayersongtitleLabel)
        self.miniplayercontainerLayout.addWidget(self.miniplayerstatusWidget)
        self.miniplayercontainerLayout.addWidget(self.miniplayertimeSlider)
        self.miniplayercontainerLayout.addWidget(self.miniplayertoolcontainerWidget)

        self.miniplayerLayout.addWidget(self.miniplayersongimageLabel, alignment=Qt.AlignLeft)
        self.miniplayerLayout.addWidget(self.miniplayercontainerWidget, stretch=1)

        self.playinglist = QWidget()
        self.playinglistLayout = QGridLayout(self.playinglist)
        self.playinglistLayout.setSpacing(0)
        self.playinglistLayout.setContentsMargins(0, 0, 0, 0)
        self.playinglist.setLayout(self.playinglistLayout)

        self.playinglistSongTracker = QToolButton()
        self.playinglistSongTracker.setIcon(QIcon(QPixmap(images[settings.theme]['trackerimg'])))
        self.playinglistSongTracker.setIconSize(QSize(20, 20))
        self.playinglistSongTracker.setStyleSheet("""
        QToolButton {
            margin-bottom: 30px;
            margin-right: 30px;
            background: transparent;
            border: none;
        }
        QToolButton:pressed {
            margin-left: 1px;
            margin-top: 1px;
            margin-bottom: 29px;
            margin-right: 29px;
        }
        """)
        self.playinglistSongTracker.setCursor(Qt.PointingHandCursor)
        self.playinglistSongTracker.clicked.connect(self.scrollToSong)

        self.playinglistScroll = ScrollArea()
        self.playinglistScroll.setWidgetResizable(True)
        self.playinglistScroll.setStyleSheet("""
        border: none;
        background-color: transparent;
        """)
        self.playinglistWidgetScrollBar = self.playinglistScroll.verticalScrollBar()
        self.playinglistWidgetScrollBar.setCursor(Qt.PointingHandCursor)
        self.playinglistScroll.horizontalScrollBar().hide()
        self.playinglistWidgetScrollBar.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background: #EBEBEB;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #BEB0C1;
            border-radius: 6px;
            min-height: 12px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #BEB0C1;
        }
        QScrollBar::handle:vertical:pressed {
            background-color: #BEB0C1;
        }
        QScrollBar::sub-line:vertical {
            border: none;
            background-color: none;
        }
        QScrollBar::sub-line:vertical:hover {
            background-color: none;
        }
        QScrollBar::sub-line:vertical:pressed {
            background-color: none;
        }
        QScrollBar::add-line:vertical {
            border: none;
            background-color: none;
        }
        QScrollBar::add-line:vertical:hover {
            background-color: none;
        }
        QScrollBar::add-line:vertical:pressed { 
            background-color: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }       
        """)

        self.playinglistWidget = QWidget(self.playinglistScroll)
        self.playinglistWidgetLayout = QVBoxLayout(self.playinglistWidget)
        self.playinglistWidgetLayout.setSpacing(0)
        self.playinglistWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.playinglistWidget.setLayout(self.playinglistWidgetLayout)
        self.playinglistScroll.setWidget(self.playinglistWidget)

        self.playinglisttoolWidget = QWidget()
        self.playinglisttoolLayout = QHBoxLayout(self.playinglisttoolWidget)
        self.playinglisttoolLayout.setSpacing(0)
        self.playinglisttoolLayout.setContentsMargins(0, 0, 0, 0)
        self.playinglisttoolWidget.setLayout(self.playinglisttoolLayout)

        self.playinglisttoolselectedcountLabel = QLabel(self.playinglisttoolWidget)
        self.playinglisttoolselectedcountLabel.setFixedWidth(100)

        playinglisttoolbuttondefault = """
        QToolButton {
            background: #EBEBEB;
            border: none;
            margin-left: 5px;
            margin-top: 5px;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        
        QToolButton:pressed {
            margin-left: 6px;
            margin-top: 6px;
            margin-right: 4px;
            margin-bottom: 4px;
        }
        """

        self.playinglisttoolplayButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolplayButton.setIcon(QIcon(QPixmap(images['common']['playimg'])))
        self.playinglisttoolplayButton.setIconSize(QSize(40, 40))
        self.playinglisttoolplayButton.setFixedSize(QSize(40, 40))
        self.playinglisttoolplayButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolplayButton.clicked.connect(self.playSelectedList)
        self.playinglisttoolplayButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttoolshuffleButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolshuffleButton.setIcon(QIcon(QPixmap(images['common']['shuffleimg'])))
        self.playinglisttoolshuffleButton.setIconSize(QSize(40, 40))
        self.playinglisttoolshuffleButton.setFixedSize(QSize(40, 40))
        self.playinglisttoolshuffleButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolshuffleButton.clicked.connect(self.shuffleSelectedList)
        self.playinglisttoolshuffleButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttooladdButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttooladdButton.setIcon(QIcon(QPixmap(images['common']['addimg'])))
        self.playinglisttooladdButton.setIconSize(QSize(40, 40))
        self.playinglisttooladdButton.setFixedSize(QSize(40, 40))
        self.playinglisttooladdButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttooladdButton.clicked.connect(self.addSelectedList)
        self.playinglisttooladdButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttoolremoveButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolremoveButton.setIcon(QIcon(QPixmap(images['common']['removeimg'])))
        self.playinglisttoolremoveButton.setIconSize(QSize(40, 40))
        self.playinglisttoolremoveButton.setFixedSize(QSize(40, 40))
        self.playinglisttoolremoveButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolremoveButton.clicked.connect(self.popSelectedList)
        self.playinglisttoolremoveButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttoolremovedupButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolremovedupButton.setIcon(QIcon(QPixmap(images['common']['removedupimg'])))
        self.playinglisttoolremovedupButton.setIconSize(QSize(40, 40))
        self.playinglisttoolremovedupButton.setFixedSize(QSize(40, 40))
        self.playinglisttoolremovedupButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolremovedupButton.clicked.connect(self.removeDuplicates)
        self.playinglisttoolremovedupButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttoolselectallButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolselectallButton.setIcon(QIcon(QPixmap(images['common']['selectallimg'])))
        self.playinglisttoolselectallButton.setIconSize(QSize(40, 40))
        self.playinglisttoolselectallButton.setFixedSize(QSize(40, 40))
        self.playinglisttoolselectallButton.clicked.connect(self.selectAll)
        self.playinglisttoolselectallButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolselectallButton.setStyleSheet(playinglisttoolbuttondefault)

        self.playinglisttoolsearchEdit = QLineEdit(self.playinglisttoolWidget)
        self.playinglisttoolsearchEdit.setClearButtonEnabled(True)
        self.playinglisttoolsearchEdit.setFixedHeight(40)
        self.playinglisttoolsearchEdit.setStyleSheet("""
        QLineEdit {
            background: #DDDDDD;
            border: none;
            border-radius: 15px;
            margin: 5px;
            font: 14px Segoe UI;
        }
        """)
        self.playinglisttoolsearchEdit.setPlaceholderText("Search...")
        self.playinglisttoolsearchEdit.addAction(QIcon(QPixmap(images['common']['searchimg'])),
                                                 QLineEdit.LeadingPosition)

        self.playinglisttoolsortButton = QToolButton(self.playinglisttoolWidget)
        self.playinglisttoolsortButton.setIcon(QIcon(QPixmap(images['common']['sortimg'])))
        self.playinglisttoolsortButton.setIconSize(QSize(40, 40))
        self.playinglisttoolsortButton.setFixedSize(QSize(70, 40))
        self.playinglisttoolsortButton.setCursor(Qt.PointingHandCursor)
        self.playinglisttoolsortButton.setStyleSheet("""
        QToolButton {
            background: #EBEBEB;
            border: none;
            margin-left: 5px;
            margin-top: 5px;
            margin-right: 20px;
            margin-bottom: 5px;
        }
        
        QToolButton:pressed {
            margin-left: 6px;
            margin-top: 6px;
            margin-right: 24px;
            margin-bottom: 4px;
        }
        """)

        self.playinglisttoolLayout.addWidget(self.playinglisttoolselectedcountLabel, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolplayButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolshuffleButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttooladdButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolremoveButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolremovedupButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolselectallButton, alignment=Qt.AlignLeft)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolsearchEdit)
        self.playinglisttoolLayout.addWidget(self.playinglisttoolsortButton, alignment=Qt.AlignRight)

        verticalSpacer1 = QSplitter(Qt.Horizontal)
        verticalSpacer1.setStyleSheet("""background: #BBBBBB; margin: 0px; margin-left: 20px; margin-right: 20px;""")
        verticalSpacer1.setFixedHeight(1)
        verticalSpacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        verticalSpacer2 = QSplitter(Qt.Horizontal)
        verticalSpacer2.setStyleSheet("""background: #BBBBBB; margin: 0px; margin-left: 20px; margin-right: 20px;""")
        verticalSpacer2.setFixedHeight(1)
        verticalSpacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.playinglistLayout.addWidget(verticalSpacer1, 0, 0)
        self.playinglistLayout.addWidget(self.playinglistScroll, 1, 0)
        self.playinglistLayout.addWidget(self.playinglistSongTracker, 1, 0, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.playinglistLayout.addWidget(verticalSpacer2, 2, 0)
        self.playinglistLayout.addWidget(self.playinglisttoolWidget, 3, 0, alignment=Qt.AlignBottom)
        self.playinglistLayout.setColumnStretch(0, 1)

        self.mainLayout.addWidget(self.menuBar, 0, 0, 3, 1)
        self.mainLayout.addWidget(self.mainStack, 0, 1)
        self.mainLayout.addWidget(self.miniplayerWidget, 1, 1)
        self.mainLayout.addWidget(self.playinglist, 2, 1)
        self.hide_miniplayer()
        self.playinglist.setVisible(False)

        self.shadowStack = QStackedWidget()

        self.shadowcreateWidget = QWidget(self)  # CreateNewPlaylist(self)

        self.shadowStack.addWidget(self.shadowcreateWidget)
        self.shadowStack.setCurrentWidget(self.shadowcreateWidget)

        self.upperShadowLayout.addWidget(self.shadowStack)

        self.current_window_details = {'page': "home", 'childpage': "main"}
        self.window_log = []

        self.playlist.currentIndexChanged.connect(self.songChanged)
        self.player.durationChanged.connect(self.songChanged)
        self.player.mediaStatusChanged.connect(self.checkPlaylistEnd)
        self.player.positionChanged.connect(self.positionChanged)

        self.playlist.setCurrentIndex(settings.index)
        self.hometimevolumeSlider.setValue(settings.volume)
        self.updateVolumeButton()
        self.updateShuffleButton()
        self.updateOverplayButton()
        if settings.overplayvalue == 1:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        elif settings.overplayvalue == 2:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.homebuttonplaylistButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "home", 'childpage': "playlist"}))
        self.homeactiontolyricButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "home", "childpage": "lyric"}))

        self.load()
        self.playlist.setCurrentIndex(settings.index)

    def hide_miniplayer(self):
        self.miniplayerWidget.hide()
        self.miniplayersongimageLabel.hide()
        self.miniplayercontainerWidget.hide()
        self.miniplayersongtitleLabel.hide()
        self.miniplayersongtimeLabel.hide()
        self.miniplayersongvolumeLabel.hide()
        self.miniplayersongartistLabel.hide()
        self.miniplayertimeSlider.hide()
        self.miniplayertoolcontainerWidget.hide()
        self.miniplayerpreviousButton.hide()
        self.miniplayerplaypauseButton.hide()
        self.miniplayernextButton.hide()
        self.miniplayervolumeSlider.hide()
        self.miniplayeron = False

    def show_miniplayer(self):
        self.miniplayerWidget.show()
        self.miniplayersongimageLabel.show()
        self.miniplayercontainerWidget.show()
        self.miniplayersongtitleLabel.show()
        self.miniplayersongtimeLabel.show()
        self.miniplayersongvolumeLabel.show()
        self.miniplayersongartistLabel.show()
        self.miniplayertimeSlider.show()
        self.miniplayertoolcontainerWidget.show()
        self.miniplayerpreviousButton.show()
        self.miniplayerplaypauseButton.show()
        self.miniplayernextButton.show()
        self.miniplayervolumeSlider.show()
        self.miniplayeron = True

        # if len(listOfSongs):
        #     duration = self.player.duration()
        #     index = self.playlist.currentIndex()
        #     settings.index = index
        #     file = listOfSongs[index]['song']
        #     name = listOfSongs[index]['name']
        #     artist = listOfSongs[index]['artist']
        #     cover = scover(file)
        #     if cover is not None:
        #         img = Image.open(cover)
        #         img.convert('RGB')
        #         data = img.tobytes("raw", "RGB")
        #         qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
        #         image = QPixmap(qim)
        #     if cover is None:
        #         qim = images[settings.theme]['songimg']
        #         image = QPixmap(qim)
        # if not len(listOfSongs):
        #     name = "Feel The Music"
        #     duration = 0
        #     artist = "Unknown"
        #     qim = images[settings.theme]['songimg']
        #     image = QPixmap(qim)

        # self.miniplayersongtitleLabel.setText(name)
        # # self.miniplayersongstatusLabel.setText(f"""00:00:00 / {self.sec_to_time(duration)}\t\tVolume : {settings.volume}%\t{artist}""")
        # self.miniplayersongtimeLabel.setText(f"00:00:00 / {self.sec_to_time(duration)}")
        # self.miniplayersongvolumeLabel.setText(f"Volume : {settings.volume}%")
        # self.miniplayersongartistLabel.setText(artist)
        # self.miniplayersongimageLabel.setPixmap(image)  # .setImage(qim, 100, 100)
        # self.miniplayervolumeSlider.setValue(settings.volume)
        # self.miniplayertimeSlider.setMaximum(duration)

    def wheelEvent(self, event):
        n = event.angleDelta().y() / 120
        if not self.miniplayeron:
            self.hometimevolumeSlider.setValue(int(settings.volume + n * 3))
        if self.miniplayeron:
            self.miniplayervolumeSlider.setValue(int(settings.volume + n * 3))
        event.accept()

    def keyPressEvent(self, event):
        passThrough = True
        if event.key() == Qt.Key_F4 and (event.modifiers() & Qt.AltModifier):
            passThrough = False
            self.close()
        if event.key() == Qt.Key_PageUp:
            passThrough = False
            self.previous()
        if event.key() == Qt.Key_Space:
            passThrough = False
            self.play(forceOpen=True)
        if event.key() == Qt.Key_PageDown:
            passThrough = False
            self.next()
        if event.key() == Qt.Key_Right:
            passThrough = False
            self.player.setPosition(self.player.position() + 500)
        if event.key() == Qt.Key_Left:
            passThrough = False
            self.player.setPosition(self.player.position() - 500)
        if event.key() == Qt.Key_Down:
            if self.current_window_details['page'] == "home" and self.current_window_details['childpage'] == "main":
                passThrough = False
                self.hometimevolumeSlider.setValue(settings.volume - 3 if (settings.volume - 3) > 0 else 0)
        if event.key() == Qt.Key_Up:
            if self.current_window_details['page'] == "home" and self.current_window_details['childpage'] == "main":
                passThrough = False
                self.hometimevolumeSlider.setValue(settings.volume + 3 if (settings.volume + 3) < 100 else 100)
        if event.key() == Qt.Key_Escape:
            passThrough = False
            self.showMinimized()
        if passThrough:
            super(Window, self).keyPressEvent(event)

    def popupSortType(self, event=None):
        menu = QMenu(self)
        menu.setCursor(Qt.PointingHandCursor)
        menu.setStyleSheet("""
        QMenu {
            background-color: white;
            border: 1px solid #6D6D6D;
            font: 16px Segoe UI;
            color: black;
        }
        QAction {
            background-color: white;
            border: 0px;
            font: 16px Segoe UI;
            color: #6D6D6D;
            padding: 5px;
            margin-top: 4px;
            margin-bottom: 4px;
        }
        QAction:hover {
            background-color: #699DE2;
            color: white;
        }
        """)
        action_list = ["Name", "Genre", "Album", "Artist", "Date modifiend", "Time added"]
        for x in action_list:
            action = QAction(f"     {x}" if x != settings.sorttype else f"✅{x}", self)
            menu.addAction(action)
        menu.triggered.connect(lambda event: self.selectSortType(event.text().strip()))
        pos1 = self.homeactionsortButton.pos()
        pos2 = self.pos()
        pos = self.homeactionsortButton.mapToGlobal(self.homeactionsortButton.rect().topLeft())
        menu.popup(QPoint(pos.x(), pos.y() - 150))

    def selectSortType(self, sortType):
        if "✅" in sortType: sortType[1:]
        if settings.sorttype == "Shuffle":
            self.lastSortType = sortType
            self.shuffleButton()
        else:
            self.homeactionshuffleButton.setDisabled(True)
            self.homeactionsortButton.setDisabled(True)

            playing = [False, True]
            lastIndexNo = 0
            lastPosition = 0

            if self.player.state() == QMediaPlayer.PlayingState:
                playing[0] = True
                try:
                    lastIndexNo = listOfSongs[settings.index]['no']
                except IndexError:
                    pass
                lastPosition = self.player.position()
                if self.player.state() == QMediaPlayer.PausedState:
                    playing[0] = False

            self.sortList(sortType)
            lastIndex = settings.index
            self.load()
            self.playlist.setCurrentIndex(settings.index)

            if playing[0]:
                if playing[1]:
                    self.play(forceOpen=False)
                self.playlist.setCurrentIndex(lastIndex)
                settings.index = lastIndex
                self.player.setPosition(lastPosition)
                self.player.play(forceOpen=False)
                self.positionChanged(lastPosition)

            self.homeactionshuffleButton.setEnabled(True)
            self.homeactionsortButton.setEnabled(True)

    def sortList(self, sortType):
        global listofplay, listOfSongs
        lastIndexNo = 0
        if settings['selectinglist'] == settings['playinglist']:
            try:
                lastIndexNo = listOfSongs[settings.index]['no']
            except IndexError:
                pass
        if sortType == "Name":
            settings.sorttype = sortType
            settings.sortside = "Ascending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('name', 'song', 'genre', 'album', 'artist',
                                                                          'date', 'no'))
        elif sortType == "Genre":
            settings.sorttype = sortType
            settings.sortside = "Ascending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('genre', 'name', 'song', 'album', 'artist',
                                                                          'date', 'no'))
        elif sortType == "Album":
            settings.sorttype = sortType
            settings.sortside = "Ascending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('album', 'name', 'song', 'genre', 'artist',
                                                                          'date', 'no'))
        elif sortType == "Artist":
            settings.sorttype = sortType
            settings.sortside = "Ascending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('artist', 'name', 'song', 'genre', 'album',
                                                                          'date', 'no'))
        elif sortType == "Date modified":
            settings.sorttype = sortType
            settings.sortside = "Descending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('date', 'name', 'song', 'genre', 'album',
                                                                          'artist', 'no'))
            listofplay[settings['selectinglist']].reverse()
        elif sortType == "Time added":
            settings.sorttype = sortType
            settings.sortside = "Ascending"
            listofplay[settings['selectinglist']] = sorted(listofplay[settings['selectinglist']],
                                                           key=itemgetter('no', 'name', 'song', 'genre', 'album',
                                                                          'artist', 'date'))

        if settings['selectinglist'] == settings['playinglist']:
            listOfSongs = listofplay[settings['selectinglist']]
            settings.index = 0
            for x in range(len(listOfSongs)):
                if listOfSongs[x]['no'] == lastIndexNo:
                    settings.index = x
                    break
            if settings.index < 0 or settings.index >= len(listOfSongs):
                settings.index = 0
        dumpplaylists()

    def showSongInfo(self, event=None):
        if len(listofplay[settings['playinglist']]):
            if settings.index < len(listofplay[settings['playinglist']]):
                self.w = SongInfo(self)
                self.w.show()
                # self.w.raise_()

    def shuffleButton(self, event=None):
        global listOfSongs, listofplay, settings

        self.homeactionshuffleButton.setDisabled(True)
        self.homeactionsortButton.setDisabled(True)

        playing = [False, True]
        lastIndexNo = 0
        lastPosition = 0

        if self.player.state() == QMediaPlayer.PlayingState:
            playing[0] = True
            try:
                lastIndexNo = listOfSongs[settings.index]['no']
            except IndexError:
                pass
            lastPosition = self.player.position()
            if self.player.state() == QMediaPlayer.PausedState:
                playing[0] = False

        if settings.sorttype == "Shuffle":
            self.sortList(self.lastSortType)
            self.updateShuffleButton()
            lastIndex = settings.index
            self.load()
            self.playlist.setCurrentIndex(settings.index)
        else:
            self.lastSortType = settings.sorttype if settings.sorttype != "Shuffle" else "Name"
            settings.sorttype = "Shuffle"
            self.updateShuffleButton()
            random.shuffle(listOfSongs)
            listofplay[settings['selectinglist']] = listOfSongs
            settings.index = 0
            for x in range(len(listOfSongs)):
                if listOfSongs[x]['no'] == lastIndexNo:
                    settings.index = x
                    break
            if settings.index < 0 or settings.index >= len(listOfSongs):
                settings.index = 0
            lastIndex = settings.index
            self.load()
            self.playlist.setCurrentIndex(settings.index)

        if playing[0]:
            if playing[1]:
                self.play(forceOpen=False)
            self.playlist.setCurrentIndex(lastIndex)
            settings.index = lastIndex
            self.player.setPosition(lastPosition)
            self.player.play(forceOpen=False)
            self.positionChanged(lastPosition)

        self.homeactionshuffleButton.setEnabled(True)
        self.homeactionsortButton.setEnabled(True)

    def updateShuffleButton(self):
        if settings.sorttype == "Shuffle":
            self.homeactionshuffleButton.setStyleSheet("""
                QToolButton {
                    background: red;
                    border: none;
                    margin-left: 5px;
                    margin-right: 5px;
                }

                QToolButton:hover {
                    background: orange;
                }
            """)
        if settings.sorttype != "Shuffle":
            self.homeactionshuffleButton.setStyleSheet("""
                QToolButton {
                    background: #737373;
                    border: none;
                    margin-left: 5px;
                    margin-right: 5px;
                }

                QToolButton:hover {
                    background: #000000;
                }
            """)

    def overplayButton(self, event=None):
        if settings.overplayvalue == 0:
            settings.overplayvalue = 1
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        elif settings.overplayvalue == 1:
            settings.overplayvalue = 2
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        else:
            settings.overplayvalue = 0
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.updateOverplayButton()

    def updateOverplayButton(self):
        if settings.overplayvalue == 1:
            self.homeactionoverplayButton.setIcon(QIcon(QPixmap(images[settings.theme]['overplay1img'])))
            self.homeactionoverplayButton.setStyleSheet("""
                QToolButton {
                    background: red;
                    border: none;
                    margin-left: 5px;
                    margin-right: 5px;
                }
                
                QToolButton:hover {
                    background: orange;
                }
            """)
        if settings.overplayvalue == 2:
            self.homeactionoverplayButton.setIcon(QIcon(QPixmap(images[settings.theme]['overplay2img'])))
            self.homeactionoverplayButton.setStyleSheet("""
                QToolButton {
                    background: red;
                    border: none;
                    margin-left: 5px;
                    margin-right: 5px;
                }
                
                QToolButton:hover {
                    background: orange;
                }
            """)
        if settings.overplayvalue == 0:
            self.homeactionoverplayButton.setIcon(QIcon(QPixmap(images[settings.theme]['overplay1img'])))
            self.homeactionoverplayButton.setStyleSheet("""
                QToolButton {
                    background: #737373;
                    border: none;
                    margin-left: 5px;
                    margin-right: 5px;
                }
                
                QToolButton:hover {
                    background: #000000;
                }
            """)

    def fullscreenButton(self, event=None):
        if self.isFullScreen():
            self.showNormal()
            self.homeactionfullscreenButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizeimg'])))
        else:
            self.showFullScreen()
            self.homeactionfullscreenButton.setIcon(QIcon(QPixmap(images[settings.theme]['minimizeimg'])))

    def setVolume(self, volume):
        if self.player.isMuted():
            self.volumeButton()
        settings.volume = volume
        self.player.setVolume(volume)
        self.hometimevolumeLabel.setText(f"{settings.volume}%")
        self.updateVolumeButton()
        if self.miniplayeron:
            # artist = "Unknown"
            # if len(listOfSongs):
            #     artist = listOfSongs[settings.index]['artist']
            # self.miniplayersongstatusLabel.setText(f"""{self.sec_to_time(self.player.position())} / {self.sec_to_time(self.player.duration())}\t\tVolume : {settings.volume}%\t{artist}""")
            self.miniplayersongvolumeLabel.setText(f"Volume : {settings.volume}%")

    def volumeButton(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.updateVolumeButton()
        else:
            self.player.setMuted(True)
            self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume4img'])))

    def updateVolumeButton(self):
        if settings.volume == 0:
            self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume4img'])))
        if 0 < settings.volume < 34:
            self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume1img'])))
        if 34 <= settings.volume < 67:
            self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume2img'])))
        if settings.volume >= 67:
            self.homebuttonvolumeButton.setIcon(QIcon(QPixmap(images[settings.theme]['volume3img'])))

    def updateState(self):
        if self.lastState == Qt.WindowFullScreen:
            self.homeactionfullscreenButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizeimg'])))
        if self.lastState == Qt.WindowMaximized:
            self.titleBar.restoreButton.setIcon(QIcon(QPixmap(images[settings.theme]['maximizewinimg'])))

        if self.windowState() == Qt.WindowFullScreen:
            self.homeactionfullscreenButton.setIcon(QIcon(QPixmap(images[settings.theme]['minimizeimg'])))
        if self.windowState() == Qt.WindowMaximized:
            self.titleBar.restoreButton.setIcon(QIcon(QPixmap(images[settings.theme]['restoreimg'])))

    def resizeEvent(self, a0=None):
        super().resizeEvent(a0)
        self.homesongwallimageLabel.setHeight(self.width() - 60, self.height() - 233)
        if self.current_window_details['page'] == "home" and self.current_window_details['childpage'] == "lyric":
            self.homesonglyricWidget.setHeight(self.width() - 60, self.height() - 233)
        if self.current_window_details['page'] == "home" and self.current_window_details['childpage'] == "download":
            self.homesongdownloadWidget.setHeight(self.width() - 60, self.height() - 233)
        if self.current_window_details['page'] == "playlists" and self.current_window_details['childpage'] == "main":
            for x in list(self.__class__.WIDGETS['playlists'].keys()):
                self.__class__.WIDGETS['playlists'][x].adjustPosition(self.width() - 60, self.height() - 233)
            self.playlistboxCreate.adjustPosition(self.width() - 60, self.height() - 233)
            self.playlistsboxLayout.setColumnStretch((self.width() - 60) // 200 + 1, 1)
        if self.lastState != self.windowState():
            self.updateState()
            self.lastState = self.windowState()

    def positionChanged(self, position):
        self.hometimecurrentLabel.setText(self.sec_to_time(position))
        self.hometimeSlider.blockSignals(True)
        self.hometimeSlider.setValue(position)
        if self.miniplayeron:
            # self.miniplayersongstatusLabel.setText(f"""{self.sec_to_time(position)} / {self.sec_to_time(self.player.duration())}\t\tVolume : {settings.volume}%\t{listOfSongs[settings.index]['artist']}""")
            self.miniplayersongtimeLabel.setText(
                f"{self.sec_to_time(position)} / {self.sec_to_time(self.player.duration())}")
            self.miniplayertimeSlider.blockSignals(True)
            self.miniplayertimeSlider.setValue(position)
            self.miniplayertimeSlider.blockSignals(False)
        self.hometimeSlider.blockSignals(False)
        if self.current_window_details['page'] == "home" and self.current_window_details['childpage'] == "lyric":
            self.homesonglyricWidget.refresh(self.sec_to_time(position + 2000 + self.lyricSync))

    def checkPlaylistEnd(self, event=None):
        if self.player.mediaStatus() == QMediaPlayer.EndOfMedia and self.playlist.currentIndex() == self.playlist.mediaCount():
            self.stop()
            settings.index = 0
            self.playlist.setCurrentIndex(settings.index)

    def songChanged(self, event=None):
        try:
            lastIndex = settings.index
            duration = self.player.duration()
            index = self.playlist.currentIndex()
            settings.index = index
            file = listOfSongs[index]['song']
            name = listOfSongs[index]['name']
            artist = listOfSongs[index]['artist']
            self.lyricSync = listOfSongs[index]['lyricsync']
            cover = scover(file)
            if cover is not None:
                img = Image.open(cover)
                img.convert('RGB')
                data = img.tobytes("raw", "RGB")
                qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
                image = QPixmap.fromImage(qim)
            if cover is None:
                qim = images[settings.theme]['songimg']
                image = QPixmap(qim)
            self.homesonglyricWidget.setDefaults()
            self.homesonglyricWidget.load()

            self.homesongtitleLabel.setText(name)
            self.homesongartistLabel.setText(artist)
            self.hometimeSlider.setMaximum(duration)
            if duration >= 0: self.hometimelengthLabel.setText(self.sec_to_time(duration))
            self.homesongwallimageLabel.setPixmap(image)
            self.homesongwallimageLabel.setHeight(self.width() - 60, self.height() - 233)

            try:
                self.__class__.WIDGETS['playlistitems'][lastIndex].updateState()
                self.__class__.WIDGETS['playlistitems'][settings.index].updateState()
                self.__class__.WIDGETS['playlistswidgets'][settings['playinglist']].WIDGETS['items'][
                    lastIndex].updateState()
                self.__class__.WIDGETS['playlistswidgets'][settings['playinglist']].WIDGETS['items'][
                    settings.index].updateState()
            except (KeyError, IndexError, ValueError):
                pass
            dumpsettings()

            if self.miniplayeron:
                self.miniplayertimeSlider.setMaximum(duration)
                self.miniplayersongtitleLabel.setText(name)
                # self.miniplayersongstatusLabel.setText(f"""00:00:00 / {self.sec_to_time(duration)}\t\tVolume : {settings.volume}%\t{artist}""")
                self.miniplayersongtimeLabel.setText(f"00:00:00 \ {self.sec_to_time(duration)}")
                self.miniplayersongartistLabel.setText(artist)
                self.miniplayersongimageLabel.setPixmap(image)  # .setImage(qim, 100, 100)
        except (RuntimeError, IndexError):
            self.stop()
        except FileNotFoundError:
            listOfSongs.pop(settings.index)
            listofplay[settings['playinglist']] = listOfSongs
            self.load()
            self.play(forceOpen=False)
            dumpplaylists()

    def open(self, event=None):
        global listOfSongs
        paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "mp3 Audio (*.mp3, *.m4a)All files (*.*)")
        if paths:
            self.stop()
            settings.sorttype = "Time added"
            settings.sortside = "Acsending"
            listOfSongs = []
            count147 = 0
            for x in paths:
                if x.endswith(".mp3") or x.endswith(".m4a"):
                    newdict = {}
                    tag = TinyTag.get(x)
                    newdict['no'] = count147
                    newdict['song'] = x
                    if tag.title:
                        newdict['name'] = tag.title
                    else:
                        newdict['name'] = ((x.split("/"))[-1]).split(".")
                        if len(newdict['name']) > 2:
                            newdict['name'] = ".".join(newdict['name'][:-1])
                        if len(newdict['name']) <= 2:
                            newdict['name'] = newdict['name'][0]
                    if tag.album:
                        newdict['genre'] = tag.genre
                    else:
                        newdict['genre'] = "Unknown"
                    if tag.album:
                        newdict['album'] = tag.album
                    else:
                        newdict['album'] = "Unknown"
                    if tag.artist:
                        newdict['artist'] = tag.artist
                    else:
                        newdict['artist'] = "Unknown"
                    filestat = os.stat(x)
                    date = time.localtime(filestat.st_mtime)
                    year = date[0]
                    month = date[1]
                    day = date[2]
                    hour = "%02d" % date[3]
                    minute = "%02d" % date[4]
                    second = "%02d" % date[5]
                    strYear = str(year)[0:]
                    if month <= 9:
                        strMonth = '0' + str(month)
                    else:
                        strMonth = str(month)
                    if day <= 9:
                        strDay = '0' + str(day)
                    else:
                        strDay = str(day)
                    newdict['date'] = int(
                        "{}".format(strYear + strMonth + strDay + str(hour) + str(minute) + str(second)))
                    newdict['lyricsync'] = 0
                    listOfSongs.append(newdict)
                    count147 += 1
            listofplay['playlist'] = listOfSongs
            settings['playinglist'] = 'playlist'
            settings['selectinglist'] = 'playlist'
            dumpplaylists()
            settings.index = 0
            self.load()
            self.play(forceOpen=False)

    def refreshPlaylists(self):
        try:
            clearLayout(self.playlistsboxLayout)
        except Exception as e:
            print(e)

        self.__class__.WIDGETS['playlists'] = {}
        for i, x in enumerate(list(listofplay.keys())):
            w = PlaylistsItem(i, x, self)
            self.__class__.WIDGETS['playlists'][x] = w
            self.playlistsboxLayout.addWidget(self.__class__.WIDGETS['playlists'][x], 0, i)
            self.__class__.WIDGETS['playlists'][x].adjustPosition(self.width() - 60, self.height() - 233)
        i = len(list(listofplay.keys()))
        self.playlistboxCreate = CreatePlayList(self, i)
        self.playlistboxCreate.adjustPosition(self.width() - 60, self.height() - 233)
        self.playlistsboxLayout.addWidget(self.playlistboxCreate, 0, i)
        self.playlistsboxLayout.setRowStretch(i + 1, 1)
        self.playlistsboxLayout.setColumnStretch((self.width() - 60) // 200 + 1, 1)

    def pack(self, pack):
        if pack['sep']:
            self.playinglistWidgetLayout.addStretch(1)
        if not pack['sep']:
            w = ListItem(self, pack['song'], pack['pack'])
            self.__class__.WIDGETS['playlistitems'].append(w)
            self.playinglistWidgetLayout.addWidget(self.__class__.WIDGETS['playlistitems'][pack['pack']])

    def refreshPlaylist(self, sec):
        try:
            clearLayout(self.playinglistWidgetLayout)
        except Exception as e:
            print(e)
        self.__class__.WIDGETS['playlistitems'] = []
        for i, x in enumerate(listOfSongs):
            if self.lastrefreshSec != sec: break
            w = ListItem(self, x, i)
            self.__class__.WIDGETS['playlistitems'].append(w)
            self.playinglistWidgetLayout.addWidget(self.__class__.WIDGETS['playlistitems'][-1])
        self.playinglistWidgetLayout.addStretch(1)
        try:
            self.__class__.WIDGETS['playlistitems'][settings.index].playUpdate()
        except (KeyError, IndexError):
            pass
        # if self.playlistThread.isRunning():
        #     self.playlistThread.exit()
        # self.playlistWorker.setSec(sec)
        # self.playlistThread.start()

    def load(self):
        pass
        ## self.__class__.SESSION['selected_list'] = []
        ## self.playlist.clear()
        ## tmpr = []
        ## for x in listOfSongs:
        ##     if os.path.exists(x['song']):
        ##         self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(x['song'])))
        ##     if not os.path.exists(x['song']):
        ##         tmpr.append(x)
        ## for x in tmpr:
        ##     listOfSongs.remove(x)
        ## listofplay[settings['playinglist']] = listOfSongs
        ## self.playlist.setCurrentIndex(settings.index)
        ## dumpsettings()
        ## sec = time.time()
        ## self.lastrefreshSec = sec
        ## self.updateListTool()
        ## QTimer.singleShot(20, lambda: self.refreshPlaylist(sec))
        ## if not 'playlistswidgets' in self.__class__.WIDGETS: self.__class__.WIDGETS['playlistswidgets'] = {}
        ## if settings['selectinglist'] in self.__class__.WIDGETS['playlistswidgets'] and self.current_window_details['page'] != "playlists":
        ##     self.__class__.WIDGETS['playlistswidgets'][settings['selectinglist']].lastrefreshSec = sec
        ##     QTimer.singleShot(20, lambda: self.__class__.WIDGETS['playlistswidgets'][settings['selectinglist']].refreshPlaylist(sec))

    def playItem(self, index):
        if index < len(listOfSongs):
            self.stop()
            self.playlist.setCurrentIndex(index)
            self.play(forceOpen=False)

    def previous(self, event=None):
        self.playlist.previous()
        if self.player.state() != QMediaPlayer.PlayingState or self.player.state() == QMediaPlayer.PausedState:
            self.play(forceOpen=True)

    def play(self, event=None, forceOpen=True):
        if self.player.state() != QMediaPlayer.PlayingState:
            if not self.playlist.isEmpty():
                self.homebuttonplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['pauseimg'])))
                self.miniplayerplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['pauseimg'])))
                self.homebuttonplaypauseButton.setToolTip("Pause")
                self.songChanged()
                self.player.play()
            if self.playlist.isEmpty():
                if forceOpen: self.open()
                if not forceOpen: self.stop()
        else:
            self.player.pause()
            if self.player.state() == QMediaPlayer.PausedState:
                self.homebuttonplaypauseButton.setToolTip("Play")
                self.homebuttonplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
                self.miniplayerplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
            else:
                self.homebuttonplaypauseButton.setToolTip("Pause")
                self.homebuttonplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['pauseimg'])))
                self.miniplayerplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['pauseimg'])))
            self.homebuttonplaypauseButton.update()
        try:
            self.__class__.WIDGETS["playlistitems"][settings.index].playUpdate()
        except Exception as e:
            print(e)
        try:
            self.__class__.WIDGETS["playlistswidgets"][settings['playinglist']].WIDGETS['items'][
                settings.index].playUpdate()
        except Exception as e:
            print(e)

    def next(self, event=None):
        self.playlist.next()
        if self.player.state() != QMediaPlayer.PlayingState or self.player.state() == QMediaPlayer.PausedState:
            self.play(forceOpen=True)

    def stop(self, event=None):
        self.homebuttonplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
        self.miniplayerplaypauseButton.setIcon(QIcon(QPixmap(images[settings.theme]['playimg'])))
        self.homesongtitleLabel.setText("Feel The Music")
        self.homesongartistLabel.setText("Unknown")
        self.homesongwallimageLabel.setPixmap(QPixmap(images[settings.theme]['songimg']))
        self.homesongwallimageLabel.setHeight(self.width() - 60, self.height() - 233)
        self.player.stop()
        self.homebuttonplaypauseButton.setToolTip("Play")

        if self.miniplayeron:
            self.miniplayersongtitleLabel.setText("Feel The Music")
            self.miniplayersongimageLabel.setPixmap(QPixmap(images[settings.theme]['coverimg']))
            self.miniplayersongtimeLabel.setText("00:00:00 / 00:00:00")
            self.miniplayersongartistLabel.setText("Unknown")
            self.miniplayertimeSlider.setMaximum(0)

    def playSelectedList(self, event=None):
        global listOfSongs
        if len(self.__class__.SESSION['selected_list']):
            newPlaylist = [listofplay[settings['selectinglist']][x] for x in self.__class__.SESSION['selected_list']]
            self.stop()
            self.__class__.SESSION['selected_list'] = []
            listOfSongs = newPlaylist
            listofplay['playlist'] = listOfSongs
            settings['playinglist'] = 'playlist'
            settings.index = 0
            if settings.sorttype != "Shuffle":
                self.lastSortType = settings.sorttype
                settings.sorttype = "Shuffle"
            self.load()
            self.shuffleButton()
            index = 0
            self.playlist.setCurrentIndex(index)
            settings.index = index
            dumpsettings()
            dumpplaylists()
            self.play(forceOpen=True)
            self.change_windowmode(new_windowmode={"page": "home", "childpage": "main"})

    def shuffleSelectedList(self, event=None):
        global listOfSongs
        if len(self.__class__.SESSION['selected_list']):
            newPlaylist = [listofplay[settings['selectinglist']][x] for x in self.__class__.SESSION['selected_list']]
            self.stop()
            self.__class__.SESSION['selected_list'] = []
            listOfSongs = newPlaylist
            listofplay['playlist'] = listOfSongs
            settings['playinglist'] = 'playlist'
            settings.index = 0
            if settings.sorttype == "Shuffle": settings.sorttype = self.lastSortType
            self.load()
            self.shuffleButton()
            index = 0
            self.playlist.setCurrentIndex(index)
            settings.index = index
            dumpsettings()
            dumpplaylists()
            self.play(forceOpen=True)
            self.change_windowmode(new_windowmode={"page": "home", "childpage": "main"})

    def addSelectedList(self, event=None):
        if len(self.__class__.SESSION['selected_list']):
            menu = QMenu(self)
            menu.setCursor(Qt.PointingHandCursor)
            menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #6D6D6D;
                font: 16px Segoe UI;
                color: black;
            }
            QAction {
                background-color: white;
                border: 0px;
                font: 16px Segoe UI;
                color: #6D6D6D;
                padding: 5px;
                margin-top: 4px;
                margin-bottom: 4px;
            }
            QAction:hover {
                background-color: #699DE2;
                color: white;
            }
            """)
            options = [x for x in list(listofplay.keys())]
            options.remove(settings['selectinglist'])
            for x in options:
                action = QAction(x if x != 'playlist' else "Playlist", self)
                menu.addAction(action)
            menu.triggered.connect(lambda event: self.addToSelectedList(event.text().strip()))
            pos1 = self.playinglisttooladdButton.pos()
            pos2 = self.pos()
            pos = self.playinglisttooladdButton.mapToGlobal(self.playinglisttooladdButton.rect().topLeft())
            menu.popup(QPoint(pos.x(), pos.y() - (25 * len(options))))

    def addToSelectedList(self, to):
        global listOfSongs, listofplay
        if to == "Playlist": to = "playlist"
        newPlaylist = [listofplay[settings['selectinglist']][x] for x in self.__class__.SESSION['selected_list']]
        for x in range(len(self.__class__.WIDGETS['playlistitems'])):
            self.__class__.WIDGETS['playlistitems'][x].deselect()
        self.__class__.SESSION['selected_list'] = []
        listofplay[to] += newPlaylist
        dumpplaylists()

    def popSelectedList(self, event=None):
        if len(self.__class__.SESSION['selected_list']):
            menu = QMenu(self)
            menu.setCursor(Qt.PointingHandCursor)
            menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #6D6D6D;
                font: 16px Segoe UI;
                color: black;
            }
            QAction {
                background-color: white;
                border: 0px;
                font: 16px Segoe UI;
                color: #6D6D6D;
                padding: 5px;
                margin-top: 4px;
                margin-bottom: 4px;
            }
            QAction:hover {
                background-color: #699DE2;
                color: white;
            }
            """)
            options = {"Remove from playlist": self.removeSelectedList, "Delete the files": self.deleteSeletedList}
            for option in list(options.keys()):
                action = QAction(option, self)
                menu.addAction(action)
            menu.triggered.connect(lambda event: options[event.text().strip()]())
            pos1 = self.playinglisttoolremoveButton.pos()
            pos2 = self.pos()
            pos = self.playinglisttoolremoveButton.mapToGlobal(self.playinglisttoolremoveButton.rect().topLeft())
            menu.popup(QPoint(pos.x(), pos.y() - (25 * len(options))))

    def removeSelectedList(self, event=None):
        global listOfSongs, listofplay
        if len(self.__class__.SESSION['selected_list']):
            lastPosition = self.player.position()
            lastIndex = settings.index
            forcePlay = False
            if self.player.state() == QMediaPlayer.PlayingState:
                forcePlay = True
            self.stop()
            selectedList = [x for x in self.__class__.SESSION['selected_list']]
            for x in range(len(self.__class__.WIDGETS['playlistitems'])):
                self.__class__.WIDGETS['playlistitems'][x].deselect()
            self.__class__.SESSION['selected_list'] = []
            index = settings.index
            selectedList.sort(reverse=True)
            for x in selectedList:
                listOfSongs.pop(x)
            listofplay[settings['selectinglist']] = listOfSongs
            if len(listOfSongs) > 0:
                selectedList.append(index)
                selectedList.sort()
                del_index = selectedList.index(index)
                new_index = index - del_index
                if new_index < 0 or new_index >= len(listOfSongs): new_index = 0
                settings.index = new_index
                self.load()
                settings.index = new_index
                self.playlist.setCurrentIndex(new_index)
                if lastIndex not in selectedList:
                    self.player.setPosition(lastPosition)
                if forcePlay: self.play(forceOpen=False)
            if len(listOfSongs) <= 0:
                settings['selectinglist'] = 'playlist'
                settings['playinglist'] = 'playlist'
                listOfSongs = listofplay[settings['playinglist']]
                settings.index = 0
                if settings.sorttype != "Shuffle":
                    self.lastSortType = settings.sorttype
                    settings.sorttype = "Shuffle"
                self.load()
                self.shuffleButton()
                index = 0
                self.playlist.setCurrentIndex(index)
                settings.index = index
                dumpsettings()
                if forcePlay: self.play(forceOpen=False)
            dumpsettings()
            dumpplaylists()

    def deleteSeletedList(self, event=None):
        if len(self.__class__.SESSION['selected_list']):
            lastPosition = self.player.position()
            lastIndex = settings.index
            forcePlay = False
            if self.player.state() == QMediaPlayer.PlayingState:
                forcePlay = True
            self.stop()
            selectedList = [x for x in self.__class__.SESSION['selected_list']]
            for x in range(len(self.__class__.WIDGETS['playlistitems'])):
                self.__class__.WIDGETS['playlistitems'][x].deselect()
            self.__class__.SESSION['selected_list'] = []
            index = settings.index
            selectedList.sort(reverse=True)
            for x in selectedList:
                try:
                    os.remove(listOfSongs[x]['song'])
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
                listOfSongs.pop(x)
            listofplay[settings['selectinglist']] = listOfSongs
            if len(listOfSongs) > 0:
                selectedList.append(index)
                selectedList.sort()
                del_index = selectedList.index(index)
                new_index = index - del_index
                if new_index < 0 or new_index >= len(listOfSongs): new_index = 0
                settings.index = new_index
                self.load()
                settings.index = new_index
                self.playlist.setCurrentIndex(new_index)
                if lastIndex not in selectedList:
                    self.player.setPosition(lastPosition)
                if forcePlay: self.play(forceOpen=False)
            if len(listOfSongs) <= 0:
                settings['selectinglist'] = 'playlist'
                settings['playinglist'] = 'playlist'
                listOfSongs = listofplay[settings['playinglist']]
                settings.index = 0
                if settings.sorttype != "Shuffle":
                    self.lastSortType = settings.sorttype
                    settings.sorttype = "Shuffle"
                self.load()
                self.shuffleButton()
                index = 0
                self.playlist.setCurrentIndex(index)
                settings.index = index
                dumpsettings()
                if forcePlay: self.play(forceOpen=False)
            dumpsettings()
            dumpplaylists()

    def removeDuplicates(self, event=None):
        global listofplay, listOfSongs, settings
        newListIndexes = []
        newListSongs = []
        deleteListIndexes = []
        for i in range(len(listofplay[settings['selectinglist']])):
            if listofplay[settings['selectinglist']][i]['song'] in newListSongs:
                deleteListIndexes.append(i)
            if not listofplay[settings['selectinglist']][i]['song'] in newListSongs:
                newListSongs.append(listofplay[settings['selectinglist']][i]['song'])
                newListIndexes.append(i)
        deleteListIndexes.sort(reverse=True)
        for x in deleteListIndexes:
            listofplay[settings['selectinglist']].pop(x)
        if settings['selectinglist'] == settings['playinglist']:
            lastPosition = self.player.position()
            forcePlay = False
            if self.player.state() == QMediaPlayer.PlayingState:
                forcePlay = True
            self.stop()
            listOfSongs = listofplay[settings['selectinglist']]
            index = settings.index
            deleteListIndexes.append(index)
            deleteListIndexes.sort()
            del_index = deleteListIndexes.index(index)
            new_index = index - del_index
            if new_index < 0 or new_index >= len(listOfSongs): new_index = 0
            settings.index = new_index
            self.load()
            settings.index = new_index
            self.playlist.setCurrentIndex(new_index)
            self.player.setPosition(lastPosition)
            if forcePlay: self.play(forceOpen=False)
        print("[REMOVE DUPLICATES]", len(deleteListIndexes), "items.")

    def selectAll(self, event=None):
        if len(listofplay[settings['selectinglist']]) != len(self.__class__.SESSION['selected_list']):
            for x in range(len(self.__class__.WIDGETS['playlistitems'])):
                self.__class__.WIDGETS['playlistitems'][x].select()
        else:
            for x in range(len(self.__class__.WIDGETS['playlistitems'])):
                self.__class__.WIDGETS['playlistitems'][x].deselect()

    def scrollToSong(self, event=None):
        try:
            self.playinglistScroll.verticalScrollBar().setValue(
                self.__class__.WIDGETS["playlistitems"][settings.index].y())
        except (IndexError, KeyError):
            pass

    def updateListTool(self, event=None):
        self.playinglisttoolselectedcountLabel.setText(
            f"{len(self.__class__.SESSION['selected_list'])} Song(s) selected" if len(
                self.__class__.SESSION['selected_list']) else "")
        if len(listofplay[settings['selectinglist']]) != len(self.__class__.SESSION['selected_list']):
            self.playinglisttoolselectallButton.setIcon(QIcon(QPixmap(images['common']['selectallimg'])))
        else:
            self.playinglisttoolselectallButton.setIcon(QIcon(QPixmap(images['common']['unselectallimg'])))

    def createPlaylistUI(self, playlist):
        widget = PlaylistsListWidget(self, playlist)
        self.__class__.WIDGETS['playlistswidgets'][playlist] = widget

        self.playlistsStack.addWidget(self.__class__.WIDGETS['playlistswidgets'][playlist])

    def backword_page(self, event=None):
        try:
            newwin = self.window_log[-1]
            self.change_windowmode(new_windowmode=newwin)
            self.window_log.pop(-1)
            self.window_log.pop(-1)
        except IndexError:
            pass

    def change_windowmode(self, new_windowmode):
        if new_windowmode != self.current_window_details:
            if self.current_window_details['page'] == "home":
                if self.current_window_details['childpage'] == "main":
                    pass
                if self.current_window_details['childpage'] == "lyric":
                    # self.homesonglyricWidget.setVisible(False)
                    # self.homesongwallimageLabel.setVisible(True)
                    # self.homecentralWidget.setCurrentWidget(self.homesongwallimageLabel)
                    self.homeactiontolyricButton.setIcon(QIcon(QPixmap(images[settings.theme]['tolyricimg'])))
                    self.homeactiontolyricButton.clicked.connect(
                        lambda event: self.change_windowmode(new_windowmode={'page': "home", "childpage": "lyric"}))
                if self.current_window_details['childpage'] == "playlist":
                    self.hide_miniplayer()
                    self.menumenuButton.clicked.disconnect()
                    self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['menuimg'])))
                    self.playinglist.setVisible(False)
                    self.mainStack.setVisible(True)
                if self.current_window_details['childpage'] == "download":
                    self.homeactiontolyricButton.setVisible(True)
                    self.menumenuButton.clicked.disconnect()
                    self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['menuimg'])))
            if self.current_window_details['page'] == "playlists":
                # self.mainLayout.removeWidget(self.playlistsWidget)
                self.hide_miniplayer()
                if self.current_window_details['childpage'] == "main":
                    pass
                if self.current_window_details['childpage'] == "playlist":
                    settings['selectinglist'] = settings['playinglist']
                    self.menumenuButton.clicked.disconnect()
                    self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['menuimg'])))
                if self.current_window_details['childpage'] == "create":
                    self.upperShadowWidget.setVisible(False)
            if self.current_window_details['page'] == "explore":
                self.hide_miniplayer()
                if self.current_window_details['childpage'] == "main":
                    pass
                if self.current_window_details['childpage'] == "downloads":
                    self.menumenuButton.clicked.disconnect()
                    self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['menuimg'])))

            if new_windowmode['page'] == "home":
                if new_windowmode['childpage'] == "main":
                    self.init_home_main()
                if new_windowmode['childpage'] == "lyric":
                    self.init_home_lyric()
                if new_windowmode['childpage'] == "playlist":
                    self.init_home_playlist()
                if new_windowmode['childpage'] == "download":
                    self.init_home_download()
            if new_windowmode['page'] == "playlists":
                if new_windowmode['childpage'] == "main":
                    self.init_playlists_main()
                if new_windowmode['childpage'] == "playlist":
                    self.init_playlists_playlist(new_windowmode['playlist'])
                if new_windowmode['childpage'] == "create":
                    self.init_playlists_create()
            if new_windowmode['page'] == "explore":
                if new_windowmode['childpage'] == "main":
                    self.init_explore_main()
                if new_windowmode['childpage'] == "downloads":
                    self.init_explore_downloads()

    def init_home_main(self):
        self.mainStack.setCurrentWidget(self.homeWidget)
        self.homecentralWidget.setCurrentWidget(self.homesongwallimageLabel)
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "home", 'childpage': 'main'}

    def init_home_lyric(self):
        self.mainStack.setCurrentWidget(self.homeWidget)
        # self.homesonglyricWidget.setVisible(True)
        # self.homesongwallimageLabel.setVisible(False)
        self.homecentralWidget.setCurrentWidget(self.homesonglyricWidget)
        self.homesonglyricWidget.refresh(self.sec_to_time(self.player.position() + 2000 + self.lyricSync))
        self.homeactiontolyricButton.clicked.disconnect()
        self.homeactiontolyricButton.clicked.connect(
            lambda event: self.change_windowmode(new_windowmode={'page': "home", 'childpage': "main"}))
        self.homeactiontolyricButton.setIcon(QIcon(QPixmap(images[settings.theme]['tohomeimg'])))
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "home", 'childpage': 'lyric'}

    def init_home_playlist(self):
        self.mainStack.setVisible(False)
        self.show_miniplayer()
        self.playinglist.setVisible(True)
        self.menumenuButton.clicked.connect(self.backword_page)
        self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['backwordimg'])))
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "home", 'childpage': 'playlist'}

    def init_home_download(self):
        self.homecentralWidget.setCurrentWidget(self.homesongdownloadWidget)
        self.menumenuButton.clicked.connect(self.backword_page)
        self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['backwordimg'])))
        self.homesongdownloadWidget.forceSearch()
        self.homeactiontolyricButton.setVisible(False)
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "home", 'childpage': 'download'}

    def init_playlists_main(self):
        self.mainStack.setCurrentWidget(self.playlistsWidget)
        self.playlistsStack.setCurrentWidget(self.playlistsScroll)
        self.show_miniplayer()
        for x in list(self.__class__.WIDGETS['playlists'].keys()):
            self.__class__.WIDGETS['playlists'][x].adjustPosition(self.width() - 60, self.height() - 233)
            self.__class__.WIDGETS['playlists'][x].refreshItem()
        self.playlistboxCreate.adjustPosition(self.width() - 60, self.height() - 233)
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "playlists", 'childpage': 'main'}

    def init_playlists_playlist(self, playlist):
        self.mainStack.setCurrentWidget(self.playlistsWidget)

        settings['selectinglist'] = playlist

        if "playlistswidgets" not in self.__class__.WIDGETS: self.__class__.WIDGETS['playlistswidgets'] = {}
        if playlist not in self.__class__.WIDGETS['playlistswidgets']: self.createPlaylistUI(playlist)

        self.playlistsStack.setCurrentWidget(self.__class__.WIDGETS['playlistswidgets'][playlist])
        self.__class__.WIDGETS['playlistswidgets'][playlist].updateTracker()

        if "items" in self.__class__.WIDGETS['playlistswidgets'][playlist].WIDGETS:
            for x in range(len(self.__class__.WIDGETS['playlistswidgets'][playlist].WIDGETS['items'])):
                self.__class__.WIDGETS['playlistswidgets'][playlist].WIDGETS['items'][x].updateState()

        self.menumenuButton.clicked.connect(self.backword_page)
        self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['backwordimg'])))

        self.show_miniplayer()
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "playlists", 'childpage': 'playlist', 'playlist': playlist}

    def init_playlists_create(self):
        self.shadowStack.setCurrentWidget(self.shadowcreateWidget)
        self.upperShadowWidget.setVisible(True)

        self.shadowcreateWidget.playlistnameEdit.clear()

        self.show_miniplayer()
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "playlists", 'childpage': 'create'}

    def init_explore_main(self):
        self.mainStack.setCurrentWidget(self.exploreWidget)
        self.exploreStack.setCurrentWidget(self.exploreYTWidget)
        self.show_miniplayer()
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "explore", 'childpage': 'main'}

    def init_explore_downloads(self):
        self.mainStack.setCurrentWidget(self.exploreWidget)
        self.exploreStack.setCurrentWidget(self.exploreDownloadsWidget)

        self.menumenuButton.clicked.connect(self.backword_page)
        self.menumenuButton.setIcon(QIcon(QPixmap(images[settings.theme]['backwordimg'])))

        self.show_miniplayer()
        self.window_log.append(self.current_window_details)
        self.current_window_details = {'page': "explore", 'childpage': 'downloads'}


if __name__ == '__main__':
    app = QApplication(sys.argv)

    """---program variables---"""
    try:
        width, height = [int(x) for x in read_file("{}\\mwd.File".format(resourcedir)).split("\n")]
    except (FileNotFoundError, ValueError) as e:
        print('e003', e)
        width = 800
        height = 600

    settings = Setting()
    listOfSongs = []
    images = {
        "light": {
            "helody": "lib\\resources\\L000.png",
            "sortimg": "lib\\resources\\L001.png",
            "maximizeimg": "lib\\resources\\L002.png",
            "minimizeimg": "lib\\resources\\L003.png",
            "overplay1img": "lib\\resources\\L004.png",
            "overplay2img": "lib\\resources\\L005.png",
            "shuffleimg": "lib\\resources\\L006.png",
            "volume1img": "lib\\resources\\L007.png",
            "volume2img": "lib\\resources\\L008.png",
            "volume3img": "lib\\resources\\L009.png",
            "volume4img": "lib\\resources\\L010.png",
            "openimg": "lib\\resources\\L011.png",
            "previousimg": "lib\\resources\\L012.png",
            "playimg": "lib\\resources\\L013.png",
            "pauseimg": "lib\\resources\\L014.png",
            "nextimg": "lib\\resources\\L015.png",
            "stopimg": "lib\\resources\\L016.png",
            "playlistimg": "lib\\resources\\L017.png",
            "songimg": "lib\\resources\\L018.png",
            "homeimg": "lib\\resources\\L019.png",
            "playlistimg": "lib\\resources\\L020.png",
            "menuimg": "lib\\resources\\L021.png",
            "exploreimg": "lib\\resources\\L022.png",
            "settingimg": "lib\\resources\\L023.png",
            "coverimg": "lib\\resources\\L024.png",
            "songinfoimg": "lib\\resources\\L026.png",
            "backwordimg": "lib\\resources\\L027.png",
            "minimizewinimg": "lib\\resources\\L029.png",
            "maximizewinimg": "lib\\resources\\L031.png",
            "restoreimg": "lib\\resources\\L033.png",
            "restoreimg": "lib\\resources\\L034.png",
            "closeimg": "lib\\resources\\L033.png",
            "tolyricimg": "lib\\resources\\L035.png",
            "tohomeimg": "lib\\resources\\L036.png",
            "trackerimg": "lib\\resources\\L037.png",
            "downloadsimg": "lib\\resources\\L038.png"
        },

        "dark": {
            "helody": "lib\\resources\\D000.png",
            "sortimg": "lib\\resources\\D001.png",
            "maximizeimg": "lib\\resources\\D002.png",
            "minimizeimg": "lib\\resources\\D003.png",
            "overplay1img": "lib\\resources\\D004.png",
            "overplay2img": "lib\\resources\\D005.png",
            "shuffleimg": "lib\\resources\\D006.png",
            "volume1img": "lib\\resources\\D007.png",
            "volume2img": "lib\\resources\\D008.png",
            "volume3img": "lib\\resources\\D009.png",
            "volume4img": "lib\\resources\\D010.png",
            "openimg": "lib\\resources\\D011.png",
            "previousimg": "lib\\resources\\D012.png",
            "playimg": "lib\\resources\\D013.png",
            "pauseimg": "lib\\resources\\D014.png",
            "nextimg": "lib\\resources\\D015.png",
            "stopimg": "lib\\resources\\D016.png",
            "playlistimg": "lib\\resources\\D017.png",
            "songimg": "lib\\resources\\D018.png",
            "homeimg": "lib\\resources\\D019.png",
            "playlistimg": "lib\\resources\\D020.png",
            "menuimg": "lib\\resources\\D021.png",
            "exploreimg": "lib\\resources\\D022.png",
            "settingimg": "lib\\resources\\D023.png",
            "coverimg": "lib\\resources\\D024.png",
            "songinfoimg": "lib\\resources\\D026.png",
            "backwordimg": "lib\\resources\\D027.png",
            "minimizewinimg": "lib\\resources\\D029.png",
            "maximizewinimg": "lib\\resources\\D031.png",
            "restoreimg": "lib\\resources\\D033.png",
            "restoreimg": "lib\\resources\\D034.png",
            "closeimg": "lib\\resources\\D033.png",
            "tolyricimg": "lib\\resources\\D035.png",
            "tohomeimg": "lib\\resources\\D036.png",
            "trackerimg": "lib\\resources\\D037.png",
            "downloadsimg": "lib\\resources\\D038.png"
        },

        "common": {
            "playimg": "lib\\resources\\C003.png",
            "selectimg": "lib\\resources\\C001.png",
            "selectedimg": "lib\\resources\\C002.png",
            "shuffleimg": "lib\\resources\\C004.png",
            "editimg": "lib\\resources\\C005.png",
            "removeimg": "lib\\resources\\C006.png",
            "addimg": "lib\\resources\\C007.png",
            "playingimg": "lib\\resources\\C015.gif",
            "selectallimg": "lib\\resources\\C009.png",
            "unselectallimg": "lib\\resources\\C010.png",
            "removedupimg": "lib\\resources\\C011.png",
            "playlistsimg": "lib\\resources\\C012.png",
            "negativeimg": "lib\\resources\\C013.png",
            "restoreimg": "lib\\resources\\C014.png",
            "searchimg": "lib\\resources\\C016.png",
            "sortimg": "lib\\resources\\C017.png",
            "avatar-ske": "lib\\resources\\C018.gif",
            "video-ske": "lib\\resources\\C0119.gif"
        }
    }

    logging.basicConfig(level='INFO')
    controller = DBController()
    api = API()
    w = Window(width, height)
    sys.exit(app.exec_())
