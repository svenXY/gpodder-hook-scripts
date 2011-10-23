metadata = {
    "name": "Bittorrent downloader",
    "desc": "Downloads the file if the file from the podcast ends with .torrent",
    "authors": [ 'Thomas Perl <thp@gpodder.org>', 'Bernd Schlapsi <brot@gmx.info>' ],
    "url": 'https://github.com/gpodder/gpodder-hook-scripts',
    "params":  {
        "bittorrent_cmd": {
            "desc": "Defines the command line bittorrent program:",
            "gui": {
                "override_allowed": True,
                "type": "str"
            }   
        }   
    }   
}
