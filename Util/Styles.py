from PyQt5.QtCore import QSize

# Styles

# Menu Button
menuButton = """
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
"""

# Mini Button
miniButton = """
QToolButton {
    background: #737373;
    margin-left: 5px;
    margin-right: 5px;
    border: none;
}

QToolButton:hover {
    background: #000000;
}
"""
miniButtonSize = QSize(14, 14)

# Default Slider
defaultSlider = """
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
"""

# Default Button
defaultButton = """
QToolButton {
    background-color: #737373;
    border: none;
    margin: 10px;
}
QToolButton:hover {
    background-color: #000000;
}
"""
defaultButtonSize = QSize(24, 24)
