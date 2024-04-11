from sqlalchemy import Integer, String, Column

from Helody import db


class Playlists(db.Model):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Playlist {self.name}>"
