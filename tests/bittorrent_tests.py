#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
from config import data
from bittorrent import hook


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['CRETorrent']['url']
        episode_no = data.TEST_PODCASTS['CRETorrent']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

        self.cmd = hook.DEFAULT_PARAMS['bittorrent_cmd']['value']

    def tearDown(self):
        self.client._db.close()

    def test_shellcommand(self):
        self.assertIsNotNone(self.filename)
        self.assertIsNotNone(self.episode._episode)

        bt_hook = hook.gPodderHooks(test=True)
        result = bt_hook.on_episode_downloaded(self.episode._episode)
        self.assertIsNotNone(result)
        self.assertTrue(result, tuple)

        stdout, stderr = result
        test_cmd = self.cmd % self.filename
        self.assertEqual(stdout.rstrip(), test_cmd)
