#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import unittest

from gpodder import api
from config import data
from bittorrent_downloader import extension


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['CRETorrent']['url']
        episode_no = data.TEST_PODCASTS['CRETorrent']['episode']
        self.podcast = self.client.get_podcast(url)

        self.episode = self.podcast.get_episodes()[episode_no]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

        self.cmd = extension.DEFAULT_CONFIG['extensions']['bittorrent_downloader']['cmd']

        with open(os.path.join(os.path.dirname(extension.__file__), 'metadata.json'), 'r') as f:
           self.metadata = json.load(f)

    def tearDown(self):
        self.client._db.close()

    def test_shellcommand(self):
        self.assertIsNotNone(self.filename)
        self.assertIsNotNone(self.episode._episode)

        bt_extension = extension.gPodderExtensions(metadata=self.metadata, test=True)
        result = bt_extension.on_episode_downloaded(self.episode._episode)
        self.assertIsNotNone(result)
        self.assertTrue(result, tuple)

        stdout, stderr = result
        test_cmd = self.cmd % self.filename
        self.assertEqual(stdout.rstrip(), test_cmd)
