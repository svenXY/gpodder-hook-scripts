#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from gpodder import api
from config import data
from enqueue_in_vlc import hook


class TestEnqueueInVLC(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['TinFoilHat']['url']
        self.podcast = self.client.get_podcast(url)
        self.podcast_title = self.podcast.title

        self.episode = self.podcast.get_episodes()[-1]

    def tearDown(self):
        self.client._db.close()

    def test_menu_entry(self):
        vlc_hook = hook.gPodderHooks()
        menu_entry = vlc_hook.on_episodes_context_menu([self.episode._episode]) 
        self.assertTrue(isinstance(menu_entry, list))
        self.assertEqual(len(menu_entry), 1)

        self.assertTrue(isinstance(menu_entry[0], tuple))
        self.assertEqual(len(menu_entry[0]), 2)

        self.assertEqual(menu_entry[0][0], 'Enqueue in VLC')

    def test_enqueue_cmd(self):
        cmd = hook.CMD + " --no-audio"
        vlc_hook = hook.gPodderHooks(cmd)
        vlc_hook._enqueue_episodes([self.episode._episode]) 
