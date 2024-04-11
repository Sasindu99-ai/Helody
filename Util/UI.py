from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

__all__ = ["UI"]


class UI:
    @staticmethod
    def pixmap(file_name: str, width: int = None, height: int = None,
               aspect_ratio_mode: Qt.AspectRatioMode = Qt.IgnoreAspectRatio,
               transform_mode: Qt.TransformationMode = Qt.FastTransformation) -> QPixmap:
        pixmap = QPixmap()
        pixmap.load(file_name)
        if width is None and height is not None:
            pixmap.scaled(width, height, aspect_ratio_mode, transform_mode)
        return pixmap
