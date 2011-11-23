#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import os
import shutil
import unittest

from gpodder import api
from config import data
import mp3split

def get_splitfiles(from_filename):
    path, filename = os.path.split(from_filename)
    filename2, ext = os.path.splitext(filename)
    files2delete = os.path.join(path, "%s_*%s" % (filename2, ext))
    return glob.glob(files2delete)


class TestRenameDownloads(unittest.TestCase):
    def setUp(self):
        self.client = api.PodcastClient()

        url = data.TEST_PODCASTS['TinFoilHat']['url']
        episodeno = data.TEST_PODCASTS['TinFoilHat']['episode']
        self.podcast = self.client.get_podcast(url)
        self.podcast_title = self.podcast.title

        self.episode = self.podcast.get_episodes()[episodeno]
        self.filename = self.episode._episode.local_filename(create=False, check_only=True)
        self.title = self.episode.title

    def tearDown(self):
        self.client._db.close()

        for splitfile in get_splitfiles(self.filename):
            os.remove(splitfile)

    def test_mp3split(self):
        self.assertEqual(os.path.split(self.filename)[1], 'TFH-001.mp3')

        basename, ext = os.path.splitext(self.filename)
        filename_new = "%s-test%s" % (basename, ext)
        shutil.copyfile(self.filename, filename_new)
        mp3split.mp3split(self.filename, filename_new)

        generated_files = get_splitfiles(self.filename)
        self.assertEqual(len(generated_files), 2)

        self.assertIn('TFH-001_1.mp3', [os.path.split(f)[1] for f in generated_files])
        self.assertIn('TFH-001_2.mp3', [os.path.split(f)[1] for f in generated_files])

