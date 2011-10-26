metadata = {
    "name": 'Convert to MP4',
    "desc": 'Converts Files to MP4 to use on Rockbox devices',
    "authors": [ 'Guy Sheffer <guysoft at gmail.com>', 'Thomas Perl <thp@gpodder.org>', 'Bernd Schlapsi <brot@gmx.info>' ],
    "url": 'https://github.com/gpodder/gpodder-hook-scripts',
}

params = {
    "device_width": {
        "desc": 'Device width',
        "value": 224.0,
        "type": 'spinbutton'
    },
    "device_height": {
        "desc": 'Device height',
        "value": 176.0,
        "type": 'spinbutton'
    },
    "ffmpeg_options": {
        "desc": 'ffmpeg options',
        "value": '-vcodec mpeg2video -b 500k -ab 192k -ac 2 -ar 44100 -acodec libmp3lame',
        "type": 'textitem'
    }
}
