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

    def formatTime(self, time):
        milliseconds = 0
        seconds = ((time / 1000) % 60)
        minutes = ((time / 1000) / 60)
        hours = (((time / 1000) / 60) / 60)
        formatedTime = str ( hours ) + ':' + str (minutes) + ':' + str ( seconds ) + ',' + str ( milliseconds )
        return formatedTime

    def convertTEDSubtitlesToSRTSubtitles(self, jsonString, introDuration):
        jsonObject = json.loads( jsonString )

        srtContent = ''
        captionIndex = 1

        for caption in jsonObject['captions'] :
            startTime = str ( self.formatTime ( introDuration + caption['startTime'] ) )
            endTime = str ( self.formatTime ( introDuration + caption['startTime'] + caption['duration'] ) )

            srtContent += ( str ( captionIndex ) + os.linesep )
            srtContent += ( startTime + ' --> ' + endTime + os.linesep )
            srtContent += ( caption['content'] + os.linesep )
            srtContent += os.linesep

            captionIndex = captionIndex + 1
        return srtContent

    def on_episode_downloaded(self, episode):
        current_filename = episode.local_filename(create=False)
        basename, ext = os.path.splitext(current_filename)
        talkId = episode.guid.split(':')[1]
        try:
            int(talkId)
        except ValueError:
            return
        sub_url = 'http://www.ted.com/talks/subtitles/id/' + str(talkId) + '/lang/eng'
        logger.debug('subtitle url: %s',sub_url)
        logger.debug('episode url: %s',episode.link)

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
            introDuration = result2.split('introDuration=')[1].split('&')[0]
        except urllib2.URLError, e:
            logger.debug("subtitle url returned error %s", e, exc_info=1)

        if (introDuration):
            sub = self.convertTEDSubtitlesToSRTSubtitles ( result,
                                                          int(introDuration) )
            srtFile = open ( basename + '.srt' , 'w+' )
            srtFile.write ( sub.encode ( "utf-8" ) )
            srtFile.close ()
