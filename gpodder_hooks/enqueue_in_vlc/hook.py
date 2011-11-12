# -*- coding: utf-8 -*-
# Hook script to add a context menu item for enqueueing episodes in a player
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
# (c) 2011-06-08 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.
import shlex
import subprocess

import gpodder
from gpodder.hooks import HookParent

CMD = "vlc --started-from-file --playlist-enqueue" 

class gPodderHooks(HookParent):
    def __init__(self, metadata=None, params=None, cmd=CMD):
        super(gPodderHooks, self).__init__(metadata=metadata, params=params)

        self.cmd = cmd
        self.check_command(self.cmd)

    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        subprocess.Popen(shlex.split(self.cmd) + filenames,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def on_episodes_context_menu(self, episodes):
        if self.metadata is None and not self.metadata.has_key('name'):
            return False

        return [(self.metadata['name'], self._enqueue_episodes)]
