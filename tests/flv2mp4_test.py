#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
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
        self.converted_file = os.path.splitext(self.filename)[0] + '.mp4'

    def tearDown(self):
        self.client._db.close()
        
        if os.path.exists(self.converted_file):
            os.remove(self.converted_file)

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)

        flv_hook = hook.gPodderHooks(test=True)
        flv_hook.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_file))
        self.assertTrue(os.path.getsize(self.converted_file)>0)
