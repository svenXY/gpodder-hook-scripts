#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from gpodder import api
from gpodder import extensions
from gpodder import util
from config import data
from utils import get_episode

EXTENSION_NAME = 'bittorrent_downloader'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestBittorrent(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['CRETorrent'], True)

        self.em = extensions.ExtensionManager(self.client.core, EXTENSION_FILE)

        self.save_enabled = self.em.core.config.extensions.enabled
        self.save_cmd = self.em.core.config.extensions.bittorrent_downloader.cmd

        self.em.core.config.extensions.enabled = [EXTENSION_NAME]
        self.em.core.config.extensions.bittorrent_downloader.cmd = 'echo "%s"' % self.save_cmd

    def tearDown(self):
        self.em.core.config.extensions.enabled = self.save_enabled
        self.em.core.config.extensions.bittorrent_downloader.cmd = self.save_cmd
        self.em.shutdown()
        self.client._db.close()

    def test_shellcommand(self):
        self.assertIsNotNone(self.filename)
        self.assertIsNotNone(self.episode._episode)

        # TODO: not sure if the return value is a good idea
        result = self.em.on_episode_downloaded(self.episode._episode)
        self.assertIsNotNone(result)
        self.assertTrue(result, tuple)

        stdout, stderr = result
        test_cmd = self.save_cmd % self.filename
        self.assertEqual(stdout.rstrip(), test_cmd)
