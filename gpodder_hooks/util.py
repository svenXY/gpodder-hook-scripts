import shlex
import subprocess

def check_command(cmd):
    program = shlex.split(cmd)[0]

    try:
        subprocess.Popen(shlex.split('%s --version' % program), stdout=subprocess.PIPE)
    except Exception as (errno, errstr):
        raise ImportError('%s: %s' % (errstr, program))
