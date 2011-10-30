# -*- coding: utf-8 -*-
# Put FLV files from YouTube into a MP4 container after download
# This requires ffmpeg to be installed. Also works as a context
# menu item for already-downloaded files. This does not convert
# the files in reality, but just swaps the container format.
#
# (c) 2011-08-05 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.

import gpodder
from gpodder import youtube

import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)


FFMPEG_CMD = 'ffmpeg -i "%(infile)s" -vcodec copy -acodec copy "%(outfile)s"'


class gPodderHooks(object):
    def __init__(self, test=False):
        self.test = test

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

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
        ffmpeg = subprocess.Popen(shlex.split(str(cmd)),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = ffmpeg.communicate()

        if ffmpeg.returncode == 0:
            logger.info('FLV conversion successful.')
            if not self.test:
                os.remove(filename)
                episode.download_filename = basename+'.mp4'
                episode.save()
        else:
            logger.info('Error converting file. FFMPEG installed?')
            try:
                os.remove(target)
            except OSError:
                pass
