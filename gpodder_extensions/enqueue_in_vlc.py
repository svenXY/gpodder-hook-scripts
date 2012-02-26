# -*- coding: utf-8 -*-
# Extension script to add a context menu item for enqueueing episodes in a player
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
# (c) 2011-06-08 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.
import shlex
import subprocess

from gpodder import util

import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('Enqueue in VLC')
__description__ = _('Add a context menu item for enqueueing episodes in VLC')
__author__ = 'Thomas Perl <thp@gpodder.org>, Bernd Schlapsi <brot@gmx.info>'
__only_for__ = 'gtk'


CMD = "vlc --started-from-file --playlist-enqueue"

class gPodderExtension:
    def __init__(self, container):
        self.container = container

        #self.cmd = kwargs.get('cmd', CMD)
        self.cmd = CMD
        program = shlex.split(self.cmd)[0]
        if not util.find_command(program):
            raise ImportError("Couldn't find program '%s'" % program)

    def on_load(self):
        logger.info('Extension "%s" is being loaded.' % __title__)

    def on_unload(self):
        logger.info('Extension "%s" is being unloaded.' % __title__)

    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        subprocess.Popen(shlex.split(self.cmd) + filenames,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def on_episodes_context_menu(self, episodes):
        if not [e for e in episodes if e.file_exists()]:
            return None

        return [(self.container.metadata.title, self._enqueue_episodes)]


