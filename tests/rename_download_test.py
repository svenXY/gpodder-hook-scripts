#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from gpodder import api
import test_config as config
from rename_download.hook import rename_file


class TestRenameDownloads(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        self.podcast = self.client.get_podcast(config.TEST_PODCASTS['TinFoilHat']['url'])
        self.podcast_title = self.podcast.title

        self.episode = self.podcast.get_episodes()[-1]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)
        self.title = self.episode.title

    def tearDown(self):
        self.client._db.close()

    def test_rename_file(self):
        filename_test = os.path.join(os.environ['GPODDER_DOWNLOAD_DIR'],
            self.podcast_title, 'Pilot show.mp3')
        filename_new = rename_file(self.filename, self.title) 

        self.assertEqual(filename_test, filename_new)
        self.assertNotEqual(self.filename, filename_new)

