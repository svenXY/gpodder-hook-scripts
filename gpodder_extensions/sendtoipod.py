# -*- coding: utf-8 -*-
# Send files to iPod using libgpod
# Copyright (c) 2012-10-15 Paul Ortyl <ortylp@3miasto.net.pl>
# Licensed under the same terms as gPodder itself
'''
Extention to gPodder for sending files to iPod from context menu
'''

# missing features:
# * refresh of UI/model after episode gets deleted
# * user feedback
# * automatic conversion to file format supported by iPod (assume mp3)


import os
import gpodder
import logging
logger = logging.getLogger(__name__)

_are_libraries_available = True
try:
    import gpod
    import eyeD3
except Exception, e:
    _are_libraries_available = False

_ = gpodder.gettext

__title__ = _('Send file(s) to iPod from context menu')
__description__ = _('Send file(s) to iPod from context menu')
__authors__ = 'Paul Ortyl <ortylp@3miasto.net.pl>'

DefaultConfig = {
    'context_menu': True,  # Show item in context menu
}

class gPodderExtension:
    def __init__(self, container):

        self.container = container
        self.config = self.container.config
        # use default evironment variable as defined for gtkpod
        self.ipod_mount = os.getenv('IPOD_MOUNTPOINT')

    def on_episode_downloaded(self, episode):
        True

    def on_episodes_context_menu(self, episodes):
        if not _are_libraries_available:
            return None

        if not self.config.context_menu:
            return None

        if 'audio/mpeg' not in [e.mime_type for e in episodes
            if e.mime_type is not None and e.file_exists()]:
            return None

        if self._find_ipod():
            return [(_('Send To iPod'), self._send_to_ipod)]
        else:
            return None

    def _send_to_ipod(self, episodes):
        itdb = gpod.itdb_parse(self.ipod_mount, None)
        if not itdb:
            logger.error('Could not open iPod database at %s' % self.ipod_mount)
            self.ipod_mount = None
            return

        itdb_modified = False

        for episode in episodes:
            filename = episode.local_filename(create=False)
            if filename is None:
              return

            extension = os.path.splitext(filename)[1]

            if episode.file_type() != 'audio':
              return

            if extension.lower() != '.mp3':
              return

            modified = self.send_file_to_ipod(itdb, filename)
            itdb_modified |= modified
            if modified:
              episode.mark_old()
              episode.delete_from_disk()

        if itdb_modified:
            gpod.itdb_write(itdb, None)
            gpod.itdb_free(itdb)

    def send_file_to_ipod(self, itdb, fname):
        if eyeD3.isMp3File(fname):
            logger.debug("Copying file '%s' to iPod..." % fname)
            podcasts = gpod.itdb_playlist_podcasts(itdb)
            af = eyeD3.Mp3AudioFile(fname, eyeD3.ID3_ANY_VERSION)
            tag = af.getTag()
            track = gpod.itdb_track_new()
            track.visible = 1
            track.filetype = "mp3"
            track.ipod_path = fname
            track.tracklen = af.getPlayTime() * 1000
            track.album = str(tag.getAlbum())
            track.artist = str(tag.getArtist())
            track.title = str(tag.getTitle())
            track.genre = str(tag.getGenre())
            track.playcount = 0
            gpod.itdb_track_add(itdb, track, -1)
            gpod.itdb_playlist_add_track(podcasts, track, -1)
            is_copied = gpod.itdb_cp_track_to_ipod(track, fname, None)
            if is_copied:
                logger.info("File '%s' has been successfully copied to iPod" % fname)
            else:
                logger.error("File '%s' could not be copied to iPod" % fname)
            return is_copied
        else:
            logger.error("File format for %s is not mp3, skipping" % fname)
            return False

    def _find_ipod(self):
        '''Try to autodetect mount point of ipod and set the internal path to ipod'''
        if self.ipod_mount: return True

        # find first vfat mounted directory with iPod_Control subdir
        try:
            with open('/proc/mounts', 'r') as f:
                for line in f.readlines():
                    tokens = line.split(' ', 4)
                    if tokens and 'vfat' == tokens[2] and os.path.exists(tokens[1] + '/iPod_Control'):
                        self.ipod_mount = tokens[1]
                        return True
        except IOError as e: pass  # in case we are not on standard linux

        return False




