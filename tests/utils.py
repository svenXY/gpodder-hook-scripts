#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os.path
import re

def get_episode(client, podcast_config, read_filename=False):
    podcast = client.get_podcast(podcast_config['url'])
    episode = podcast.get_episodes()[podcast_config['episode']]

    if read_filename:
        filename = episode._episode.local_filename(create=False, check_only=True)
        return (episode, filename)

    return episode

def get_metadata(extension_module):
    filename, ext = os.path.splitext(extension_module.__file__)
    extension_py = open(filename + '.py').read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", extension_py))

    return metadata
