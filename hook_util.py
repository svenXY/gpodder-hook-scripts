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
import types
import json
import os.path

def create_config_param(name, value, desc, param_type, override_allowed):
    if name is None:
        raise ValueError("You have to provide the parameter name")

    if value is None:
        raise ValueError("You have to provide a default value for the parameter")

    if desc is None:
        raise ValueError("You have to provide a description for the parameter")

    if param_type not in ('str'):
        raise ValueError("The param-type must be 'str'")

    if not isinstance(override_allowed, bool):
        raise ValueError("Parameter 'override_allowed' must be True or False")

    return { name:
        { "value": value,
          "default_value": value,
          "desc": desc,
          "gui": {
              "type": param_type,
              "override_allowed": override_allowed
          }
        }
    }


def create_config_file(hook_script, name, desc, params):
    if not os.path.exists(hook_script):
        raise ValueError("Couldn't find hook-script '%s'" % hook_script)

    if name is None:
        raise ValueError("You have to provide a descriptive name")

    if desc is None:
        raise ValueError("You have to provide some description")

    if not isinstance(params, types.ListType) and not isinstance(params, types.TupleType):
        raise ValueError("The 'params' Parameter must be a Tuple or a List")

    filename = os.path.basename(hook_script) 
    basename, ext = os.path.splitext(filename)

    config = { "hook_script": filename,
        "name": name,
        "desc": desc,
        "enabled": False,
        "params": params
    }

    with open("%s.conf" % basename, 'w') as f:
        json.dump(config, f, indent=4)


def chk_config(configfile):
    try:
        config = json.load(open(configfile))
        if not config.has_key('hook_script'):
            print("Config file '%s' misses 'hook_script' definition" % configfile)
        else:
            if not os.path.exists(config['hook_script']):
                print("Couldn't find hook-script '%s'" % config['hook_script'])
        return config
    except ValueError:
        print("Config file '%s' isn't a valid json file" % configfile)


if __name__ == '__main__':
    # create a config file parameter
    params = hook_util.create_config_param(
        name='bittorrent_cmd',
        value='qbittorrent %s',
        desc='Defines the command line bittorrent program',
        param_type='str',
        override_allowed=True
    )
    
    # create/write a config file
    hook_util.create_config_file(
        hook_script='bittorrent.py',
        name='Bittorrent downloader',
        desc='Downloads the file if the file from the podcast ends with .torrent',
        params=(params,)
    )
