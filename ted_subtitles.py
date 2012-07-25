# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Use a logger for debug output - this will be managed by gPodder
import os
import json
import urllib2
import logging
logger = logging.getLogger(__name__)

# Provide some metadata that will be displayed in the gPodder GUI
__title__ = 'TED Subtitle Download Extension'
__description__ = 'downloads ted subtitles'
__only_for__ = 'gtk, cli, qml'
__authors__ = 'Danilo Shiga <daniloshiga@gmail.com>'

class gPodderExtension:
    # The extension will be instantiated the first time it's used
    # You can do some sanity checks here and raise an Exception if
    # you want to prevent the extension from being loaded..
    def __init__(self, container):
        self.container = container

    def formattime(self, time):
        milliseconds = 0
        seconds = str(((time / 1000) % 60))
        minutes = str(((time / 1000) / 60))
        hours = str((((time / 1000) / 60) / 60))
        formatedtime = hours + ':' + minutes + ':' + seconds + ',' + milliseconds
        return formatedtime

    def ted_to_srt(self, jsonstring, introduration):
        jsonobject = json.loads( jsonstring )

        srtContent = ''
        captionIndex = 1

        for caption in jsonobject['captions'] :
            starttime = str ( self.formattime ( introduration + caption['starttime'] ) )
            endTime = str ( self.formattime ( introduration + caption['starttime'] + caption['duration'] ) )

            srtContent += ( str ( captionIndex ) + os.linesep )
            srtContent += ( starttime + ' --> ' + endTime + os.linesep )
            srtContent += ( caption['content'] + os.linesep )
            srtContent += os.linesep

            captionIndex = captionIndex + 1
        return srtContent

    def on_episode_downloaded(self, episode):
        current_filename = episode.local_filename(create=False)
        basename, _ = os.path.splitext(current_filename)
        talkId = episode.guid.split(':')[1]
        try:
            int(talkId)
        except ValueError:
            return
        sub_url = 'http://www.ted.com/talks/subtitles/id/' + str(talkId) + '/lang/eng'
        logger.debug('subtitle url: %s', sub_url)
        logger.debug('episode url: %s', episode.link)

        try:
            req = urllib2.Request(sub_url)
            response = urllib2.urlopen(req)
            result = response.read()
        except urllib2.URLError, e:
            logger.debug("subtitle url returned error %s", e, exc_info=1)

        try:
            req2 = urllib2.Request(episode.link)
            response2 = urllib2.urlopen(req2)
            result2 = response2.read()
            introduration = result2.split('introduration=')[1].split('&')[0]
        except urllib2.URLError, e:
            logger.debug("subtitle url returned error %s", e, exc_info=1)

        if (introduration):
            sub = self.ted_to_srt ( result,
                                   int(introduration) )
            srtFile = open ( basename + '.srt' , 'w+' )
            srtFile.write ( sub.encode ( "utf-8" ) )
            srtFile.close ()
