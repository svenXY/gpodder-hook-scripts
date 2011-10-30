#!/usr/bin/python
# -*- coding: utf-8 -*-
# Requirements: apt-get install python-kaa-metadata  ffmpeg python-dbus
# To use, copy it as a Python script into ~/.config/gpodder/hooks/rockbox_mp4_convert.py
# See the module "gpodder.hooks" for a description of when each hook
# gets called and what the parameters of each hook are.
#Based on Rename files after download based on the episode title
#And patch in Bug https://bugs.gpodder.org/show_bug.cgi?id=1263
# Copyright (c) 2011-04-06 Guy Sheffer <guysoft at gmail.com>
# Copyright (c) 2011-04-04 Thomas Perl <thp.io>
# Licensed under the same terms as gPodder itself
from util import check_command, init_dbus, message
from gpodder import util

import kaa.metadata
import os
import shlex
import subprocess

import logging
logger = logging.getLogger(__name__)


DEFAULT_PARAMS = {
    "device_width": {
        "desc": 'Device width',
        "value": 224.0,
        "type": 'spinbutton'
    },
    "device_height": {
        "desc": 'Device height',
        "value": 176.0,
        "type": 'spinbutton'
    },
    "ffmpeg_options": {
        "desc": 'ffmpeg options',
        "value": '-vcodec mpeg2video -b 500k -ab 192k -ac 2 -ar 44100 -acodec libmp3lame',
        "type": 'textitem'
    }
}

ROCKBOX_EXTENTION = "mpg"
EXTENTIONS_TO_CONVERT = ['.mp4',"." + ROCKBOX_EXTENTION]
FFMPEG_CMD = 'ffmpeg -y -i "%(from)s" -s %(width)sx%(height)s %(options)s "%(to)s"'

NOTIFY_INTERFACE = init_dbus()

def get_rockbox_filename(origin_filename):
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


def calc_resolution(video_width, video_height, device_width, device_height):
    if video_height is None:
        return None
        
    width_ratio = device_width / video_width
    height_ratio = device_height / video_height
                
    dest_width = device_width
    dest_height = width_ratio * video_height
                
    if dest_height > device_height:
        dest_width = height_ratio * video_width
        dest_height = device_height

    return (dest_width, dest_height)


def convert_mp4(from_file, params):
    """Convert MP4 file to rockbox mpg file"""
    # generate new filename and check if the file already exists
    to_file = get_rockbox_filename(from_file)
    if os.path.isfile(to_file):
        return to_file

    logger.info("Converting: %s", from_file)

    # calculationg the new screen resolution
    info = kaa.metadata.parse(from_file)
    resolution = calc_resolution(
        info.video[0].width,
        info.video[0].height,
        params['device_width']['value'],
        params['device_height']['value']
    )
    if resolution is None:
        logger.error("Error calculating the new screen resolution") 
        return None
    dest_width, dest_height = resolution
        
    # Running conversion command (ffmpeg)
    message(NOTIFY_INTERFACE, 'Running conversion script',
        "Converting '%s'" % from_file
    )
    convert_command = FFMPEG_CMD % {
        'from': from_file,
        'to': to_file,
        'width': str(int(dest_width)),
        'height': str(int(dest_height)),
        'options': params['ffmpeg_options']['value']
    }

    # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
    process = subprocess.Popen(shlex.split(str(convert_command)),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        logger.error(stderr)
        return None

    return to_file


class gPodderHooks(object):
    def __init__(self, params=DEFAULT_PARAMS):
        logger.info("RockBox mp4 converter hook loaded")
        self.params = params

        check_command(FFMPEG_CMD)

    def on_episode_downloaded(self, episode):
        current_filename = episode.local_filename(False)
        converted_filename = convert_mp4(current_filename, self.params)

        if converted_filename is not None:
            episode.filename = os.path.basename(converted_filename)
            episode.save()
            os.remove(current_filename)
            logger.info('Conversion for %s was successfully' % current_filename)
        else:
            logger.info('Conversion for %s had errors' % current_filename)
