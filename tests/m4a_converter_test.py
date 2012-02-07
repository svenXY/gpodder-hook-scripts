#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
import m4a_converter as extension


class TestM4AConversion(unittest.TestCase):
    def setUp(self):
        self.config = extension.DEFAULT_CONFIG
        self.client = api.PodcastClient()

        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['LogbuchNetzpolitik'], True)
        self.converted_mp3 = os.path.splitext(self.filename)[0] + '.mp3'
        self.converted_ogg = os.path.splitext(self.filename)[0] + '.ogg'

        self.episode1 = get_episode(self.client,
            data.TEST_PODCASTS['TinFoilHat'], False)

        self.metadata = get_metadata(extension)

    def tearDown(self):
        self.client._db.close()
        
        if os.path.exists(self.converted_mp3):
            os.remove(self.converted_mp3)
        if os.path.exists(self.converted_ogg):
            os.remove(self.converted_ogg)

    def test_m4a2mp3(self):
        self.assertIsNotNone(self.filename)

        self.assertEqual('lnp003-twitter-facebook-american-censorship-day.m4a',
            os.path.split(self.filename)[1])

        self.config['extensions']['m4a_converter']['file_format'] = [True, False]
        m4a_extension = extension.gPodderExtension(metadata=self.metadata,
            config=self.config, test=True)
        m4a_extension.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_mp3))
        self.assertTrue(os.path.getsize(self.converted_mp3)>0)

    def test_m4a2ogg(self):
        self.assertIsNotNone(self.filename)

        self.assertEqual('lnp003-twitter-facebook-american-censorship-day.m4a',
            os.path.split(self.filename)[1])

        self.config['extensions']['m4a_converter']['file_format'] = [False, True]
        m4a_extension = extension.gPodderExtension(metadata=self.metadata,
            config=self.config, test=True)
        m4a_extension.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_ogg))
        self.assertTrue(os.path.getsize(self.converted_ogg)>0)

    def test_context_menu(self):
        self.assertIn(self.episode._episode.mime_type, extension.MIME_TYPES)
        self.assertNotIn(self.episode1._episode.mime_type, extension.MIME_TYPES)

        m4a_extension = extension.gPodderExtension(metadata=self.metadata, test=True)
        self.assertTrue(m4a_extension._show_context_menu([self.episode._episode,]))
        self.assertFalse(m4a_extension._show_context_menu([self.episode1._episode,]))
