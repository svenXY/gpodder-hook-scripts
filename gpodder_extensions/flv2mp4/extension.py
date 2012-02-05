# -*- coding: utf-8 -*-
# Put FLV files from YouTube into a MP4 container after download
# This requires ffmpeg to be installed. Also works as a context
# menu item for already-downloaded files. This does not convert
# the files in reality, but just swaps the container format.
#
# (c) 2011-08-05 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.

import gpodder
from gpodder.util import sanitize_encoding
from gpodder import youtube
from gpodder.extensions import ExtensionParent

import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

PARAMS = {
    'context_menu': {
        'desc': 'add plugin to the context-menu',
        'type': 'checkbox',
    }
}

DEFAULT_CONFIG = {
    'extensions': {
        'flv2mp4': {
            'context_menu': True,
        }
    }
}

FFMPEG_CMD = 'ffmpeg -i "%(infile)s" -vcodec copy -acodec copy "%(outfile)s"'


class gPodderExtension(ExtensionParent):
    def __init__(self, config=DEFAULT_CONFIG, **kwargs):
        super(gPodderExtension, self).__init__(config=config, **kwargs)
        self.context_menu_callback = self._convert_episodes

        self.test = kwargs.get('test', False)
        self.check_command(FFMPEG_CMD)

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def _show_context_menu(self, episodes):
        if not self.config.context_menu:
            return False

        if 'video/x-flv' not in [e.mime_type for e in episodes]:
            return False
        return True

    def _convert_episode(self, episode):
        if not youtube.is_video_link(episode.url):
            logger.debug('Not a YouTube video. Ignoring.')
            return

        filename = episode.local_filename(create=False)
        dirname = os.path.dirname(filename)
        basename, ext = os.path.splitext(os.path.basename(filename))

        if open(filename, 'rb').read(3) != 'FLV':
            logger.debug('Not a FLV file. Ignoring.')
            return

        if ext == '.mp4':
            # Move file out of place for conversion
            newname = os.path.join(dirname, basename+'.flv')
            os.rename(filename, newname)
            filename = newname

        target = os.path.join(dirname, basename+'.mp4')
        cmd = FFMPEG_CMD % {
            'infile': filename,
            'outfile': target
        }

        # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
        cmd = sanitize_encoding(cmd)

        ffmpeg = subprocess.Popen(shlex.split(cmd),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = ffmpeg.communicate()

        if ffmpeg.returncode == 0:
            logger.info('FLV conversion successful.')
            if not self.test:
                self.rename_episode_file(episode, basename+'.mp4')
                os.remove(filename)
        else:
            logger.info('Error converting file. FFMPEG installed?')
            try:
                os.remove(target)
            except OSError:
                pass

    def _convert_episodes(self, episodes):
        for episode in episodes:
            self._convert_episode(episode)
