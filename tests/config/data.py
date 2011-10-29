import os

config_dir = os.path.dirname(os.path.abspath(__file__))

TEST_PODCASTS = {
    # we don't have to download a epiosode for the tests
    'CRETorrent': {#'url': 'http://chaosradio.ccc.de/chaosradio_express-latest-bt.rss',
                   'url': 'file://%s/cre-torrent.rss' % config_dir,
                   'episode': -1 },

    # selected episode should be 'dh-20091121-kurz-005.ogg'
    'DeimHart': {#'url': 'http://deimhart.net/index.php?/feeds/categories/3-sendung-ogg.rss',
                 'url': 'file://%s/DeimHart.rss' % config_dir,
                 'episode': -12 },

    # we don't have to download a epiosode for the tests
    'LinuxOutlaws': {#'url': 'http://feeds.feedburner.com/linuxoutlaws-ogg',
                     'url': 'file://%s/linuxoutlaws-ogg.rss' % config_dir,
                     'episode': None },

    # selected episode should be 'TFH-001.mp3'
    'TinFoilHat': {#'url': 'http://feeds.feedburner.com/TinFoilHat',
                   'url': 'file://%s/TinFoilHat.rss' % config_dir,
                   'episode': -1 },

    # we don't have to download a epiosode for the tests
    'Zpravy': {#'url': 'http://www2.rozhlas.cz/podcast/zpravy.php',
               'url': 'file://%s/zpravy.rss' % config_dir,
               'episode': None },

    # selected episode should be 'TED: Matt Cutts: Try something new for 30 days - Matt Cutts (2011)'
    'TEDTalks': {'url': 'file://%s/tedtalks_video.rss' % config_dir,
                 'episode': -31},
}
