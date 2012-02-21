#-*- coding: utf-8 -*-
# Automatically open .torrent files with a BitTorrent client
# Copy this script to ~/.config/gpodder/extensions/ to enable it.
# Thomas Perl <thp@gpodder.org>; 2010-10-11
import shlex
import subprocess

from gpodder import util

import logging
logger = logging.getLogger(__name__)


# Metadata for this extension
__title__ = 'Bittorrent downloader'
__description__ = 'Downloads the file if the file from the podcast ends with .torrent'
__author__ = "Thomas Perl <thp@gpodder.org>, Bernd Schlapsi <brot@gmx.info>"


DefaultConfig = {
    'extensions': {
        'bittorrent_downloader': {
            'cmd': u'transmission-cli %s'
        }
    }
}


class gPodderExtension:
    def __init__(self, container):
        self.container = container
        self.cmd = self.container.config.cmd

        #self.test = kwargs.get('test', False)
        #if self.test:
        #    self.cmd = 'echo "%s"' % self.cmd

        program = shlex.split(self.cmd)[0]
        if not util.find_command(program):
            raise ImportError("Couldn't find program '%s'" % program)

    def on_load(self):
        logger.info('Extension "%s" is being loaded.' % __title__)

    def on_unload(self):
        logger.info('Extension "%s" is being unloaded.' % __title__)

    def on_episode_downloaded(self, episode):
        if episode.extension() == '.torrent':
            self.notify_action("Downloading", episode)
            cmd = self.cmd % episode.local_filename(False)

            # Prior to Python 2.7.3, this module (shlex) did not
            # support Unicode input.
            cmd = util.sanitize_encoding(cmd)

            # for testing purpose it's possible to get to stdout+stderr
            # output
            p = subprocess.Popen(shlex.split(cmd), shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                self.notify_action("Downloading finished", episode)
            else:
                self.notify_action("Downloading finished with erros",
                    episode)

            if self.test:
                return (stdout, stderr)
