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

import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('Reset etag')
__description__ = _('This hook resets the etag and last modified information for a podcast')
__author__ = 'Bernd Schlapsi <brot@gmx.info>'


DefaultConfig = {
    'extensions': {
        'reset_etag': {
            'domain_list': [u'http://podcast.wdr.de', ],
        }
    }
}


class gPodderExtension:
    def __init__(self, container):
        self.container = container

    def on_load(self):
        logger.info('Extension "%s" is being loaded.' % __title__)

    def on_unload(self):
        logger.info('Extension "%s" is being unloaded.' % __title__)

    def on_podcast_updated(self, podcast):
        if podcast.url.startswith(self.container.config.domain_list):
            podcast.etag = None
            podcast.last_modified = None
            podcast.save()
            logger.info(u'deleted etag and last modified date from podcast: %s' % podcast.title)
