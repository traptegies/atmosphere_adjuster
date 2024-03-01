#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atmosphere-Adjuster.

Searches for new mp3-files in a given library and makes them more
    atmospheric. Stores info about adjustment in the mp3's metadata comment.

Created on Fri Mar 1 11:13:17 2024

@author: traptegies

IMPORTS
"""
import eyed3
import os
from pydub import AudioSegment

"""
GLOBALS
"""
lib_dir = r'/mnt/raiddrives/Movies_Series'

"""
##############################################################################
                                   MAIN
##############################################################################
"""
if __name__ == '__main__':
    # scan library for new mp3 files
    songs = []
    for path, subdirs, files in os.walk(lib_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                # add path
                file = os.path.join(path, file)
                # read mp3
                audio_file = eyed3.load(file)
                # check comments tag
                comments_accessor = None
                comments = []
                try:
                    if audio_file.tag.comments:
                        # get comments accessor
                        comments_accessor = audio_file.tag.comments
                        comments = [comment.text for comment in comments_accessor]
                        # release the file
                        audio_file = None
                except AttributeError:  # is raised when comment tag not found
                    print('No metadata found in:', file)
                    comments = []

                if 'atmosphered' not in comments:
                    # silence and fade in and out
                    song = AudioSegment.from_file(file, format='mp3')
                    # analyze audio volume
                    dbfs = song.dBFS  # average decibel relative to full scale
                    # reduce general volume by twice the average
                    song = song - 2 * abs(dbfs)
                    # fading
                    song = song.fade_in(duration=5000)
                    song = song.fade_out(duration=3000)
                    # save file
                    song.export(file, format='mp3')
                    # reload file and adjust metadata
                    audio_file = eyed3.load(file)
                    audio_file.tag.comments.set('atmosphered')
                    # save the file again
                    audio_file.tag.save(file)
                    # print success
                    print('successfully adjusted:', file)
