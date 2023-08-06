# encoding=utf-8

import os
import subprocess


__all__ = ["edit_file", "get_config", "get_user_path", "get_exec_path"]


def edit_file(filename):
    editor = os.getenv("EDITOR", "editor")
    subprocess.Popen([editor, filename]).wait()


def get_config(name, defaults):
    config = get_user_path(name)

    if not os.path.exists(config):
        with open(config, "wb") as f:
            ardj = get_exec_path("ardj")
            data = defaults.format(HOME=os.getenv("HOME"),
                                   DATA=os.path.dirname(config),
                                   BIN=os.path.dirname(ardj))
            f.write(data)
            os.chmod(config, 0640)

        print "Wrote default config to %s, PLEASE EDIT." % config

    return config


def get_user_path(path):
    """
    Returns the name of a user local file.
    Creates the ~/.ardj folder and subfolders if necessary.
    """

    root = os.path.expanduser("~/.ardj")
    path = os.path.join(root, path)

    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    return path


def get_exec_path(command):
    """Returns the full path of an executable, None if not in $PATH."""
    for folder in os.getenv("PATH").split(os.pathsep):
        path = os.path.join(folder, command)
        if os.path.exists(path):
            return path
    return None


def run2(command, pidfile):
    p = subprocess.Popen(command)

    with open(pidfile, "wb") as f:
        f.write(str(p.pid))

    p.wait()
    os.unlink(pidfile)

    return p.returncode


def send_signal(fn, sig):
    if not os.path.exists(fn):
        return False

    with open(fn, "rb") as f:
        pid = int(f.read())

        try:
            os.kill(pid, sig)
            return True
        except OSError, e:
            print "Could not send signal to %s -- error %s" % (fn, e)
            return False
