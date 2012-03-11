#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

import gpodder

from config import data
import utils

EXTENSION_NAME = 'tfh_shownotes'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')
TFH_TITLE = 'Tin Foil Hat'
IMAGEFILE='/tmp/FRONT_COVER.jpeg'
DESC=u'Show Notes Get the commands at http://cafeninja.blogspot.com<img height="1" src="http://feeds.feedburner.com/~r/TinFoilHat/~4/zzwDl_AW194" width="1" />'


class TestTfhShownotes(unittest.TestCase):
    def setUp(self):
        self.core, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['TinFoilHat'], True),
             (data.TEST_PODCASTS['DeimHart'], True)
            ]
        )
        self.episode, self.filename, self.episode1, self.filename1 = podcast_list

        self.core.config.extensions.enabled = [EXTENSION_NAME]

        self.tfh_extension = gpodder.user_extensions.containers[0].module

    def tearDown(self):
        self.core.shutdown()

    def test_episode_name(self):
        self.assertEqual('Pilot show', self.episode.title)

    def test_extract_image(self):
        imagefile = self.tfh_extension.extract_image(self.filename)
        self.assertTrue(imagefile)
        self.assertEqual(IMAGEFILE, imagefile)

    def test_extract_shownotes(self):
        shownotes = self.tfh_extension.extract_shownotes(IMAGEFILE, remove_image=False)
        self.assertIsNotNone(shownotes)

    def test_search_shownotes_in_desc(self):
        shownotes = self.tfh_extension.extract_shownotes(IMAGEFILE, remove_image=False)
        desc = self.episode.description

        self.assertEqual(DESC, desc)
        self.assertEqual(-1, desc.find(shownotes))

    def test_context_menu(self):
        self.assertEqual(self.episode.channel.title, TFH_TITLE)
        self.assertNotEqual(self.episode1.channel.title, TFH_TITLE)

        self.assertTrue(gpodder.user_extensions.on_episodes_context_menu([self.episode,]))
        self.assertFalse(gpodder.user_extensions.on_episodes_context_menu([self.episode1,]))
