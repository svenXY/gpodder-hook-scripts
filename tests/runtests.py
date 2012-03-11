#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import shlex
import subprocess
import sys
import unittest

import logging
FMT = '%(created)f [%(name)s] %(levelname)s: %(message)s'
#logging.basicConfig(format=FMT, level=logging.DEBUG)
logging.basicConfig()

from config import data

def read_args():
    #read command line arguments
    parser = argparse.ArgumentParser(description='start gPodder extension script tests')
    parser.add_argument('--gpo', required=True, dest='gpo',
                        help='Path of the gPodder')
    parser.add_argument('--extension', required=True, dest='extension',
                        help='Path of the gPodder extension scripts')
    parser.add_argument('--init', required=False, action='store_true', default=False,
                        help='initialization of the test date ' +
                             '(e.g: downloading podcasts needed for the tests')
    return parser.parse_args()


def append_python_path(gpo_path, extension):
    gpo_src_path = os.path.join(gpo_path, 'src')
    if os.path.exists(gpo_src_path):
        sys.path.append(gpo_src_path)

    if os.path.exists(extension):
        sys.path.append(args.extension)


def ins_test_podcast(core, podcast_url, episode2dl=None):
    from gpodder import download

    podcast = core.model.load_podcast(podcast_url, create=True)

    if not podcast.pause_subscription:
        podcast.pause_subscription = True
        podcast.save()

    if episode2dl is not None:
        episode = podcast.get_all_episodes()[episode2dl]
        if (not episode.was_downloaded(and_exists=True)):
            task = download.DownloadTask(episode, core.config)
            task.status = download.DownloadTask.QUEUED
            task.run()


def init_data():
    from gpodder import core

    os.environ['GPODDER_DISABLE_EXTENSIONS'] = 'yes'
    gpo_core = core.Core()

    # set preferred youtube format to FLV (for flv2mp4 test)
    gpo_core.config.youtube_preferred_fmt_id = 34
    gpo_core.config.save()

    for name, conf in data.TEST_PODCASTS.items():
        ins_test_podcast(gpo_core, conf['url'], conf['episode'])

    gpo_core.shutdown()
    os.environ['GPODDER_DISABLE_EXTENSIONS'] = ''

if __name__ == "__main__":
    args = read_args()
    append_python_path(args.gpo, args.extension)

    test_dir = os.path.dirname(__file__)
    os.environ['GPODDER_HOME'] = os.path.join(test_dir, 'gpodder3', 'config')
    os.environ['GPODDER_DOWNLOAD_DIR'] = os.path.join(test_dir, 'gpodder3', 'config', 'Downloads')
    os.environ['GPODDER_EXTENSIONS'] = args.extension

    if args.init:
        init_data()

    #import all test files
    import bittorrent_downloader_test
    import cmml_generator_test
    import enqueue_in_vlc_test
    import flv2mp4_test
    import m4a_converter_test
    import mp3gain_test
    import normalize_audio_test
    import rename_download_test
    import rm_ogg_cover_test
    import rockbox_convert2mp4_test
    import tagging_test
    import tfh_shownotes_test
    import zpravy_test

    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(bittorrent_downloader_test)
    suite.addTests(loader.loadTestsFromModule(cmml_generator_test))
    suite.addTests(loader.loadTestsFromModule(enqueue_in_vlc_test))
    ## suite.addTests(loader.loadTestsFromModule(flv2mp4_test))
    ## suite.addTests(loader.loadTestsFromModule(m4a_converter_test))
    suite.addTests(loader.loadTestsFromModule(mp3gain_test))
    ## suite.addTests(loader.loadTestsFromModule(normalize_audio_test))
    suite.addTests(loader.loadTestsFromModule(rename_download_test))
    suite.addTests(loader.loadTestsFromModule(rm_ogg_cover_test))
    suite.addTests(loader.loadTestsFromModule(rockbox_convert2mp4_test))
    suite.addTests(loader.loadTestsFromModule(tagging_test))
    suite.addTests(loader.loadTestsFromModule(tfh_shownotes_test))
    suite.addTests(loader.loadTestsFromModule(zpravy_test))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
