#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Extensions script for gPodder to create a CMML file
# containing chapters for Linux Outlaws.
#
# Version 1.0 - Copyright (C) 2011 Eric Le Lay <neric27@wanadoo.fr>
#
# To use, copy it as a Python script into ~/.config/gpodder/extensions/linux_outlaws_cmml.py
#
# Dependencies:
# * This script needs the BeautifulSoup
#    http://www.crummy.com/software/BeautifulSoup/documentation.html
#   In gentoo, it's included in the beautifulsoup package.
# * It also uses xml.etree, which comes with recent
#    python versions (tested with python 2.7)
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
import os

import BeautifulSoup
from BeautifulSoup import BeautifulSoup

import re
from xml.etree import ElementTree as ET

import logging
logger = logging.getLogger(__name__)

_ = gpodder.gettext

__title__ = _('CMML generator')
__description__ = _('Generates CMML-files after downloading a Episode. Supported podcasts: Linux Outlaws, RadioTux')
__author__ = 'Eric Le Lay <neric27@wanadoo.fr>, Bernd Schlapsi <brot@gmx.info>'


LINUX_OUTLAWS = u'Linux Outlaws'
RADIOTUX = u'RadioTux Magazin'

# order of the podcast_list => LINUX_OUTLAWS, RADIOTUX
DefaultConfig = {
    'extensions': {
        'cmml_generator': {
            'podcast_list': [ True, True ],
            'context_menu': True,
        }
    }
}


class gPodderExtension:
    def __init__(self, container):
        self.container = container
        self.choices = [ LINUX_OUTLAWS, RADIOTUX ]

    def on_load(self):
        logger.info('Extension "%s" is being loaded.' % __title__)

    def on_unload(self):
        logger.info('Extension "%s" is being unloaded.' % __title__)

    def on_episode_downloaded(self, episode):
        self._convert_episode(episode)

    def on_episode_delete(self, episode, filename):
        self.delete_cmml_file(filename)

    def _process_episode(self, episode, podcast_title):
        if not episode.channel.title.startswith(podcast_title):
            return False

        if not self.container.config.podcast_list[self.choices.index(podcast_title)]:
            return False

        return True

    def on_episodes_context_menu(self, episodes):
        if not self.container.config.context_menu:
            return None

        episodes = [e for e in episodes if e.file_exists() and
            (self._process_episode(e, LINUX_OUTLAWS) or
             self._process_episode(e, RADIOTUX))]
        if not episodes:
            return None

        return [(self.container.metadata.title, self._convert_episodes)]

    def _convert_episode(self, episode):
        logger.info('create_cmml(%s, %s)' % (episode.title, episode.channel.url))

        html = episode.description
        audio_file = episode.local_filename(False)

        # may have to change that if the feed is renamed...
        if self._process_episode(episode, LINUX_OUTLAWS):
            self.create_cmml_linux_outlaws(html, audio_file)

        elif self._process_episode(episode, RADIOTUX):
            self.create_cmml_radiotux(html, audio_file)

    def _convert_episodes(self, episodes):
        for episode in episodes:
            self._convert_episode(episode)

    def get_cmml_filename(self, audio_file):
        (name, ext) = os.path.splitext(audio_file)
        return '%s.cmml' % name

    def delete_cmml_file(self, filename):
        cmml_file = self.get_cmml_filename(filename)
        if os.path.exists(cmml_file):
            os.remove(cmml_file)

    def create_cmml_linux_outlaws(self, html, audio_file):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        time_re  = text=re.compile("\\d{1,2}(:\\d{2}){2}")
        times = soup.findAll(text=time_re)
        if len(times) > 0:
            to_file = self.get_cmml_filename(audio_file)
            cmml = ET.Element('cmml',attrib={'lang':'en'})
            remove_ws = re.compile('\s+')
            for t in times:
                txt = ''
                for c in t.parent.findAll(text=True):
                    if c is not t: txt += c
                txt = remove_ws.sub(' ', txt)
                txt = txt.strip()
                logger.info("found chapter %s at %s"%(txt,t))
                # totem want's escaped html in the title attribute (not &amp; but &amp;amp;)
                txt = txt.replace('&','&amp;')
                clip = ET.Element('clip')
                clip.set('id',t)
                clip.set( 'start', ('npt:'+t))
                clip.set('title',txt)
                cmml.append(clip)
            ET.ElementTree(cmml).write(to_file,encoding='utf-8')

    def create_cmml_radiotux(self, html, audio_file):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        startzeit = soup.findAll(text='Startzeit')
        if len(startzeit) == 1:
            to_file = self.get_cmml_filename(audio_file)
            cmml = ET.Element('cmml',attrib={'lang':'en'})
            remove_ws = re.compile('\s+')
            for s in startzeit:
                tr = s.parent.parent.parent
                for row in tr.findNextSiblings(name='tr'):
                    txt = ''
                    tds=row.findAll(name='td')
                    t = remove_ws.sub('',tds[1].string)
                    for c in tds[0].findAll(text=True):
                        txt += c
                    txt = remove_ws.sub(' ', txt)
                    txt = txt.strip()
                    logger.info("found chapter %s at %s"%(txt,t))
                    # totem want's escaped html in the title attribute (not &amp; but &amp;amp;)
                    txt = txt.replace('&','&amp;')
                    clip = ET.Element('clip')
                    clip.set('id',t)
                    clip.set( 'start', ('npt:'+t))
                    clip.set('title',txt)
                    cmml.append(clip)
            ET.ElementTree(cmml).write(to_file, encoding='utf-8')
