#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
from enqueue_in_vlc import extension


class TestEnqueueInVLC(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.episode = get_episode(self.client, data.TEST_PODCASTS['TinFoilHat'], False)
        self.metadata = get_metadata(extension)

    def tearDown(self):
        self.client._db.close()

    def test_menu_entry(self):
        vlc_extension = extension.gPodderExtension(metadata=self.metadata)
        menu_entry = vlc_extension.on_episodes_context_menu([self.episode._episode]) 
        self.assertTrue(isinstance(menu_entry, list))
        self.assertEqual(len(menu_entry), 1)

        self.assertTrue(isinstance(menu_entry[0], tuple))
        self.assertEqual(len(menu_entry[0]), 2)

        self.assertEqual(menu_entry[0][0], 'Enqueue in VLC')

    def test_enqueue_cmd(self):
        cmd = extension.CMD + " --no-audio"
        vlc_extension = extension.gPodderExtension(cmd=cmd)
        vlc_extension._enqueue_episodes([self.episode._episode]) 
