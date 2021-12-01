import os
import sys
from fuse import FUSE ,Operations

class file_system(Operations):
    def __init__(self,root):
        self.root = root
    ###############################################
    def getattr(self, path, fh=None):   #fh=none is written in source code only  
        full_path = self._full_path(path)
        #print(full_path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                    'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        #print(path)
        return path

    ###############################################

    def create(self, path, mode, fi=None):     #fi = none is written in source code only  
        path = self._full_path(path)
        #print(path)
        file = os.open(path , os.O_RDWR | os.O_CREAT, mode)
        line = "hello world"
        os.write(file , str.encode(line))   # byte object is needed not strign hence encode is used
        return file
    
    def mkdir(self, path, mode):
        #print(path)
        path = self._full_path(path)
        #print(path)
        os.mkdir(path,mode)
    def rmdir(self, path):
        path = self._full_path(path)
        os.removedirs(path)

    def readdir(self, path, fh):
        path = self._full_path(path)
        l = os.listdir(path)  # it doesn't include . & ..
        l.append('.')
        l.append('..')
        return l

    # def fsync(self, path, datasync, fh): # it pushesh the buffer to disk
    #     path = self._full_path(path)
    #     file = os.open(path , os.O_RDWR | os.O_CREAT)
    #     if(datasync != 0):
    #         os.fsync(file)
    #     else: 
    #         os.sync(file)
    # def symlink(self, target, source): #symbolic link are like shorcuts it is a pointer to target file
    #     target = self._full_path(target)
    #     print(target)
    #     print(source)
    #     os.symlink(source, target) 

    # def link(self, target, source):   # creates a hard link
    #     target = self._full_path(target)
    #     source = self._full_path(source)
    #     os.link(source, target)

root = sys.argv[1]
mount = sys.argv[2]
# print(root)
FUSE(file_system(root) , mount ,nothreads=True, foreground=True)