import os
import sys
import errno
import shutil 
from pathlib import Path

from fuse import FUSE, FuseOSError, Operations

class File_System(Operations):
    def __init__(self, root):
        self.root = root
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        print(path)
        return path
    
    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        file = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        line = "hello world"
        os.write(file , str.encode(line))
        return file



    def getattr(self, path, fh=None):
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    



#sys.argv[2] = mountdir
#sys.argv[1] = root

FUSE( File_System(sys.argv[1]), sys.argv[2], nothreads=True, foreground=True) 