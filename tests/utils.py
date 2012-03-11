#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from gpodder import core
from gpodder import extensions


def init_test(extension_file, podcast_configs):
    os.environ['GPODDER_EXTENSIONS'] = extension_file
    gpo_core = core.Core()
    podcast_list = []

    for podcast_config, read_filename in podcast_configs:
        podcast = gpo_core.model.load_podcast(podcast_config['url'])
        episode = podcast.get_all_episodes()[podcast_config['episode']]

        filename = None
        if read_filename:
            filename = episode.local_filename(create=False, check_only=True)

        podcast_list.append(episode)
        podcast_list.append(filename)

    return (gpo_core, podcast_list)
