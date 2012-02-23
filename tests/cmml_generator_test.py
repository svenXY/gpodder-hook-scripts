#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import unittest
import urllib2

from config import data
import utils


EXTENSION_NAME = 'cmml_generator'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestCmmlLinuxOutlaws(unittest.TestCase):
    def setUp(self):
        self.client, self.em, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['LinuxOutlaws'], True),
             (data.TEST_PODCASTS['TinFoilHat'], True)
            ]
        )
        self.episode, self.filename, self.episode2, self.filename2 = podcast_list

        self.save_enabled = self.em.core.config.extensions.enabled
        self.em.core.config.extensions.enabled = [EXTENSION_NAME]

    def tearDown(self):
        self.em.on_episode_delete(self.episode, self.filename)
        self.em.core.config.extensions.enabled = self.save_enabled
        self.em.shutdown()
        self.client._db.close()

    def test_create_cmml(self):
        self.em.on_episode_downloaded(self.episode._episode)
        cmml_file = self.em.containers[0].module.get_cmml_filename(self.filename)
        self.assertTrue(os.path.exists(cmml_file))
        self.assertTrue(os.path.getsize(cmml_file)>0)

    def test_context_menu(self):
        self.assertTrue(self.em.on_episodes_context_menu([self.episode._episode,]))
        self.assertFalse(self.em.on_episodes_context_menu([self.episode2._episode,]))
