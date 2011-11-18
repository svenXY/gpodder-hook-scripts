# -*- coding: utf-8 -*-
# Extension script to add a context menu item for enqueueing episodes in a player
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
# (c) 2011-06-08 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.
import shlex
import subprocess

import gpodder
from gpodder.extensions import ExtensionParent

CMD = "vlc --started-from-file --playlist-enqueue" 

class gPodderExtensions(ExtensionParent):
    def __init__(self, **kwargs):
        super(gPodderExtensions, self).__init__(**kwargs)
        self.context_menu_callback = self._enqueue_episodes

        self.cmd = kwargs.get('cmd', CMD)
        self.check_command(self.cmd)

    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        subprocess.Popen(shlex.split(self.cmd) + filenames,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
    def _show_context_menu(self, episodes):        
        return True
