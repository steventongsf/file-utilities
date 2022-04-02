#!/usr/bin/env python

#pip install ffmpeg-python
#https://www.thepythoncode.com/article/extract-media-metadata-in-python
#ID3 Properties:
#   https://eyed3.readthedocs.io/en/latest/
#   https://eyed3.readthedocs.io/en/latest/eyed3.id3.html#module-eyed3.id3.tag
# Find mp3 files
import os,sys
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
            date = audiofile.tag.getBestDate()
            self.attributes["release_year"] = date.year
            self.attributes["duration_seconds"] = audiofile.info.time_secs
            #self.attributes["genre"] = audiofile.Genre
        # TODO Add support for other media types like mp4, wmv, etc.
class FileFinder():
    def __init__(self) -> None:
        self.mp3_records = []

    def get_files(self,path, handler):
        all_records = []
        dirnames = []
        filenames = []
        for root,d_names,f_names in os.walk(path):
            for d in d_names:
                dirnames.append(os.path.join(root, d))
        for d in dirnames:    
            #print(d)
            for e in os.listdir(d):
                filenames.append(f"{d}/{e}")
        #print(filenames)
        for f in filenames:
            row = handler(f)
            if row is not None:
                self.mp3_records.append(row)
class MediaLibrary():
    pass

def mp3_handler(file):
    global mp3_count
    if pathlib.Path(file).suffix == ".mp3":
        mf = MediaFile(file)
        return mf.attributes
    else:
        return None


if __name__ == "__main__":
    try:
        sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} <path to search>")
        sys.exit(1)
    ff = FileFinder()
    ff.get_files(sys.argv[1], mp3_handler)
    print(str(len(ff.mp3_records))+" mp3 files found.")
    sys.exit(0)


