#!/usr/bin/python
# -*- coding: utf-8 -*-
import filecmp
import shutil 
import unittest

from gpodder import api
from config import data
from mp3gain import hook


class TestMp3Gain(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        (self.ogg_episode, self.ogg_file, self.ogg_file_save) = self.read_episode(
                data.TEST_PODCASTS['DeimHart']['url'],
                data.TEST_PODCASTS['DeimHart']['episode'])

        (self.mp3_episode, self.mp3_file, self.mp3_file_save) = self.read_episode(
                data.TEST_PODCASTS['TinFoilHat']['url'],
                data.TEST_PODCASTS['TinFoilHat']['episode'])

    def tearDown(self):
        self.client._db.close()
        shutil.move(self.mp3_file_save, self.mp3_file)
        shutil.move(self.ogg_file_save, self.ogg_file)

    def read_episode(self, podcast_url, episode2dl):
        podcast = self.client.get_podcast(podcast_url)
        episode = podcast.get_episodes()[episode2dl]
        filename = episode._episode.local_filename(create=False, check_only=True)
        filename_save = '%s.save' % filename 
        shutil.copyfile(filename, filename_save)

        return(episode, filename, filename_save)

    def test_mp3_file(self):
        self.assertTrue(filecmp.cmp(self.mp3_file, self.mp3_file_save))

        norm_hook = hook.gPodderHooks()
        norm_hook._convert_episode(self.mp3_episode._episode)

        self.assertFalse(filecmp.cmp(self.mp3_file, self.mp3_file_save))

    def test_ogg_file(self):
        self.assertTrue(filecmp.cmp(self.ogg_file, self.ogg_file_save))

        norm_hook = hook.gPodderHooks()
        norm_hook._convert_episode(self.ogg_episode._episode)

        self.assertTrue(filecmp.cmp(self.ogg_file, self.ogg_file_save))

    def test_context_menu(self):
        norm_hook = hook.gPodderHooks()
        self.assertTrue(norm_hook._show_context_menu([self.mp3_episode._episode,]))
        self.assertFalse(norm_hook._show_context_menu([self.ogg_episode._episode,]))

