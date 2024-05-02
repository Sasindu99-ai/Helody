from Core import Database
from lib.res import ColorTheme, ImageSet

__all__ = ["Color", "db", "Images"]

db: Database = Database("DB/helody.sqlite")
Color: ColorTheme = ColorTheme(ColorTheme.LIGHT)
Images: ImageSet = ImageSet(theme=Color.get_theme())
