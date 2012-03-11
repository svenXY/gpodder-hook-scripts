#-*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/extensions/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

import gpodder
from gpodder import util

import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('Bittorrent downloader')
__description__ = _('Downloads the file if the file from the podcast ends with .torrent')
__author__ = 'Thomas Perl <thp@gpodder.org>, Bernd Schlapsi <brot@gmx.info>'


DefaultConfig = {
    'cmd': 'transmission-cli %s'
}


class gPodderExtension:
    def __init__(self, container):
        self.container = container
        self.config = self.container.config

        # Dependency checks
        program = shlex.split(self.config.cmd)[0]
        self.container.require_command(program)

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            self.container.manager.on_notification_show('Downloading', episode)
            cmd = self.config.cmd % episode.local_filename(False)

            p = subprocess.Popen(shlex.split(cmd), shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                self.container.manager.on_notification_show('Downloading finished', episode)
            else:
                self.container.manager.on_notification_show('Downloading finished with erros',
                    episode)

