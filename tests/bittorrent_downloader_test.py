#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
from bittorrent_downloader import extension


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['CRETorrent'], True)
        self.cmd = extension.DEFAULT_CONFIG['extensions']['bittorrent_downloader']['cmd']
        self.metadata = get_metadata(extension)

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
