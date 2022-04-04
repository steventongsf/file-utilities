#!/usr/bin/env python

from unittest import TestCase
from local_music import MediaFile, FileFinder, mp3_handler

# python -m pytest -s tests/
class TestLocalMusic():
    media_file = "E:\\music\\80s\\Joe Jackson\\Greatest Hits\\01 - Greatest Hits - Is She Really Going Out With Him- - Joe Jackson.mp3"

    def test_MediaFile(self):
        f = MediaFile(self.media_file)
        assert(f.attributes["title"] == "Is She Really Going Out With H")
        #print(f.attributes)

    def test_FileFinder(self):
        ff = FileFinder()
        ff.get_files("E:\\music\\80s", mp3_handler)