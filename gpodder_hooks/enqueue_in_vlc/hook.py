# -*- coding: utf-8 -*-
# Hook script to add a context menu item for enqueueing episodes in a player
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
# (c) 2011-06-08 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.
import shlex
import subprocess

import gpodder
from metadata import metadata
from util import check_command

CMD = "vlc --started-from-file --playlist-enqueue" 

class gPodderHooks(object):
    def __init__(self, params=CMD):
        self.cmd = params 
        check_command(self.cmd)

    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        subprocess.Popen(shlex.split(self.cmd) + filenames,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def on_episodes_context_menu(self, episodes):
        return [(metadata['name'], self._enqueue_episodes)]
