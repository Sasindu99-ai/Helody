from sqlalchemy import Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from lib import db


class Song(db.Model):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    album = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    cover = Column(Text, nullable=True)
    path = Column(Text, nullable=False)
    playing = Column(Enum("yes", "no"), default="no")
    modifiedDate = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, default=now())
    updatedAt = Column(DateTime, default=now(), onupdate=now())

    playlists = relationship("Playlist",
                             secondary="playlist_songs",
                             back_populates="songs")

    def __repr__(self):
        return f"<Song {self.title}>"
