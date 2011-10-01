#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from gpodder import api
from rename_downloads import rename_file

TINFOILHAT='http://feeds.feedburner.com/TinFoilHat'


class TestRenameDownloads(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        self.podcast = self.client.get_podcast(TINFOILHAT)
        self.podcast_title = self.podcast.title

        self.episode = self.podcast.get_episodes()[-1]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)
        self.title = self.episode.title

    def tearDown(self):
        self.client._db.close()

    def test_rename_file(self):
        self.assertEqual(os.path.join(os.environ['GPODDER_DOWNLOAD_DIR'],
                                        self.podcast_title, 'Pilot show.mp3'),
            rename_file(self.filename, self.title))

