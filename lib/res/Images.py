import os

__all__ = ["Images"]


class ImagesMeta(type):
    __BASE__ = "lib/res/images/"
    __THEME__ = "0/"

    def __new__(cls, name, bases, dct):
        base = dct.get("__BASE__", "")
        for attr_name, attr_value in dct.items():
            if not attr_name.startswith("__"):
                if os.path.exists(os.getcwd() + "/" + base + attr_value):
                    dct[attr_name] = base + attr_value
                else:
                    dct[attr_name] = base + cls.__THEME__ + attr_value
        return super().__new__(cls, name, bases, dct)


class Images(metaclass=ImagesMeta):
    __BASE__ = "lib/res/images/"
    __THEME__ = "0/"

    def __init__(self, theme: int = ""):
        if theme is not None and theme != "":
            self.__THEME__ = str(theme) + "/"

    icon = "helody.png"
