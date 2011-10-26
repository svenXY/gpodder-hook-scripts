# -*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/hooks/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

DEFAULT_PARAMS = {
    "bittorrent_cmd": {
        "desc": "Defines the command line bittorrent program:",
        "value": "qbittorrent %s",
        "type": "textitem"
    }
}

class gPodderHooks(object):
    def __init__(self, params=DEFAULT_PARAMS):
        self.bittorrent_cmd = params['bittorrent_cmd']['value']

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            cmd = self.bittorrent_cmd % episode.local_filename(False)
            subprocess.Popen(shlex.split(cmd))

