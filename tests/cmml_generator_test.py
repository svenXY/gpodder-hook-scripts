#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import unittest
import urllib2

from gpodder import api
from config import data
from utils import get_episode, get_metadata
from cmml_generator import extension

LINUXOUTLAWS_FILENAME='linuxoutlaws230.ogg'

def create_cmml_from_file(ogg_file):
    m = re.match('(.*linuxoutlaws)([0-9]+)\\.(ogg|mp3)',ogg_file)
    if m is not None:
        episode_num = m.group(2)
        url = 'http://sixgun.org/linuxoutlaws/' + episode_num
        page = urllib2.urlopen(url)
        extension.create_cmml_linux_outlaws(page, ogg_file)
    else:
        print("not a Linux Outlaws file !")


class TestCmmlLinuxOutlaws(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()
        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['LinuxOutlaws'], True)
        self.episode2, self.filename2 = get_episode(self.client,
            data.TEST_PODCASTS['TinFoilHat'], True)
        self.metadata = get_metadata(extension)

    def tearDown(self):
        extension.delete_cmml_file(LINUXOUTLAWS_FILENAME)
        extension.delete_cmml_file(self.filename)
        self.client._db.close()

    def test_create_cmml(self):
        cmml_file = extension.get_cmml_filename(LINUXOUTLAWS_FILENAME)
        create_cmml_from_file(LINUXOUTLAWS_FILENAME)
        self.assertTrue(os.path.exists(cmml_file))
        self.assertTrue(os.path.getsize(cmml_file)>0)

    def test_create_cmml_extension(self):
        cmml_extension = extension.gPodderExtensions(metadata=self.metadata)
        cmml_extension.on_episode_downloaded(self.episode._episode)
        cmml_file = extension.get_cmml_filename(self.filename)
        self.assertTrue(os.path.exists(cmml_file))
        self.assertTrue(os.path.getsize(cmml_file)>0)

    def test_context_menu(self):
        cmml_extension = extension.gPodderExtensions(metadata=self.metadata)
        self.assertTrue(cmml_extension._show_context_menu([self.episode._episode,]))
        self.assertFalse(cmml_extension._show_context_menu([self.episode2._episode,]))
