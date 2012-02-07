#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import unittest

from gpodder import api
from config import data
from utils import get_episode, get_metadata
import rockbox_convert2mp4 as extension


class TestRockboxMP4Convert(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        self.episode, self.filename = get_episode(self.client,
            data.TEST_PODCASTS['TEDTalks'], True)
        
        self.metadata = get_metadata(extension)
        self.rb_extension = extension.gPodderExtension(metadata=self.metadata) 

    def tearDown(self):
        self.client._db.close()

        converted_file = self.rb_extension._get_rockbox_filename(self.filename)
        if (os.path.exists(converted_file)):
            os.remove(converted_file)

    def test_file_renaming(self):
        self.assertIsNotNone(self.filename)
        self.assertEqual(os.path.basename(self.filename), 'MattCutts_2011U.mp4')
        self.assertEqual(self.rb_extension._get_rockbox_filename(self.filename),
            os.path.join(os.path.dirname(self.filename), 'MattCutts_2011U.mpg'))
        
    def test_calc_resolution(self):
        resolution = self.rb_extension._calc_resolution(512, 288, 224.0, 176.0)
        self.assertEqual(resolution, (224, 126))

        resolution = self.rb_extension._calc_resolution(1024, 768, 224.0, 176.0)
        self.assertEqual(resolution, (224, 168))

    def test_mp4convert(self):
        self.assertIsNotNone(self.filename)
        self.assertEqual(self.episode._episode.title, 'TED: Matt Cutts: Try something new for 30 days - Matt Cutts (2011)')

        new_filename = self.rb_extension._convert_mp4(self.episode._episode, self.filename)
        self.assertIsNotNone(new_filename)
        self.assertTrue(os.path.exists(new_filename))
