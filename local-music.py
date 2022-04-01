#!/usr/bin/env python

#pip install ffmpeg-python
#https://www.thepythoncode.com/article/extract-media-metadata-in-python
#ID3 Properties:
#   https://eyed3.readthedocs.io/en/latest/
#   https://eyed3.readthedocs.io/en/latest/eyed3.id3.html#module-eyed3.id3.tag
# Find mp3 files
import eyed3
import pathlib
# 
class MediaFile():
    def __init__(self, pathname) -> None:
        self.attributes = {}
        if pathlib.Path(pathname).suffix == ".mp3":
            audiofile = eyed3.load(pathname)
            self.attributes["filename"] = pathname
            self.attributes["title"] = audiofile.tag.title
            self.attributes["composer"] = audiofile.tag.composer
            self.attributes["artist"] = audiofile.tag.artist
            self.attributes["album_artist"] = audiofile.tag.album_artist
            self.attributes["album"] = audiofile.tag.album
            self.attributes["publisher"] = audiofile.tag.publisher
            date = audiofile.tag.best_release_date
            self.attributes["release_year"] = date.year
            self.attributes["duration_seconds"] = audiofile.info.time_secs

f = MediaFile("E:\\music\\80s\\Joe Jackson\\Greatest Hits\\01 - Greatest Hits - Is She Really Going Out With Him- - Joe Jackson.mp3")
print(f.attributes)