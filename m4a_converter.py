# -*- coding: utf-8 -*-
# Convertes m4a audio files to mp3
# This requires ffmpeg to be installed. Also works as a context
# menu item for already-downloaded files.
#
# (c) 2011-11-23 Bernd Schlapsi <brot@gmx.info>
# Released under the same license terms as gPodder itself.

import gpodder

import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)


FFMPEG_CMD = 'ffmpeg -i "%(infile)s" -sameq "%(outfile)s"'
MIME_TYPES = ['audio/x-m4a', 'audio/mp4']
EXTENSION = '.mp3'


class gPodderExtensions(ExtensionParent):
    def __init__(self, test=False):
        self.test = test

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _convert_episode(self, episode):
        filename = episode.local_filename(create=False)
        dirname = os.path.dirname(filename)
        basename, ext = os.path.splitext(os.path.basename(filename))
        new_filename = basename + EXTENSION

        if episode.mime_type not in MIME_TYPES:
            return

        target = os.path.join(dirname, new_filename)
        cmd = FFMPEG_CMD % {
            'infile': filename,
            'outfile': target 
        }

        # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
        if isinstance(cmd, unicode):
            cmd = cmd.encode('ascii', 'ignore')
            
        ffmpeg = subprocess.Popen(shlex.split(cmd),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = ffmpeg.communicate()

        if ffmpeg.returncode == 0:
            logger.info('m4a -> mp3 conversion successful.')
            if not self.test:
                os.remove(filename)
                episode.download_filename = new_filename
                episode.save()
        else:
            logger.info('Error converting file. FFMPEG installed?')
            try:
                os.remove(target)
            except OSError:
                pass
