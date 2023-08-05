import os


__all__ = ['get_home', 'cmd_exists']


def get_home():
    # This function should be robust
    # First, let us try with expanduser
    try:
        homedir = os.path.expanduser("~")
    except ImportError:
        # This may happen.
        pass
    else:
        if os.path.isdir(homedir):
            return homedir
    # Then, with getenv
    for this in ('HOME', 'USERPROFILE', 'TMP'):
        # getenv is same as os.environ.get
        homedir = os.environ.get(this)
        if homedir is not None and os.path.isdir(homedir):
            return homedir


def cmd_exists(cmd):
    try:
        import subprocess
        # for unix/max only
        result = subprocess.call("type " + cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result == 0:
            return True
        else:
            return False
    except Exception:
        # If subprocess is not found, we assume it exists.
        # This choice ensure that if it fails, we keep going.
        return True

def in_ipynb():
    """Checks if we are in an ipython notebook

    :return: True if in an ipython notebook otherwise returns False

    """
    try:
        cfg = get_ipython().config
        if 'parent_appname' in cfg['IPKernelApp'].keys() and \
                cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return True
        else:
            return False
    except NameError:
        return False
