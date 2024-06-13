from lib.res import ColorTheme, Database, ImageSet, Locale, Localized

__all__ = ["Color", "db", "Images", "Localized", "Locale"]

db: Database = Database("DB/helody.sqlite")
Color: ColorTheme = ColorTheme(ColorTheme.LIGHT)
Images: ImageSet = ImageSet(theme=Color.get_theme())

from Models import Playlist, PlaylistSong, Setting, Song

db.create_all()
