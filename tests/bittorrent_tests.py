#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
import test_config as config
from bittorrent import hook


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = config.TEST_PODCASTS['CRETorrent']['url']
        episode_no = config.TEST_PODCASTS['CRETorrent']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

        self.param = hook.DEFAULT_PARAM
        self.origin_cmd = self.param['bittorrent_cmd']['value']
        self.param['bittorrent_cmd']['value'] = 'echo "%s"' % self.origin_cmd

    def tearDown(self):
        self.client._db.close()

    def test_shellcommand(self):
        self.assertIsNotNone(self.filename)

        bt_hook = hook.gPodderHooks(self.param, stdout=True)
        stdout, stderr = bt_hook.on_episode_downloaded(self.episode._episode)

        cmd = self.origin_cmd % self.filename
        self.assertEqual(stdout.rstrip(), cmd)
