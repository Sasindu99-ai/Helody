from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QSizePolicy, QStackedWidget, QWidget

__all__ = ["Window"]

from Components.Common.Margin import Margin


class Window(QMainWindow):
    __VIEWS = []
    __PAGES = []
    mainWidget: QWidget
    mainLayout: QGridLayout
    centralWidget: QStackedWidget

    def __init__(self, **__kwargs):
        """
        Window(parent: Optional[QWidget] = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags(),
        row: int = 1, column: int = 1, rowSpan: int = 1, columnSpan: int = 1,
        alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
        """
        super(QMainWindow, self).__init__(
            __kwargs.get("parent"),
            __kwargs.get("flags") if "flags" in __kwargs else Qt.WindowFlags())

        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(Margin(5))
        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)

        self.centralWidget = QStackedWidget()
        row = __kwargs.get("row") if "row" in __kwargs.keys() else 1
        column = __kwargs.get("column") if "column" in __kwargs.keys() else 1
        row_span = __kwargs.get(
            "rowSpan") if "rowSpan" in __kwargs.keys() else 1
        column_span = __kwargs.get(
            "columnSpan") if "columnSpan" in __kwargs.keys() else 1
        alignment = __kwargs.get(
            "alignment") if "alignment" in __kwargs.keys() else Qt.Alignment()
        self.mainLayout.addWidget(self.centralWidget, row, column, row_span,
                                  column_span, alignment)

        self.setCentralWidget(self.mainWidget)

    def navigate(self, view):
        resume = False
        if view is None:
            return
        if view in self.__VIEWS:
            resume = True
        if view not in self.__VIEWS:
            self.__VIEWS.append(view)
            page = view(self)
            self.__PAGES.append(page)
            self.centralWidget.addWidget(page)
        self.centralWidget.setCurrentIndex(self.__VIEWS.index(view))
        if resume:
            self.__PAGES[self.__VIEWS.index(view)].onResume()
        if not resume:
            self.__PAGES[self.__VIEWS.index(view)].onCreate()
