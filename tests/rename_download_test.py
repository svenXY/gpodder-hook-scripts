#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
from rename_download.extension import rename_file


class TestRenameDownloads(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['TinFoilHat'], True)
        self.title = self.episode.title

    def tearDown(self):
        self.client._db.close()

    def test_rename_file(self):
        filename_test = os.path.join(os.environ['GPODDER_DOWNLOAD_DIR'],
            'Tin Foil Hat', 'Pilot show.mp3')
        filename_new = rename_file(self.filename, self.title) 

        self.assertEqual(filename_test, filename_new)
        self.assertNotEqual(self.filename, filename_new)

