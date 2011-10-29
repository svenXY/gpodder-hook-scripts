#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
from config import data
from zpravy.hook import get_pubdate


class TestZpravy(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.podcast = self.client.get_podcast(data.TEST_PODCASTS['Zpravy']['url'])
        self.episode = self.podcast.get_episodes()[-1]

    def tearDown(self):
        self.client._db.close()

    def test_zpravy_pubdate(self):
        try:
            pubDate = self.episode._episode.pubDate
        except:
            # since version 3 the published date has a new/other name
            pubDate = self.episode._episode.published
        guid = self.episode._episode.guid

        self.assertEqual(0, pubDate)
        self.assertEqual(guid, self.episode.url)
        self.assertNotEqual(pubDate, get_pubdate(self.episode))

