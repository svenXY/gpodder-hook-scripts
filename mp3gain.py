# -*- coding: utf-8 -*-
# This hook adjusts mp3s so that they all have the same volume 
#
# Requires: mp3gain
#
# (c) 2011-11-06 Bernd Schlapsi <brot@gmx.info>
# Released under the same license terms as gPodder itself.

import gpodder
from gpodder import youtube

import os
import platform
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

CMD = {
    'Linux': 'mp3gain -c "%s"',
    'Windows': 'mp3gain.exe -c "%s"'
}


class gPodderHooks(object):
    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _convert_episode(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        (basename, extension) = os.path.splitext(filename)
        if episode.file_type() == 'audio' and extension.lower().endswith('mp3'):

            # get platform specific command
            cmd = CMD[platform.system()]

            # start command
            p = subprocess.Popen(shlex.split(cmd % filename),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                logger.info('mp3gain processing successfull.')

            else:
                logger.info('mp3gain processing not successfull.')
                logger.debug(stderr)
