#!/usr/bin/python
# -*- coding: utf-8 -*-
# Requirements: apt-get install python-kaa-metadata  ffmpeg python-dbus
# To use, copy it as a Python script into ~/.config/gpodder/extensions/rockbox_mp4_convert.py
# See the module "gpodder.extensions" for a description of when each extension
# gets called and what the parameters of each extension are.
#Based on Rename files after download based on the episode title
#And patch in Bug https://bugs.gpodder.org/show_bug.cgi?id=1263
# Copyright (c) 2011-04-06 Guy Sheffer <guysoft at gmail.com>
# Copyright (c) 2011-04-04 Thomas Perl <thp.io>
# Licensed under the same terms as gPodder itself
from gpodder import util
from gpodder.extensions import ExtensionParent

import kaa.metadata
import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)

PARAMS = {
    "device_height": {
        "desc": u'Device height',
        "type": u'spinbutton',
    },
    "device_width": {
        "desc": u'Device width',
        "type": u'spinbutton',
    },
    "ffmpeg_options": {
        "desc": u'ffmpeg options',
        "type": u'textitem',
    }
}

DEFAULT_CONFIG = {
    'extensions': {
        'rockbox_convert2mp4': {
            "device_height": 176.0,
            "device_width": 224.0,
            "ffmpeg_options": u'-vcodec mpeg2video -b 500k -ab 192k -ac 2 -ar 44100 -acodec libmp3lame',
        }
    }
}

ROCKBOX_EXTENTION = "mpg"
EXTENTIONS_TO_CONVERT = ['.mp4',"." + ROCKBOX_EXTENTION]
FFMPEG_CMD = 'ffmpeg -y -i "%(from)s" -s %(width)sx%(height)s %(options)s "%(to)s"'


class gPodderExtensions(ExtensionParent):
    def __init__(self, config=DEFAULT_CONFIG, **kwargs):
        super(gPodderExtensions, self).__init__(config=config, **kwargs)

        self.check_command(FFMPEG_CMD)

    def on_episode_downloaded(self, episode):
        current_filename = episode.local_filename(False)
        converted_filename = self._convert_mp4(episode, current_filename)

        if converted_filename is not None:
            self.update_episode_file(episode, converted_filename)
            os.remove(current_filename)
            logger.info('Conversion for %s was successfully' % current_filename)
        else:
            logger.info('Conversion for %s had errors' % current_filename)

    def _get_rockbox_filename(self, origin_filename):
        if not os.path.exists(origin_filename):
            return None

        dirname = os.path.dirname(origin_filename)
        filename = os.path.basename(origin_filename)
        basename, ext = os.path.splitext(filename)

        if ext not in EXTENTIONS_TO_CONVERT:
            return None

        if filename.endswith(ROCKBOX_EXTENTION):
            new_filename = "%s-convert.%s" % (basename, ROCKBOX_EXTENTION)
        else:
            new_filename = "%s.%s" % (basename, ROCKBOX_EXTENTION)
        return os.path.join(dirname, new_filename)


    def _calc_resolution(self, video_width, video_height, device_width, device_height):
        if video_height is None:
            return None
            
        width_ratio = device_width / video_width
        height_ratio = device_height / video_height
                    
        dest_width = device_width
        dest_height = width_ratio * video_height
                    
        if dest_height > device_height:
            dest_width = height_ratio * video_width
            dest_height = device_height

        return (int(round(dest_width)), round(int(dest_height)))


    def _convert_mp4(self, episode, from_file):
        """Convert MP4 file to rockbox mpg file"""
        # generate new filename and check if the file already exists
        to_file = self._get_rockbox_filename(from_file)
        if os.path.isfile(to_file):
            return to_file

        logger.info("Converting: %s", from_file)
        self.notify_action("Converting", episode)

        # calculationg the new screen resolution
        info = kaa.metadata.parse(from_file)
        resolution = self._calc_resolution(
            info.video[0].width,
            info.video[0].height,
            self.config.device_width,
            self.config.device_height
        )
        if resolution is None:
            logger.error("Error calculating the new screen resolution") 
            return None
            
        convert_command = FFMPEG_CMD % {
            'from': from_file,
            'to': to_file,
            'width': str(resolution[0]),
            'height': str(resolution[1]),
            'options': self.config.ffmpeg_options
        }

        # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
        if isinstance(convert_command, unicode):
            convert_command = convert_command.encode('ascii', 'ignore')

        process = subprocess.Popen(shlex.split(convert_command),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logger.error(stderr)
            return None

        self.notify_action("Converting finished", episode)

        return to_file
