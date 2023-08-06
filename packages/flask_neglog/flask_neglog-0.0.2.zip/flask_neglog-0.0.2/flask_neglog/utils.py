import errno
import os


def ensure_dir(path):
    """os.makedirs without EEXIST."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def ensure_file_dir(path):
    parent = os.path.dirname(path)
    ensure_dir(parent)
