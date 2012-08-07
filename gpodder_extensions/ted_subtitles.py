# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
"""
TED Subtitle Download Extension
Downloads ted subtitles
"""
import os
import json
import urllib2
import logging
from datetime import timedelta
logger = logging.getLogger(__name__)

__title__ = 'TED Subtitle Download Extension'
__description__ = 'downloads ted subtitles'
__only_for__ = 'gtk, cli, qml'
__authors__ = 'Danilo Shiga <daniloshiga@gmail.com>'


class gPodderExtension(object):
    """
    TED Subtitle Download Extension
    Downloads ted subtitles
    """
    def __init__(self, container):
        self.container = container

    def milli_to_srt(self, time):
        """Converts milliseconds to srt time format"""
        srt_time = timedelta(milliseconds=time)
        srt_time = str(srt_time)
        if '.' in srt_time:
            srt_time = srt_time.replace('.', ',')[:11]
        else:
            # ',000' required to be a valid srt line
            srt_time += ',000'
        return srt_time

    def ted_to_srt(self, jsonstring, introduration):
        """Converts the json object to srt format"""
        jsonobject = json.loads(jsonstring)

        srtContent = ''
        for captionIndex, caption in enumerate(jsonobject['captions'], 1):
            startTime = self.milli_to_srt(introduration + caption['startTime'])
            endTime = self.milli_to_srt(introduration + caption['startTime'] +
                                        caption['duration'])
            srtContent += ''.join([str(captionIndex), os.linesep, startTime,
                                   ' --> ', endTime, os.linesep,
                                   caption['content'], os.linesep * 2])
        return srtContent

    def get_data_from_url(self, url):
        """deal with url requests"""
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
        except (urllib2.URLError, urllib2.HTTPError), e:
            logger.debug("subtitle url returned error %s", e, exc_info=1)
            return ''
        return response.read()

    def get_srt_filename(self, episode):
        current_filename = episode.local_filename(create=False)
        basename, _ = os.path.splitext(current_filename)
        return basename + '.srt'

    def on_episode_delete(self, episode, filename):
        self.delete_srt_file(episode)

    def delete_srt_file(self, episode):
        srt_file = self.get_srt_filename(episode)
        if os.path.exists(srt_file):
            os.remove(srt_file) 

    def on_episode_downloaded(self, episode):
        """Gpodder hook"""
        talkId = episode.guid.split(':')[1]
        try:
            int(talkId)
        except ValueError:
            logger.debug('invalid talk id: %s', talkId)
            return

        sub_url = 'http://www.ted.com/talks/subtitles/id/%s/lang/eng' % talkId
        logger.debug('subtitle url: %s', sub_url)
        sub_data = self.get_data_from_url(sub_url)
        if not sub_data:
            return

        logger.debug('episode url: %s', episode.link)
        episode_data = self.get_data_from_url(episode.link)
        if not episode_data:
            return

        intro = episode_data.split('introDuration=')[1].split('&')[0] or 0
        sub = self.ted_to_srt(sub_data, int(intro))
        srt_filename = self.get_srt_filename(episode)

        try:
            srtFile = open(srt_filename, 'w+')
            srtFile.write(sub.encode("utf-8"))
        except IOError:
            logger.debug("Can't write srt file")
        else:
            srtFile.close()
