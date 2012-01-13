#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from gpodder import api
from config import data
from m4a_converter import extension


class TestM4AConversion(unittest.TestCase):
    def setUp(self):
        self.config = extension.DEFAULT_CONFIG
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['LogbuchNetzpolitik']['url']
        episode_no = data.TEST_PODCASTS['LogbuchNetzpolitik']['episode']
        self.podcast = self.client.get_podcast(url)
        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)
        self.converted_mp3 = os.path.splitext(self.filename)[0] + '.mp3'
        self.converted_ogg = os.path.splitext(self.filename)[0] + '.ogg'

        url1 = data.TEST_PODCASTS['TinFoilHat']['url']
        episode_no1 = data.TEST_PODCASTS['TinFoilHat']['episode']
        self.podcast1 = self.client.get_podcast(url1)
        self.episode1 = self.podcast1.get_episodes()[episode_no1]

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

        self.config['m4a_converter']['params']['file_format']['value'] = [True, False]
        m4a_extension = extension.gPodderExtensions(config=self.config, test=True)
        m4a_extension.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_mp3))
        self.assertTrue(os.path.getsize(self.converted_mp3)>0)

    def test_m4a2ogg(self):
        self.assertIsNotNone(self.filename)

        self.assertEqual('lnp003-twitter-facebook-american-censorship-day.m4a',
            os.path.split(self.filename)[1])

        self.config['m4a_converter']['params']['file_format']['value'] = [False, True]
        m4a_extension = extension.gPodderExtensions(config=self.config, test=True)
        m4a_extension.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_ogg))
        self.assertTrue(os.path.getsize(self.converted_ogg)>0)

    def test_context_menu(self):
        self.assertIn(self.episode._episode.mime_type, extension.MIME_TYPES)
        self.assertNotIn(self.episode1._episode.mime_type, extension.MIME_TYPES)

        m4a_extension = extension.gPodderExtensions(test=True)
        self.assertTrue(m4a_extension._show_context_menu([self.episode._episode,]))
        self.assertFalse(m4a_extension._show_context_menu([self.episode1._episode,]))
