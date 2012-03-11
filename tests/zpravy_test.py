#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

import gpodder

from config import data
import utils

EXTENSION_NAME = 'zpravy'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestZpravy(unittest.TestCase):
    def setUp(self):
        self.core, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['Zpravy'], False)]
        )
        self.episode, self.filename = podcast_list

        self.core.config.extensions.enabled = [EXTENSION_NAME]

    def tearDown(self):
        self.core.shutdown()

    def test_zpravy_pubdate(self):
        try:
            pubDate = self.episode.pubDate
        except:
            # since version 3 the published date has a new/other name
            pubDate = self.episode.published
        guid = self.episode.guid
        zpravy_extension = gpodder.user_extensions.containers[0].module

        self.assertEqual(0, pubDate)
        self.assertEqual(guid, self.episode.url)
        self.assertNotEqual(pubDate, zpravy_extension._get_pubdate(self.episode))

