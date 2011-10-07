#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
import test_config as config
from zpravy_hook import get_pubdate


class TestZpravy(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.podcast = self.client.get_podcast(config.ZPRAVY)
        self.episode = self.podcast.get_episodes()[-1]

    def tearDown(self):
        self.client._db.close()

    def test_zpravy_pubdate(self):
        pubDate = self.episode._episode.pubDate
        guid = self.episode._episode.guid

        self.assertEqual(0, pubDate)
        self.assertEqual(guid, self.episode.url)
        self.assertNotEqual(pubDate, get_pubdate(self.episode))

