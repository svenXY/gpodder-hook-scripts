#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 2011-03-28 written by Jan Lana <lana.jan@gmail.org> 
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The $subj podcast rss does not contain id and pubdate.
# Because of the missing guid gPodder reports always "no new episodes" for the podcast. 
# This extension fix this. The pubdate can be calculated from the audio file url
# and I used the same number as guid.

import gpodder
from gpodder.extensions import ExtensionParent

import re
import time

import logging
logger = logging.getLogger(__name__)


# settings
domain = u'http://.*/media/zpravy/(\d+)-cro1_(\d\d)_(\d\d)_(\d\d)_(\d\d).mp3'

def get_pubdate(episode):
    ts = None

    m = re.search(domain, episode.url)
    if m: 
        ts = time.mktime([int(m.group(1)), int(m.group(2)), int(m.group(3)), 
            int(m.group(4)), int(m.group(5)), 0, -1, -1, -1])
    else:
        ts = episode.pubDate

    return ts
    

class gPodderExtensions(ExtensionParent):
    def __init__(self, **kwargs):
        super(gPodderExtensions, self).__init__(**kwargs)

    def on_episode_save(self, episode):
        ts = get_pubdate(episode)
        episode.pubDate = ts 
        episode.guid = int(ts)
        episode.save()
        episode.db.commit()
        logger.info(u'updated pubDate and guid for podcast: (%s/%s)' % (episode.channel.title, episode.title))
