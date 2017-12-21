import os

def path_to_dirs(path):
    path = os.path.normpath(path)
    ret = path.split(os.sep)
    ret.pop()  # remove file name, only leave dir part
    return ret
