#!/usr/bin/python
# -*- coding: utf-8 -*-
from gpodder import api
from gpodder import extensions


def init_test(extension_file, podcast_configs):
    client = api.PodcastClient()
    em = extensions.ExtensionManager(client.core, extension_file)
    podcast_list = []

    for podcast_config, read_filename in podcast_configs:
        podcast = client.get_podcast(podcast_config['url'])
        episode = podcast.get_episodes()[podcast_config['episode']]

        filename = None
        if read_filename:
            filename = episode._episode.local_filename(create=False, check_only=True)

        podcast_list.append(episode)
        podcast_list.append(filename)

    return (client, em, podcast_list)
