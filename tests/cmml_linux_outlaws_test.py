#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import unittest
import urllib2

import cmml_linux_outlaws

LINUXOUTLAWS_FILENAME='linuxoutlaws230.ogg'

def create_cmml_from_file(ogg_file):
    m = re.match('(.*linuxoutlaws)([0-9]+)\\.(ogg|mp3)',ogg_file)
    if m is not None:
        episode_num = m.group(2)
        url = 'http://sixgun.org/linuxoutlaws/' + episode_num
        page = urllib2.urlopen(url)
        cmml_linux_outlaws.create_cmml(page, ogg_file)
    else:
        print("not a Linux Outlaws file !")


class TestCmmlLinuxOutlaws(unittest.TestCase):
    def tearDown(self):
        cmml_file = cmml_linux_outlaws.get_cmml_filename(LINUXOUTLAWS_FILENAME)
        if os.path.exists(cmml_file):
            os.remove(cmml_file)

    def test_create_cmml(self):
        cmml_file = cmml_linux_outlaws.get_cmml_filename(LINUXOUTLAWS_FILENAME)
        create_cmml_from_file(LINUXOUTLAWS_FILENAME)
        self.assertTrue(os.path.exists(cmml_file))
        self.assertTrue(os.path.getsize(cmml_file)>0)
