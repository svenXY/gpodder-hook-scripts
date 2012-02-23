#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from config import data
import utils

EXTENSION_NAME = 'bittorrent_downloader'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')
TEST_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.out')


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client, self.em, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['CRETorrent'], True)]
        )
        self.episode, self.filename = podcast_list

        self.save_enabled = self.em.core.config.extensions.enabled
        self.save_cmd = self.em.core.config.extensions.bittorrent_downloader.cmd

        test_cmd = 'cp "%s" ' + TEST_OUTPUT
        self.em.core.config.extensions.enabled = [EXTENSION_NAME]
        self.em.core.config.extensions.bittorrent_downloader.cmd = test_cmd

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT):
            os.remove(TEST_OUTPUT)

        self.em.core.config.extensions.enabled = self.save_enabled
        self.em.core.config.extensions.bittorrent_downloader.cmd = self.save_cmd
        self.em.shutdown()
        self.client._db.close()

    def test_shellcommand(self):
        self.assertIsNotNone(self.filename)
        self.assertIsNotNone(self.episode._episode)

        self.em.on_episode_downloaded(self.episode._episode)
        self.assertTrue(os.path.exists(TEST_OUTPUT))
