from sqlalchemy import Column, Enum, String

from lib import db


class Setting(db.Model):
    __tablename__ = "settings"

    keyword = Column(String(255), primary_key=True, nullable=False)
    value = Column(String(255), nullable=False)
    cast = Column(Enum("int", "str", "float", "bool", "SortType", "Order"),
                  default="str",
                  nullable=False)
