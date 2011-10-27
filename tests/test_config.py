TEST_PODCASTS = {
    # rss feed don't contains all episodes
    # we don't have to download a epiosode for the tests
    'CRETorrent': {'url': 'http://chaosradio.ccc.de/chaosradio_express-latest-bt.rss',
                   'episode': -1 },

    # rss feed contains all episodes from the beginning
    # selected episode should be 'dh-20091121-kurz-005.ogg'
    'DeimHart': {'url': 'http://deimhart.net/index.php?/feeds/categories/3-sendung-ogg.rss',
                 'episode': -12 },

    # rss feed don't contains all episodes
    # we don't have to download a epiosode for the tests
    'LinuxOutlaws': {'url': 'http://feeds.feedburner.com/linuxoutlaws-ogg',
                     'episode': None },

    # rss feed contains all episodes from the beginning
    # selected episode should be 'TFH-001.mp3'
    'TinFoilHat': {'url': 'http://feeds.feedburner.com/TinFoilHat',
                   'episode': -1 },

    # rss feed don't contains all episodes
    # we don't have to download a epiosode for the tests
    'Zpravy': {'url': 'http://www2.rozhlas.cz/podcast/zpravy.php',
               'episode': None },

    # rss feed contains all episodes from the beginning
    # selected episode should be '60 Seconds Episode 9: Vader'
    '60sec': {'url': 'http://www.mevio.com/feeds/60seconds.xml',
              'episode': -9},
}
