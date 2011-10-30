# -*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/hooks/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

# Set this to the BitTorrent app of your choice
BITTORRENT_CMD = 'qbittorrent %s'


class gPodderHooks(object):
    def __init__(self, test=False):
        self.bittorrent_cmd = BITTORRENT_CMD
        self.test = test

        if test:
            self.bittorrent_cmd = 'echo "%s"' % self.bittorrent_cmd

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
            cmd = str(self.bittorrent_cmd % episode.local_filename(False))

            if self.test:
                p = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return p.communicate()
            else:
                subprocess.Popen(shlex.split(cmd))
