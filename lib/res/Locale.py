import enum
import os
import json

__all__ = ["Locale", "Localized"]


class Locale(enum.Enum):
    enUS = "enUS"
    siLK = "siLK"


class LocalizedStrings:
    locale: Locale = Locale.enUS
    json: dict = {}

    def __init__(self):
        with open(os.getcwd() + f"/lib/res/lang/{self.locale.name}.json", "r") as file:
            self.json = json.load(file)

    def get(self, key: str) -> str:
        if key in self.json.keys():
            return self.json[key]
        return key


localized = LocalizedStrings()


class Localized(str):
    key: str

    def __new__(cls, key: str):
        cls.key = key
        return super(Localized, cls).__new__(cls, localized.get(key))

    def __repr__(self):
        return localized.get(self.key)

    def __str__(self):
        return localized.get(self.key)
