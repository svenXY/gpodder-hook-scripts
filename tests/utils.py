#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os.path

def get_episode(client, podcast_config, read_filename=False):
    podcast = client.get_podcast(podcast_config['url'])
    episode = podcast.get_episodes()[podcast_config['episode']]

    if read_filename:
        filename = episode._episode.local_filename(create=False, check_only=True)
        return (episode, filename)

    return episode

def get_metadata(extension_module):
    metadata = None

    pathname = os.path.dirname(extension_module.__file__)
    filename = os.path.join(pathname, 'metadata.json')
    with open(filename, 'r') as f:
        metadata = json.load(f)

    return metadata
