#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
import test_config as config
from rockbox_mp4_convert import hook


class TestRockboxMP4Convert(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = config.TEST_PODCASTS['60sec']['url']
        episode_no = config.TEST_PODCASTS['60sec']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

    def tearDown(self):
        self.client._db.close()

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)
        self.assertEqual(self.episode._episode.title, '60 Seconds Episode 9: Vader')
        #hook.convertMP4(self.filename, self.filename+'.conv', hook.DEFAULT_PARAMS)
