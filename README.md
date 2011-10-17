# Hook

A hook script is a .py file which contains a class with the name 'gPodderHooks'.

Additionally every hook script needs a config file with some metadata. This metadata is necessary to integrate the a hook script in the gPoder GUI.

## How to create a config file 

The hook-script repository contains a python file with some usefull functions to help with the creation of the hook-script config file.

    >>> import hook_util
    >>>
    >>> params = hook_util.create_config_param(
    ...     name='bittorrent_cmd',
    ...     value='qbittorrent %s',
    ...     desc='Defines the command line bittorrent program',
    ...     param_type='str',
    ...     override_allowed=True
    ... )
    >>>
    >>> hook_util.create_config_file(
    ...     hook_script='bittorrent.py',
    ...     name='Bittorrent downloader',
    ...     desc='Downloads the file if the file from the podcast ends with .torrent',
    ...     params=(params,))
