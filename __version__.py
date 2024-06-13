# Version Details:
__version__ = "0.0.1"
__title__ = "Helody"
__project__ = "Helody"
__last_update__ = "2024-04-09"
__author__ = "Sasindu Wijetunga"
__author_email__ = "helody.helodycreations@gmail.com"
__license__ = "MIT"
__url__ = ""
__description__ = "A music player for the modern age."
__long_description__ = ""
__download_url__ = ""
__platforms__ = "Windows, macOS, Linux"
__keywords__ = "music, player, modern, helody, helodycreations, helodyplayer"
__classifiers__ = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Multimedia :: Sound/Audio :: Players",
]
__entry_points__ = {"console_scripts": ["helody = Helody.__main__:main"]}
__extras_require__ = {
    "dev": [
        "pytest",
        "pytest-cov",
        "flake8",
        "black",
        "isort",
        "mypy",
        "sphinx",
        "sphinx-rtd-theme",
        "twine",
    ]
}
__install_requires__ = [
    "PyQt5",
    "PyQtWebEngine",
    "sqlalchemy",
    "mutagen",
    "requests",
    "youtube_dl",
    "pydub",
    "pyqt5-tools",
    "pyqt5-tools",
]
__python_requires__ = ">=3.6"
__scripts__ = []
__package_data__ = {
    "Helody": [
        "icons/*",
        "ui/*",
    ]
}
__data_files__ = []
