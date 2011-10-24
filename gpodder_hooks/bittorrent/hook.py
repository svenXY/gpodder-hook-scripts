# -*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/hooks/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

class gPodderHooks(object):
    def __init__(self, params=None):
        if params is None:
            from metadata import params

        self.bittorrent_cmd = params['value']

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            cmd = self.bittorrent_cmd % episode.local_filename(False)
            subprocess.Popen(shlex.split(cmd))

