import sqlite3

con = sqlite3.connect('../DB/helody.db')

# # CREATE SETTINGS TABLE
# con.execute("""
# CREATE TABLE `settings` (
#   `name` VARCHAR(100) PRIMARY KEY NOT NULL,
#   `type` INT NOT NULL DEFAULT 0,
#   `value` TEXT NOT NULL
#   );
# """)
# con.commit()

# # CREATE PLAYLISTS TABLE
# con.execute("""
# CREATE TABLE `playlists` (
#   `id` INT(11) PRIMARY KEY,
#   `playlist` VARCHAR(100) NOT NULL,
#   `name` VARCHAR(100) NOT NULL,
#   `icon` TEXT NOT NULL,
#   `accessable` TINYINT(4) NOT NULL DEFAULT 1
#   );
# """)
# # CREATE DEFAULT PLAYLIST
# con.execute("""
# INSERT INTO `playlists` (`playlist`, `name`, `icon`, `accessable`) VALUES ('playlist', 'Playlist', 'default', '0');
# """)
# con.commit()

# # CREATE DEFAULT PLAYLIST TABLE
# con.execute("""
# CREATE TABLE `playlist` (
#   `id` INT(11) PRIMARY KEY NOT NULL,
#   `song` TEXT NOT NULL,
#   `name` TEXT NOT NULL,
#   `genre` VARCHAR(100) NOT NULL DEFAULT 'Unknown',
#   `album` VARCHAR(100) NOT NULL DEFAULT 'Unknown',
#   `artist` VARCHAR(100) NOT NULL DEFAULT 'Unknown',
#   `date` INT(20) NOT NULL,
#   `lyricsync` INT(11) NOT NULL DEFAULT 0
#   );
# """)
# con.commit()

# # ADD DEFAULT SETTINGS
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('index', 'int', '0');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('volume', 'int', '100');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('theme', 'str', 'light');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('playingList', 'str', 'playlist');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('overplayvalue', 'int', '1');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('sorttype', 'str', 'Name');")
# con.execute("INSERT INTO `settings` (`name`, `type`, `value`) VALUES ('sortside', 'str', 'Ascending');")
# con.commit()