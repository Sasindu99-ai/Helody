from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

__all__ = ["UI"]


class UI:

    @staticmethod
    def pixmap(
        file_name: str,
        width: int = None,
        height: int = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.FastTransformation
    ) -> QPixmap:
        pixmap = QPixmap()
        pixmap.load(file_name)
        if width is None and height is not None:
            pixmap.scaled(width, height, aspect_ratio_mode, transform_mode)
        return pixmap

    @staticmethod
    def icon(
        file_name: str,
        width: int = None,
        height: int = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.FastTransformation
    ) -> QIcon:
        return QIcon(
            UI.pixmap(file_name, width, height, aspect_ratio_mode,
                      transform_mode))

    @staticmethod
    def dp(unit: int, devicePixelRatio: int) -> int:  # noqa
        return unit * devicePixelRatio

    @staticmethod
    def sp(unit: int, devicePixelRatio: int) -> int:  # noqa
        return unit * devicePixelRatio

    @staticmethod
    def colorHex(color: tuple) -> str:  # noqa
        return "#{:02x}{:02x}{:02x}".format(*color)
