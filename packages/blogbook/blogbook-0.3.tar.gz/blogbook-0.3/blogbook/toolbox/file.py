# -*- coding: utf-8 -*-

import errno
import os
import shutil


def is_empty(directory):
    return not os.listdir(directory)


def force_mkdir(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


def silently_remove(path):
    try:
        os.remove(path)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def silently_rmdir(path):
    try:
        os.rmdir(path)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def parentdir(path):
    return os.path.abspath(os.path.join(path, os.pardir))
