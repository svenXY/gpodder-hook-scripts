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
from gpodder.extensions import ExtensionParent

DEFAULT_PARAMS = { 
    "context_menu": {
        "desc": u"add plugin to the context-menu",
        "value": True,
        "type": u"checkbox",
    }   
}

CMD = {
    'Linux': 'mp3gain -c "%s"',
    'Windows': 'mp3gain.exe -c "%s"'
}


class gPodderExtensions(ExtensionParent):
    def __init__(self, params=DEFAULT_PARAMS, **kwargs):
        super(gPodderExtensions, self).__init__(params=params, **kwargs)
        self.context_menu_callback = self._convert_episodes

        self.cmd = CMD[platform.system()]
        self.check_command(self.cmd)

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _show_context_menu(self, episodes):
        if not self.params['context_menu']:
            return False

        files = [e.download_filename for e in episodes]
        if 'mp3' not in [os.path.splitext(f)[1][1:].lower() for f in files]:
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
            if isinstance(cmd, unicode):
                cmd = cmd.encode('ascii', 'ignore')

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
