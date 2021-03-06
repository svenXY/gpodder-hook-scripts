#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import unittest

import gpodder

from config import data
import utils

EXTENSION_NAME = 'enqueue_in_vlc'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestEnqueueInVLC(unittest.TestCase):
    def setUp(self):
        self.core, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['TinFoilHat'], True)]
        )
        self.episode, self.filename = podcast_list

        self.core.config.extensions.enabled = [EXTENSION_NAME]

        # set ui to gtk because the extension only works with gtk
        gpodder.ui.gtk = True
        gpodder.user_extensions.containers[0].load_extension()

    def tearDown(self):
        self.core.shutdown()

    def test_menu_entry(self):
        menu_entry = gpodder.user_extensions.on_episodes_context_menu([self.episode,])
        self.assertTrue(isinstance(menu_entry, list))
        self.assertEqual(len(menu_entry), 1)

        self.assertTrue(isinstance(menu_entry[0], tuple))
        self.assertEqual(len(menu_entry[0]), 2)

        self.assertEqual(menu_entry[0][0], 'Enqueue in VLC')
