#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 09/2011 Bernd Schlapsi <brot@gmx.info>
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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
# Dependencies:
# * sox (Sound eXchange - http://sox.sourceforge.net/)
#
# The script normalise an audio file after the download

import gpodder
import shlex
import shutil
import subprocess

from gpodder.liblogger import log


class gPodderHooks(object):
    def __init__(self):
        log('audio normaliser extension is initializing.')

    def __get_max_vol(self, audiofile):
        """
        get volume adjustment from the audio file
        """
        cmd = 'sox %(file_in)s -n stat -v' %
            {'file_in': audiofile}

        # sox -v `sox TWID_015.ogg -n stat -v 2>&1` TWID_015.ogg TWID_0
        myprocess = subprocess.Popen(shlex.split(cmd),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = myprocess.communicate()

        if myprocess.returncode > 0:
            log(u'Error reading the volume adjustment from file %s' % audiofile)
        else:
            return stderr.rstrip()    

    def __normalise_file(self, audiofile):
        """
        normalise the audio file
        """
        voladj = self.__get_max_vol(filename)

        cmd = 'sox -v %(voladj)s %(file_in)s %(file_out)s' %
            {'voladj': voladj,
             'file1': filename,
             'file2': filename+".norm"}
        myprocess = subprocess.Popen(shlex.split(cmd),
            filename, filename+".norm"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = myprocess.communicate()

        if myprocess.returncode > 0:
            log(u'Error normalizing the file %s' % audiofile)
        else:
            shutil.move(filename+".norm", filename)

    def on_episode_downloaded(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        # todo: normalise the audio file in a new thread!
            
