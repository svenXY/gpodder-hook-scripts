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
