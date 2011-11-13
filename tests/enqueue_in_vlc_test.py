#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import unittest

from gpodder import api
from config import data
from enqueue_in_vlc import extension


class TestEnqueueInVLC(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['TinFoilHat']['url']
        self.podcast = self.client.get_podcast(url)
        self.podcast_title = self.podcast.title

        self.episode = self.podcast.get_episodes()[-1]

        with open(os.path.join(os.path.dirname(extension.__file__), 'metadata.json'), 'r') as f:
            self.metadata = json.load(f)

    def tearDown(self):
        self.client._db.close()

    def test_menu_entry(self):
        vlc_extension = extension.gPodderExtensions(metadata=self.metadata)
        menu_entry = vlc_extension.on_episodes_context_menu([self.episode._episode]) 
        self.assertTrue(isinstance(menu_entry, list))
        self.assertEqual(len(menu_entry), 1)

        self.assertTrue(isinstance(menu_entry[0], tuple))
        self.assertEqual(len(menu_entry[0]), 2)

        self.assertEqual(menu_entry[0][0], 'Enqueue in VLC')

    def test_enqueue_cmd(self):
        cmd = extension.CMD + " --no-audio"
        vlc_extension = extension.gPodderExtensions(cmd=cmd)
        vlc_extension._enqueue_episodes([self.episode._episode]) 
