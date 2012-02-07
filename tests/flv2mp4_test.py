#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
import flv2mp4 as extension


class TestFlv2Mp4(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['drovics'], True)
        self.converted_file = os.path.splitext(self.filename)[0] + '.mp4'

        self.episode1 = get_episode(self.client,
            data.TEST_PODCASTS['TinFoilHat'], False)

        self.metadata = get_metadata(extension)

    def tearDown(self):
        self.client._db.close()
        
        if os.path.exists(self.converted_file):
            os.remove(self.converted_file)

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)

        flv_extension = extension.gPodderExtension(metadata=self.metadata, test=True)
        flv_extension.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_file))
        self.assertTrue(os.path.getsize(self.converted_file)>0)

    def test_context_menu(self):
        self.assertEqual(self.episode._episode.mime_type, 'video/x-flv')
        self.assertNotEqual(self.episode1._episode.mime_type, 'video/x-flv')

        flv_extension = extension.gPodderExtension(metadata=self.metadata, test=True)
        self.assertTrue(flv_extension._show_context_menu([self.episode._episode,]))
        self.assertFalse(flv_extension._show_context_menu([self.episode1._episode,]))
