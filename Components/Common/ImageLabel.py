from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QPixmap, QPainterPath, QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from Util import UI


class ImageViewer(QLabel):
    _pixmap: QPixmap
    _scaled: QPixmap
    _radius: int = 0
    _sizeHint: QSize = QSize()
    _ratio: Qt.AspectRatioMode = Qt.KeepAspectRatioByExpanding
    _transformation: Qt.TransformationMode = Qt.SmoothTransformation

    def __init__(self, image: str | None = None, antialiasing=True):
        super().__init__()
        self.Antialiasing = antialiasing
        self._radius = 0
        if image:
            self.setImage(image)

    def setImage(self, image: str):  # noqa
        self._pixmap = UI.pixmap(image)
        self._sizeHint = self._pixmap.size()
        self.updateGeometry()
        self.updateScaled()

    def setAspectRatio(self, ratio: Qt.AspectRatioMode):  # noqa
        if self._ratio != ratio:
            self._ratio = ratio
            self.updateScaled()

    def setTransformation(self, transformation: Qt.TransformationMode):  # noqa
        if self._transformation != transformation:
            self._transformation = transformation
            self.updateScaled()

    def updateScaled(self):  # noqa
        if self._pixmap is not None:
            self._scaled = self._pixmap.scaled(self.size(), self._ratio, self._transformation)
        self.update()

    def sizeHint(self):
        return self._sizeHint

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateScaled()

    def paintEvent(self, event):
        if not self._pixmap:
            return
        qp = QPainter(self)
        r = self._scaled.rect()
        r.moveCenter(self.rect().center())
        if self.Antialiasing:
            qp.setRenderHint(QPainter.Antialiasing, True)
            qp.setRenderHint(QPainter.HighQualityAntialiasing, True)
            qp.setRenderHint(QPainter.SmoothPixmapTransform, True)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)
        qp.setClipPath(path)
        qp.drawPixmap(r, self._scaled)
        self.update()

    def setHeight(self, width, height):  # noqa
        size: QSize = QSize(min(width, height), min(width, height))
        self._radius = size.width() / 2
        if self._pixmap:
            self._sizeHint = size
            self.updateGeometry()
            self._scaled = self._pixmap.scaled(size, self._ratio, self._transformation)
            self.update()


class ImageLabel(QWidget):
    image: ImageViewer

    def __init__(self, image: str | None = None, antialiasing=True):
        super(ImageLabel, self).__init__()

        self.setLayout(QHBoxLayout(self))
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.image = ImageViewer(image, antialiasing)
        self.layout().addWidget(self.image)

        self.setSize(self.width(), self.height())

    def setPixmap(self, image: str):  # noqa
        self.image.setImage(image)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.setSize(a0.size().width(), a0.size().height())

    def setSize(self, width: int, height: int):  # noqa
        self.image.setHeight(width, height)
