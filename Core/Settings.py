from enum import Enum

from lib import db
from Models import Setting


class SortType(Enum):
    name = "Name"
    genre = "Genre"
    album = "Album"
    artist = "Artist"
    dateModified = "Date Modified"
    timeAdded = "Time Added"


class Order(Enum):
    ascending = "Ascending"
    descending = "Descending"


class Settings:
    volume: int = 100
    volumeMuted: bool = False
    sortBy: SortType = SortType.name
    order: Order = Order.ascending

    __refs = ["volume", "volumeMuted", "sortBy", "order"]

    def __init__(self):
        for attribute in self.__refs:
            self.__setattr__(attribute, self.getValue(attribute))

    def getValue(self, attribute: str):  # noqa
        setting: Setting | None = db.session.query(Setting).filter_by(
            keyword=attribute).first()
        if setting is not None:
            return eval(setting.cast + "(" + setting.value + ")")
        return self.__getattribute__(attribute)

    def save(self):
        for attribute in self.__refs:
            # update setting, create if not exists
            value = self.__getattribute__(attribute)
            cast = type(value).__name__
            setting: Setting | None = db.session.query(Setting).filter_by(
                keyword=attribute).first()
            if setting is None:
                setting: Setting = Setting(keyword=attribute,
                                           value=value,
                                           cast=cast)
                db.session.add(setting)
            else:
                setting.value = value
                setting.cast = cast
        db.session.commit()
