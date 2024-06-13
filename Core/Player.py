from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist

from Core.Window import Window
from lib import db
from Models import Playlist, PlaylistSong, Song


class Player(QMediaPlayer):
    parent: Window
    playlist: QMediaPlaylist
    currentPlaylist: Playlist
    songs: list[Song] | None

    def __init__(self, parent: Window):
        self.parent = parent
        super(Player, self).__init__(self.parent)

        self.playlist = QMediaPlaylist(self.parent)

        self.loadPlayList()

    def loadPlayList(self):  # noqa
        self.songs = None

        playlist = db.session.query(Playlist).filter_by(playing="yes").first()
        if playlist is None:
            playlist = Playlist(name="Playlist", playing="yes")
            db.session.add(playlist)
            db.session.commit()
        self.currentPlaylist = playlist

        self.songs = db.session.query(Song).join(
            PlaylistSong, PlaylistSong.song_id == Song.id
            and PlaylistSong.playlist_id == self.currentPlaylist.id).order_by(
                Song.id.desc()).all()
        if self.songs is not None:
            for song in self.songs:
                self.playlist.addMedia(
                    QMediaContent(QUrl.fromLocalFile(song.path)))
            self.setPlaylist(self.playlist)

            current_song: Song = next(
                (song for song in self.songs if song.playing == "yes"), None)
            if current_song is not None:
                self.playlist.setCurrentIndex(self.songs.index(current_song))
            else:
                self.playlist.setCurrentIndex(0)

    def changePlaylist(self, playlist: Playlist):  # noqa
        self.currentPlaylist.playing = "no"
        playlist.playing = "yes"
        db.session.commit()
        self.loadPlayList()
