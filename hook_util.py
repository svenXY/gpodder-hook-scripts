#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 10/2011 Bernd Schlapsi <brot@gmx.info>
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
import json
import os.path

def chk_external_dependencies(config):
	pass

def chk_config(configfile):
    try:
        config = json.load(open(configfile))
        if not config.has_key('hook-script'):
            print("Config file '%s' misses 'hook-script' definition" % configfile)
        else:
            if not os.path.exists(config['hook-script']):
                print("Couldn't find hook-script '%s'" % config['hook-script'])
        return config
    except ValueError:
        print("Config file '%s' isn't a valid json file" % configfile)
