#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import unittest

import gpodder

from config import data
import utils

EXTENSION_NAME = 'ted_subtitles'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestTedSubtitles(unittest.TestCase):
    def setUp(self):
        self.core, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['TEDTalks'], True)]
        )
        self.episode, self.filename = podcast_list

        self.core.config.extensions.enabled = [EXTENSION_NAME]

        self.extension = gpodder.user_extensions.containers[0].module
        self.srt_filename = self.extension.get_srt_filename(self.episode)

    def tearDown(self):
        self.extension.delete_srt_file(self.episode)
        self.core.shutdown()

    def test_subtitle(self):
        self.assertIsNotNone(self.filename)
        self.assertEqual(self.episode.title, 'TED: Matt Cutts: Try something new for 30 days - Matt Cutts (2011)')
        self.assertFalse(os.path.exists(self.srt_filename))

        gpodder.user_extensions.on_episode_downloaded(self.episode)

        self.assertTrue(os.path.exists(self.srt_filename))

        gpodder.user_extensions.on_episode_delete(self.episode, self.filename)

        self.assertFalse(os.path.exists(self.srt_filename))
