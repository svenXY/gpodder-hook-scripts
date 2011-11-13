# -*- coding: utf-8 -*-
# This hook adjusts the volume of audio files to a standard level
# Supported file formats are mp3 and ogg
#
# Requires: normalize-audio, mpg123
#
# (c) 2011-11-06 Bernd Schlapsi <brot@gmx.info>
# Released under the same license terms as gPodder itself.
import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

import gpodder
from gpodder.hooks import HookParent


DEFAULT_PARAMS = { 
    "context_menu": {
        "desc": u"add plugin to the context-menu",
        "value": True,
        "type": u"checkbox",
    }   
}

# a tuple of (extension, command)
SUPPORTED = (('ogg', 'normalize-ogg "%s"'), ('mp3', 'normalize-mp3 "%s"'))

#TODO: add setting to use normalize-audio instead of normalizie-mp3 for mp3 files if wanted
# http://normalize.nongnu.org/README.html FAQ #5
#MP3_CMD = 'normalize-audio "%s"'

CMDS_TO_TEST = ('normalize-ogg', 'normalize-mp3', 'normalize-audio',
    'lame', 'mpg123', 'oggenc', 'oggdec')


class gPodderHooks(HookParent):
    def __init__(self, params=DEFAULT_PARAMS, **kwargs):
        super(gPodderHooks, self).__init__(params=params, **kwargs)

        for cmd in CMDS_TO_TEST:
            self.check_command(cmd)

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _show_context_menu(self, episodes):
        if not self.params['context_menu']:
            return False

        files = [e.download_filename for e in episodes]
        extensions = [os.path.splitext(f)[1][1:].lower() for f in files]
        if 'mp3' not in extensions and 'ogg' not in extensions:
            return False
        return True

    def on_episodes_context_menu(self, episodes):
        if self.metadata is None and not self.metadata.has_key('name'):
            return False

        if self._show_context_menu(episodes):
            return [(self.metadata['name'], self._convert_episodes)]

    def _convert_episode(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        formats, commands = zip(*SUPPORTED)
        (basename, extension) = os.path.splitext(filename)
        extension = extension.lstrip('.').lower()
        if episode.file_type() == 'audio' and extension in formats:

            cmd = commands[formats.index(extension)] % filename

            # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
            if isinstance(cmd, unicode):
                cmd = cmd.encode('ascii', 'ignore')

            p = subprocess.Popen(shlex.split(cmd),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                logger.info('normalize-audio processing successfull.')

            else:
                logger.info('normalize-audio processing not successfull.')
                logger.debug(stderr)

    def _convert_episodes(self, episodes):
        for episode in episodes:
            self._convert_episode(episode)
