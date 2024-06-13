from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from lib import db


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    playing = Column(Enum("yes", "no"), default="no")
    createdAt = Column(DateTime, default=now())
    updatedAt = Column(DateTime, default=now(), onupdate=now())

    songs = relationship("Song",
                         secondary="playlist_songs",
                         back_populates="playlists")

    def __repr__(self):
        return f"<Playlist {self.name}>"
