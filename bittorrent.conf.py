config = {
    "hook_script": "bittorrent.py",
    "name": "Bittorrent downloader",
    "desc": "Downloads the file if the file from the podcast ends with .torrent",
    "params": {
        "bittorrent_cmd": {
            "desc": "Defines the command line bittorrent program",
            "value": "qbittorrent %s",
            "default_value": "qbittorrent %s",
            "gui": {
                "override_allowed": True,
                "type": "str"
            }
        }
    }
}

