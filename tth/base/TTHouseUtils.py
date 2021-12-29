import fnmatch

from panda3d.core import *

vfs = VirtualFileSystem.getGlobalPtr()

def scanVFS(root='.', files=None):
    """
    Returns a set of all of the files in the Virtual File System.
    """
    if files is None:
        files = []
    scan = vfs.scanDirectory(Filename(root))
    if not scan:
        return []
    for filepath in scan:
        filepath = str(filepath)
        if vfs.isDirectory(Filename(filepath)):
            if not scanVFS(filepath, files):
                files.append(filepath)
        else:
            files.append(filepath)
    return set(map(lambda f: f[f.find('phase_'):], files))

def globVFS(pattern, root='.'):
    """
    Returns a list of files from the Virtual File System that match the
    provided fnmatch pattern.
    """
    pattern = pattern.replace('\\','/')
    return filter(lambda f: fnmatch.fnmatch(f, pattern), scanVFS(root))

rgb2p = lambda r, g, b: (r/255.0, g/255.0, b/255.0)