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


def check_version(gpo_path):
    gpo_bin_path = os.path.join(gpo_path, 'bin')
    cmd = '%sgpodder --version' % os.path.join(gpo_bin_path, '')
    myprocess = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = myprocess.communicate()

    if myprocess.returncode > 0:
        raise NameError("couldn't start gpodder with '%s'" % cmd)
    else:
        # group(0): gpodder 2.19, group(1): gpodder, group(2): 2.19
        m = re.match(r'(\w+) ([0-9]\.[0-9]+)', stdout)
        if m is not None and m.group(2) is not None:
            try:
                version = float(m.group(2))
                if 2.0 < version < 2.99:
                    return 2
                elif version >= 2.99:
                    return 3
                else:
                    raise NameError("couldn't read gpodder version number")
            except:
                raise NameError("couldn't read gpodder version number")


def ins_test_podcast(client, podcast_url, episode2dl=None):
    podcast = client.get_podcast(podcast_url)
    if podcast is None:
        podcast = client.create_podcast(podcast_url)
        podcast.disable()

    if episode2dl is not None:
        episode = podcast.get_episodes()[episode2dl]
        if (not episode.is_downloaded):
            episode.download()


def init_data():
    from config import data
    from gpodder import api

    client = api.PodcastClient()

    # set preferred youtube format to FLV (for flv2mp4 test)
    client._config.youtube_preferred_fmt_id = 34
    client._config.save()

    for name, conf in data.TEST_PODCASTS.items():
        ins_test_podcast(client, conf['url'], conf['episode'])

    client._db.close()


if __name__ == "__main__":
    args = read_args()
    append_python_path(args.gpo, args.extension)

    gpo_version = check_version(args.gpo or '')
    test_dir = os.path.dirname(__file__)
    if gpo_version == 2:
        os.environ['GPODDER_HOME'] = os.path.join(test_dir, 'gpodder2', 'config')
        os.environ['GPODDER_DOWNLOAD_DIR'] = os.path.join(test_dir, 'gpodder2', 'downloads')

    elif gpo_version == 3:
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
    suite.addTests(loader.loadTestsFromModule(flv2mp4_test))
    suite.addTests(loader.loadTestsFromModule(m4a_converter_test))
    suite.addTests(loader.loadTestsFromModule(mp3gain_test))
    suite.addTests(loader.loadTestsFromModule(normalize_audio_test))
    suite.addTests(loader.loadTestsFromModule(rename_download_test))
    suite.addTests(loader.loadTestsFromModule(rm_ogg_cover_test))
    suite.addTests(loader.loadTestsFromModule(rockbox_convert2mp4_test))
    suite.addTests(loader.loadTestsFromModule(tagging_test))
    suite.addTests(loader.loadTestsFromModule(tfh_shownotes_test))
    suite.addTests(loader.loadTestsFromModule(zpravy_test))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
