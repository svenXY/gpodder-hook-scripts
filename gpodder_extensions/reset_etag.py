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
# This extension resets the etag and last modified information for a podcast.
# This could be necessary if the server "lies" about the last modified state
# This will cause gPodder to reload (and re-parse) the feed every time

import gpodder
from gpodder.extensions import ExtensionParent

import logging
logger = logging.getLogger(__name__)

# Metadata for this extension
__id__ = 'reset_etag'
__name__ = 'Reset etag'
__desc__ = 'This hook resets the etag and last modified information for a podcast'


PARAMS = {
    'domain_list': {
        'desc': 'reset the etag and last modified information for',
        'type': 'combobox',
    }
}

DEFAULT_CONFIG = {
    'extensions': {
        'reset_etag': {
            'domain_list': [u'http://podcast.wdr.de', ],
        }
    }
}


class gPodderExtension(ExtensionParent):
    def __init__(self, config=DEFAULT_CONFIG, **kwargs):
        super(gPodderExtension, self).__init__(config=config, **kwargs)

        self.domain_list = self.config.domain_list

    def on_podcast_updated(self, podcast):
        if podcast.url.startswith(self.domain_list):
            podcast.etag = None
            podcast.last_modified = None
            podcast.save()
            logger.info(u'deleted etag and last modified date from podcast: %s' % podcast.title)
