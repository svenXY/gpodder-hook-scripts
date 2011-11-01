def check_command(cmd):
    """Check a command line command/program"""
    import shlex
    import subprocess

    # Prior to Python 2.7.3, this module (shlex) did not support Unicode input.
    if isinstance(cmd, unicode):
        cmd = cmd.encode('ascii', 'ignore')
        
    program = shlex.split(cmd)[0]
    try:
        subprocess.Popen(shlex.split('%s --version' % program),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as (errno, errstr):
        raise ImportError('%s: %s' % (errstr, program))


def init_dbus():
    """Initialize the DBus Session, Service and Interface """
    import dbus
    
    bus = dbus.SessionBus()
    notify_service = bus.get_object('org.freedesktop.Notifications', \
            '/org/freedesktop/Notifications')
    notify_interface = dbus.Interface(notify_service, \
            'org.freedesktop.Notifications')
    return notify_interface


def message(notify_interface, hook_name, title, message):
    """Send a notify message via Dbus"""
    notify_interface.Notify('gPodder: %s' % hook_name, 0, '', title,
        message, [], {}, -1
    )
