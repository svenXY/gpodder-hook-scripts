#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gpodder import api
from config import data
from tfh_shownotes import extension

IMAGEFILE='/tmp/FRONT_COVER.jpeg'
DESC=u'Show Notes Get the commands at http://cafeninja.blogspot.com<img height="1" src="http://feeds.feedburner.com/~r/TinFoilHat/~4/zzwDl_AW194" width="1" />'


class TestTfhShownotes(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.podcast = self.client.get_podcast(data.TEST_PODCASTS['TinFoilHat']['url'])
        self.episode = self.podcast.get_episodes()[data.TEST_PODCASTS['TinFoilHat']['episode']]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)

        self.podcast1 = self.client.get_podcast(data.TEST_PODCASTS['DeimHart']['url'])
        self.episode1 = self.podcast1.get_episodes()[data.TEST_PODCASTS['DeimHart']['episode']]

    def tearDown(self):
        self.client._db.close()

    def test_episode_name(self):
        self.assertEqual('Pilot show', self.episode.title)

    def test_episode_download_status(self):
        self.assertTrue(self.episode.is_downloaded)

    def test_extract_image(self):
        imagefile = extension.extract_image(self.filename)
        self.assertTrue(imagefile)
        self.assertEqual(IMAGEFILE, imagefile)

    def test_extract_shownotes(self):
        shownotes = extension.extract_shownotes(IMAGEFILE, remove_image=False)
        self.assertIsNotNone(shownotes)

    def test_search_shownotes_in_desc(self):
        shownotes = extension.extract_shownotes(IMAGEFILE, remove_image=False)
        desc = self.episode._episode.description

        self.assertEqual(DESC, desc)
        self.assertEqual(-1, desc.find(shownotes))

    def test_context_menu(self):
        self.assertEqual(self.episode._episode.channel.title, extension.TFH_TITLE)
        self.assertNotEqual(self.episode1._episode.channel.title, extension.TFH_TITLE)

        tfh_extension = extension.gPodderExtensions()
        self.assertTrue(tfh_extension._show_context_menu([self.episode._episode,]))
        self.assertFalse(tfh_extension._show_context_menu([self.episode1._episode,]))
