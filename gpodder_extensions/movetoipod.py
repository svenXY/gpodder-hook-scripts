# -*- coding: utf-8 -*-
# Send files to iPod using libgpod
# Copyright (c) 2013-01-22 Paul Ortyl <ortylp@3miasto.net.pl>
# Licensed under the same terms as gPodder itself
'''
Extention to gPodder for sending (moving) files to iPod from context menu
'''

# HOWTO HOWTO HOWTO HOWTO HOWTO
# * copy the file 'movetoipod.py' to share/gpodder/extensions/.
# * make sure gpod and mutagen libraries (and python wrappers) are installed
#   to install it on Ubuntu suffices:
#      sudo apt-get install python-gpod python-mutagen
# * restart gpodder ( gpodder -v to see diagnostics)
# * enable this extension in preferences/extentions
# * restart gpodder again (just to make sure all hooks fired at gpodder startup)
# * connect iPod (make sure it is mounted, and mounted as vfat, use "mount" command to check it)
# * new entry "Move to iPod" should appear in the context menu of episodes
# * use it for transferring _audio_ files to the end of Podcast playlist on the iPod
#
# Other info::
#   The UI is blocked while the files are transferred.
#   For more info start gpodder with '-v' to see detailed logging.
#   This script has been tested (and is dogfooded) with iPod Shuffle 2G (and a little on 4G)
#   Video files are ignored/skipped (there is no use for them on iPod Shuffle)
#   For audio file formats other than mp3 'avconv' is used, (sudo apt-get install libav-tools)

# missing features:
# * user feedback (at the moment only via logging to console, start gpodder with '-v' option)
# * BUG: UI does not get updates after enabling of this extension, restart of gpodder is necessary
# * BUG: UI does not get updated until the complete batch of files gets processed
# missing goodies, ideas:
# * extract audio from video tracks and send it to iPod
# * two menu entries, one for audio and one for video
# * stop file transfers as soon as free space in iPod gets below predefined threshold

import os
import gpodder
import logging
import subprocess
logger = logging.getLogger(__name__)

_are_libraries_available = True
try:
    import gpod
except Exception, e:
    logger.error('gpod library is missing')
    _are_libraries_available = False

try:
    from mutagen.oggvorbis import OggVorbis
    from mutagen.mp3       import MP3
except Exception, e:
    logger.error('mutagen library is missing')
    _are_libraries_available = False

_ = gpodder.gettext

__title__ = _('Move file(s) to iPod from context menu')
__description__ = _('Move file(s) to iPod from context menu')
__authors__ = 'Paul Ortyl <ortylp@3miasto.net.pl>'
__only_for__ = 'gtk'

DefaultConfig = {
    'context_menu': True,  # Show item in context menu
}


def _convert_to_mp3(filename):
    '''Convert file to temporary mp3
        @param filename: filename of the audio file to be converted
        @return: file name of the temporary file in mp3 format, this file should be deleted afterwards
    '''
    fnameMP3 = filename + '.mp3'
    # remove file so that avconv wont get confused
    if (os.path.exists(fnameMP3)): os.unlink(fnameMP3)
    cmd = ['avconv', '-i', filename, fnameMP3]
    avconv = subprocess.Popen(cmd)
    avconv.communicate()

    if 0 == avconv.returncode:
        return fnameMP3
    else:
        os.unlink(fnameMP3)
        return None

def _get_MP3_tags(filename):
    tagsMP3 = MP3(filename)
    tags = {}
    tags['album'] = tagsMP3.get('TALB', '')
    tags['title'] = tagsMP3.get('TIT2', '')
    tags['artist'] = tagsMP3.get('TPE1', '')
    tags['length'] = tagsMP3.info.length * 1000
    tags['genre'] = tagsMP3.get('TCON', '')
    return tags

def _get_OGG_tags(filename):
    tagsOGG = OggVorbis(filename)
    tags = {}
    tags['album'] = ''.join(tagsOGG.get('album', ['']))
    tags['title'] = ''.join(tagsOGG.get('title', ['']))
    tags['artist'] = ''.join(tagsOGG.get('artist', ['']))
    tags['length'] = tagsOGG.info.length * 1000
    tags['genre'] = 'Podcast'
    return tags

def _fix_tags(tags, episode, basename):
    if not tags.has_key('album') or not tags['album']:
        tags['album'] = episode.parent.title
    if not tags.has_key('title') or not tags['title'] or basename == tags['title']:
        tags['title'] = episode.title
    if not tags.has_key('title') or not tags['title']:
        tags['title'] = basename
    if not tags.has_key('genre') or not tags['genre']:
        tags['genre'] = 'Podcast'
    if not tags.has_key('artist') or not tags['artist']:
        tags['artist'] = ''
    if not tags.has_key('length') or not tags['length']:
        tags['length'] = 0  # FIXME: get length from converted mp3 file!

    return tags

class gPodderExtension:
    def __init__(self, container):

        self.container = container
        self.config = self.container.config
        self.ui = None
        # use default environment variable as defined for gtkpod
        self.ipod_mount = os.getenv('IPOD_MOUNTPOINT')

    def on_ui_object_available(self, name, ui_object):
        '''Get reference onto UI object, needed for triggering UI update after move'''
        if name == 'gpodder-gtk': self.ui = ui_object

    def on_episodes_context_menu(self, episodes):
        if not _are_libraries_available:
            return None

        if not self.config.context_menu:
            return None

        audio = 'audio' in [e.file_type() for e in episodes
            if e.mime_type is not None and e.file_exists()]

        if not audio:
            return None

        if self._find_ipod():
            return [(_('Move To iPod'), self._send_to_ipod)]
        else:
            return None

    def _send_to_ipod(self, episodes):
        itdb = gpod.itdb_parse(self.ipod_mount, None)
        if not itdb:
            logger.error('Could not open iPod database at %s' % self.ipod_mount)
            self.ipod_mount = None
            return

        for episode in reversed(episodes):
            filename = episode.local_filename(create=False)
            if filename is None:
                continue

            extension = episode.extension()
            basename = os.path.splitext(os.path.basename(filename))[0]

            if episode.file_type() != 'audio':
                continue

            sent = False  # set to true if file transfer was successful
            # for each file type:
            # 1. extract (id3) tags
            # 2. fix missing tags using available information
            # 3. convert file to mp3 if necessary
            # 4. send to iPod
            if extension.lower() == '.mp3':
                tags = _get_MP3_tags(filename)
                sent = self.send_file_to_ipod(itdb, filename, _fix_tags(tags, episode, basename))
            elif extension.lower() == '.ogg':
                tmpname = _convert_to_mp3(filename)
                if tmpname:
                    sent = self.send_file_to_ipod(itdb, tmpname, _get_OGG_tags(filename))
                    os.unlink(tmpname);
            elif extension.lower() == '.wav':
                tags = {}
                tmpname = _convert_to_mp3(filename)
                if tmpname:
                    sent = self.send_file_to_ipod(itdb, tmpname, _fix_tags({}, episode, basename))
                    os.unlink(tmpname);
            else:
                continue

            if sent:
                episode.mark_old()
                logger.info("File '%s' has been marked 'old'" % filename)
                if not episode.archive:
                  episode.delete_from_disk()
                  logger.info("File '%s' has been deleted from gPodder database and file system"
                              % filename)
                # update UI
                if self.ui:
                  self.ui.episode_list_status_changed([episode])

        gpod.itdb_free(itdb)

    def send_file_to_ipod(self, itdb, fname, tags):
        if not os.path.exists(fname):
            logger.error("File '%s' does not exist" % fname)
            return False

        logger.debug("Copying file '%s' to iPod..." % fname)
        podcasts = gpod.itdb_playlist_podcasts(itdb)
        track = gpod.itdb_track_new()
        track.visible = 1
        track.filetype = "mp3"
        track.ipod_path = fname
        track.album = str(tags['album'])
        track.artist = str(tags['artist'])
        track.title = str(tags['title'])
        track.genre = str(tags['genre'])
        track.tracklen = tags['length']
        track.playcount = 0
        gpod.itdb_track_add(itdb, track, -1)
        gpod.itdb_playlist_add_track(podcasts, track, -1)
        is_copied = gpod.itdb_cp_track_to_ipod(track, fname, None)
        if is_copied:
            logger.info("File '%s' has been successfully copied to iPod" % fname)
        else:
            # roll back
            logger.error("File '%s' could not be copied to iPod" % fname)
            gpod.itdb_playlist_remove_track(podcasts, track)
            gpod.itdb_track_remove(track)
        track = None
        gpod.itdb_write(itdb, None)
        return is_copied

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
