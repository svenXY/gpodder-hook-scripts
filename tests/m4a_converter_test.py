#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from gpodder import api
from config import data
import m4a_converter


class TestM4AConverter(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['LogbuchNetzpolitik']['url']
        episode_no = data.TEST_PODCASTS['LogbuchNetzpolitik']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)
        self.converted_file = os.path.splitext(self.filename)[0] + '.mp3'

    def tearDown(self):
        self.client._db.close()
        
        if os.path.exists(self.converted_file):
            os.remove(self.converted_file)

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)

        m4a_hook = m4a_converter.gPodderHooks(test=True)
        m4a_hook.on_episode_downloaded(self.episode._episode)

        self.assertTrue(os.path.exists(self.converted_file))
        self.assertTrue(os.path.getsize(self.converted_file)>0)
