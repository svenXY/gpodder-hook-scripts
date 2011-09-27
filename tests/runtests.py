#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import shlex
import subprocess
import sys
import unittest


def read_args():
    #read command line arguments
    parser = argparse.ArgumentParser(description='start gPodder hook script tests')
    parser.add_argument('--gpo_bin', required=False, dest='gpo_bin',
                        help='Path of the gPodder bin files')
    parser.add_argument('--gpo_src', required=True, dest='gpo_src',
                        help='Path of the gPodder source')
    parser.add_argument('--hook_src', required=True, dest='hook_src',
                        help='Path of the gPodder hook scripts')
    parser.add_argument('--init', required=False, action='store_true', default=False,
                        help='initialization of the test date ' +
                             '(e.g: downloading podcasts needed for the tests')
    return parser.parse_args()


def append_python_path(gpo_src, hook_src):
    if os.path.exists(gpo_src):
        sys.path.append(args.gpo_src)

    if os.path.exists(hook_src):
        sys.path.append(args.hook_src)


def check_version(gpo_bin):
    cmd = '%sgpodder --version' % os.path.join(gpo_bin, '')
    myprocess = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = myprocess.communicate()

    if myprocess.returncode > 0:
        raise NameError("couldn't start gpodder with '%s'" % cmd)
    else:
        # group(0): gpodder 2.19, group(1): gpodder, group(2): 2, group(3): 19
        m = re.match(r'(\w+) ([0-9])\.([0-9]+)', stdout)
        if m is not None and m.group(2) in ('2', '3'):
            return int(m.group(2))
        else:
            raise NameError("couldn't read gpodder version number")


def init_data():
    from gpodder import api

    client = api.PodcastClient()
  
    # TinFoilHat Testdata
    TINFOILHAT='http://feeds.feedburner.com/TinFoilHat'
    podcast = client.create_podcast(TINFOILHAT)
    podcast.disable()
    pilot_show = podcast.get_episodes()[-1]
    if (not pilot_show.is_downloaded):
        pilo_show.download()

    client._db.close()


if __name__ == "__main__":
    args = read_args()
    print args
    append_python_path(args.gpo_src, args.hook_src)

    gpo_version = check_version(args.gpo_bin or '')
    test_dir = os.path.dirname(__file__)
    if gpo_version == 2:
        os.environ['GPODDER_HOME'] = os.path.join(test_dir, 'gpodder2', 'config')
        os.environ['GPODDER_DOWNLOAD_DIR'] = os.path.join(test_dir, 'gpodder2', 'downloads')

    elif gpo_version == 3:
        # TODO: add settings for version 3 of gpodder
        pass

    if args.init:
        init_data()

    #import all test files
    import cmml_linux_outlaws_test
    import tfh_shownotes_test

    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(cmml_linux_outlaws_test)
    suite.addTests(loader.loadTestsFromModule(tfh_shownotes_test))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
