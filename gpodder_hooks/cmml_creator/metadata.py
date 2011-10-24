metadata = {
    "name": "CMML generator",
    "desc": "Generates CMML-files after downloading a Episode. The supported podcasts are listed in the preferences",
    "authors": [ 'Eric Le Lay <neric27@wanadoo.fr>', 'Bernd Schlapsi <brot@gmx.info>' ],
    "url": 'https://github.com/gpodder/gpodder-hook-scripts',
}

params = {
    "podcast_list": {
        "desc": "Supported podcasts:",
        "value": [ (True, 'Linux Outlaws'), (True, 'RadioTux Magazin') ],
        "gui": {
            "type": "multichoice-list"
        }
    }
}
