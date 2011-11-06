# -*- coding: utf-8 -*-
# This hook adjusts the volume of audio files to a standard level
# Supported file formats are mp3 and ogg
#
# Requires: normalize-audio, mpg123
#
# (c) 2011-11-06 Bernd Schlapsi <brot@gmx.info>
# Released under the same license terms as gPodder itself.

import gpodder
from gpodder import youtube

import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

# a tuple of (extension, command)
SUPPORTED = (('ogg', 'normalize-ogg "%s"'), ('mp3', 'normalize-mp3 "%s"'))

# http://normalize.nongnu.org/README.html FAQ #5
#MP3_CMD = 'normalize-audio "%s"'


class gPodderHooks(object):
    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _convert_episode(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        formats, commands = zip(*SUPPORTED)
        (basename, extension) = os.path.splitext(filename)
        extension = extension.lstrip('.').lower()
        if episode.file_type() == 'audio' and extension in formats:

            cmd = commands[formats.index(extension)] % filename

            p = subprocess.Popen(shlex.split(cmd),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                logger.info('normalize-audio processing successfull.')

            else:
                logger.info('normalize-audio processing not successfull.')
                logger.debug(stderr)
