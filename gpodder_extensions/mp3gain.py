# -*- coding: utf-8 -*-
# This extension adjusts mp3s so that they all have the same volume
#
# Requires: mp3gain
#
# (c) 2011-11-06 Bernd Schlapsi <brot@gmx.info>
# Released under the same license terms as gPodder itself.
import os
import platform
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

import gpodder
from gpodder.util import sanitize_encoding
from gpodder.extensions import ExtensionParent

# Metadata for this extension
__id__ = 'mp3gain'
__name__ = 'mp3gain'
__desc__ = 'This hook adjusts mp3s so that they all have the same volume. It don\'t decode and re-encode the audio file'


PARAMS = {
    'context_menu': {
        'desc': u'add plugin to the context-menu',
        'type': u'checkbox',
    }
}

DEFAULT_CONFIG = {
    'extensions': {
        'mp3gain': {
            'context_menu': True,
        }
    }
}

CMD = {
    'Linux': 'mp3gain -c "%s"',
    'Windows': 'mp3gain.exe -c "%s"'
}


class gPodderExtension(ExtensionParent):
    def __init__(self, config=DEFAULT_CONFIG, **kwargs):
        super(gPodderExtension, self).__init__(config=config, **kwargs)
        self.context_menu_callback = self._convert_episodes

        self.cmd = CMD[platform.system()]
        self.check_command(self.cmd)

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _show_context_menu(self, episodes):
        if not self.config.context_menu:
            return False

        if 'audio/mpeg' not in [e.mime_type for e in episodes if e.mime_type is not None]:
            return False

        return True

    def _convert_episode(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        (basename, extension) = os.path.splitext(filename)
        if episode.file_type() == 'audio' and extension.lower().endswith('mp3'):

            cmd = self.cmd % filename

            # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
            cmd = sanitize_encoding(cmd)

            p = subprocess.Popen(shlex.split(cmd),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                logger.info('mp3gain processing successfull.')

            else:
                logger.info('mp3gain processing not successfull.')
                logger.debug(stderr)

    def _convert_episodes(self, episodes):
        for episode in episodes:
            self._convert_episode(episode)
