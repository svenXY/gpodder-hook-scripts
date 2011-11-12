#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 03/2011 based on bug report https://bugs.gpodder.org/show_bug.cgi?id=1294
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
# This hook resets the etag and last modified information for a podcast.
# This could be necessary if the server "lies" about the last modified state
# This will cause gPodder to reload (and re-parse) the feed every time 

import gpodder
from gpodder.hooks import HookParent

import logging
logger = logging.getLogger(__name__)


DEFAULT_PARAMS = { 
    "domain_list": {
        "desc": "reset the etag and last modified information for",
        "value": [u'http://podcast.wdr.de', ],
        "type": "combobox",
    }   
}

## settings
domains = (u'http://podcast.wdr.de', )


class gPodderHooks(HookParent):
    def __init__(self, metadata, params=DEFAULT_PARAMS):
        super(gPodderHooks, self).__init__(params=params)

        self.domain_list = params['domain_list']['value']

    def on_podcast_updated(self, podcast):
        if podcast.url.startswith(self.domain_list):
            podcast.etag = None
            podcast.last_modified = None
            podcast.save()
            logger.info(u'deleted etag and last modified date from podcast: %s' % podcast.title)
