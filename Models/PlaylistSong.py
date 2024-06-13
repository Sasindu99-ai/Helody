from sqlalchemy import Column, ForeignKey, Integer

from lib import db


class PlaylistSong(db.Model):
    __tablename__ = "playlist_songs"

    playlist_id = Column(Integer,
                         ForeignKey("playlists.id"),
                         primary_key=True,
                         nullable=False)
    song_id = Column(Integer,
                     ForeignKey("songs.id"),
                     primary_key=True,
                     nullable=False)

    def __repr__(self):
        return f"<PlaylistSong {self.playlist_id}: {self.song_id}>"
