# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
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
    def __init__(self, container):
        self.container = container

    def milli_to_srt(self, time):
        srt_time = timedelta(milliseconds=time)
        srt_time = str(srt_time)
        if '.' in srt_time:
            srt_time = srt_time.replace('.', ',')[:11]
        else:
            # ',000' required to be a valid srt line
            srt_time += ',000'
        return srt_time

    def ted_to_srt(self, jsonstring, introduration):
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
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
        except (urllib2.URLError, urllib2.HTTPError), e:
            logger.debug("subtitle url returned error %s", e, exc_info=1)
            return ''
        return response.read()

    def on_episode_downloaded(self, episode):
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

        # default to '0' ?
        # TODO: add try/except when dealing with files.
        introduration = episode_data.split('introDuration=')[1].split('&')[0]
        if introduration:
            current_filename = episode.local_filename(create=False)
            basename, _ = os.path.splitext(current_filename)

            sub = self.ted_to_srt(sub_data, int(introduration))
            srtFile = open(basename + '.srt', 'w+')
            srtFile.write(sub.encode("utf-8"))
            srtFile.close()
