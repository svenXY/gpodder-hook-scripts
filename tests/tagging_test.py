#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil 
import unittest

from mutagen import File

from gpodder import api
from config import data
from utils import get_episode, get_metadata
from tagging import extension


class TestTagging(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['TinFoilHat'], True)
        self.filename_save = '%s.save' % self.filename 
        shutil.copyfile(self.filename, self.filename_save)

        self.metadata = get_metadata(extension)

    def tearDown(self):
        self.client._db.close()
        shutil.move(self.filename_save, self.filename)

    def test_get_info(self):
        tag_extension = extension.gPodderExtensions(metadata=self.metadata)
        info = tag_extension.read_episode_info(self.episode._episode)

        self.assertEqual('Tin Foil Hat', info['album'])
        self.assertEqual('Pilot show', info['title'])
        self.assertEqual('2010-10-23 21:00', info['pubDate'])
        self.assertEqual(self.filename, info['filename'])

    def test_write2file(self):
        tag_extension = extension.gPodderExtensions(metadata=self.metadata)
        info = tag_extension.read_episode_info(self.episode._episode)
        tag_extension.write_info2file(info)

        audio = File(info['filename'], easy=True)
        self.assertIsNotNone(audio)

        self.assertEqual(info['album'], audio.tags['album'][0])
        self.assertEqual(info['title'], audio.tags['title'][0])
        self.assertEqual(info['pubDate'], audio.tags['date'][0])
        self.assertEqual('Podcast', audio.tags['genre'][0])
