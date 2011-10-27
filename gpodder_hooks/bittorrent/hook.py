# -*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/hooks/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

DEFAULT_PARAM = {
    "bittorrent_cmd": {
        "desc": "Defines the command line bittorrent program:",
        "value": 'qbittorrent %s',
        "type": "textitem"
    }
}


class gPodderHooks(object):
    def __init__(self, param=DEFAULT_PARAM, stdout=False):
        self.bittorrent_cmd = param['bittorrent_cmd']['value']
        self.stdout = stdout

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
            cmd = str(self.bittorrent_cmd % episode.local_filename(False))

            # for testing purpose it's possible to get to stdout+stderr output
            if self.stdout:
                p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
                return p.communicate()
            else:
                subprocess.Popen(shlex.split(cmd))
