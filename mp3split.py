#!/usr/bin/python
# Example hooks script for gPodder.
# To use, copy it as a Python script into ~/.config/gpodder/hooks/mp3split.py
# See the module "gpodder.hooks" for a description of when each hook
# gets called and what the parameters of each hook are.

import gpodder
import subprocess
import os

import logging
logger = logging.getLogger(__name__)

def mp3split(from_file, to_file):
    # http://docs.python.org/library/subprocess.html#subprocess-replacements
    # http://www.doughellmann.com/PyMOTW/subprocess/
    try:
        destination = os.path.dirname(to_file)
        logger.debug("mp3split: destination is %s", destination)
        command = 'mp3splt -ft 10.00 -o "@f_@n" "%s" -d "%s"' % (from_file, destination)
        logger.debug("mp3split: Executing %s", command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # retcode[1] values:
        #  <0: error
        #   0: success, script handle the copy by hand(snif, progress bar is not used)
        stdout, stderr = p.communicate()
        logger.debug("mp3split: Prozess returned %s", p.returncode)
        os.remove(to_file)
        logger.info("mp3split: Original file %s removed", to_file)
    except OSError, e:
        logger.error("mp3split: Execution failed: %s", e)

class gPodderHooks(object):
    def __init__(self):
        pass

    def on_file_copied_to_filesystem(self, mp3playerdevice, from_file, to_file):
        logger.info(u'on_file_copied_to_filesystem(%s, %s)' % (from_file, to_file))
        mp3split(from_file, to_file)
