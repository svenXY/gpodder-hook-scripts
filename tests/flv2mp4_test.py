#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import unittest

from gpodder import api
from config import data
from flv2mp4 import hook


class TestFlv2Mp4(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['drovics']['url']
        episode_no = data.TEST_PODCASTS['drovics']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

    def tearDown(self):
        self.client._db.close()

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)
        self.assertEqual(self.episode._episode.title, 'Corporations Are People, Too')

        flv_hook = hook.gPodderHooks()
        flv_hook.on_episode_downloaded(self.episode._episode)
