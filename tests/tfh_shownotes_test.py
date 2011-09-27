#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
import tfh_shownotes_hook

TINFOILHAT='http://feeds.feedburner.com/TinFoilHat'
IMAGEFILE='/tmp/FRONT_COVER.jpeg'


class TestTfhShownotes(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.podcast = self.client.get_podcast(TINFOILHAT)
        self.episode = self.podcast.get_episodes()[-1]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

    def tearDown(self):
        self.client._db.close()

    def test_episode_name(self):
        self.assertEqual('Pilot show', self.episode.title)

    def test_episode_download_status(self):
        self.assertTrue(self.episode.is_downloaded)

    def test_extract_image(self):
        imagefile = tfh_shownotes_hook.extract_image(self.filename)
        self.assertTrue(imagefile)
        self.assertEqual(IMAGEFILE, imagefile)

    def test_extract_shownotes(self):
        shownotes = tfh_shownotes_hook.extract_shownotes(IMAGEFILE)
        self.assertTrue(shownotes)

