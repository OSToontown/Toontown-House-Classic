# copyright 1999 McMillan Enterprises, Inc.
# license: use as you please. No warranty.
#
# A subclass of Archive that can be understood
# by a C program. See uplaunch.cpp for unpacking
# from C.
import archive
import struct
import zlib
import strop

class CTOC:
  """A class encapsulating the table of contents of a CArchive.
  
     When written to disk, it is easily read from C."""
  ENTRYSTRUCT = 'iiiibc' #(structlen, dpos, dlen, ulen, flag, typcd) followed by name
  def __init__(self):
    self.data = []
  
  def frombinary(self, s):
    """Decode the binary string into an in memory list.
    
        S is a binary string."""
    entrylen = struct.calcsize(self.ENTRYSTRUCT)
    p = 0
    while p<len(s):
      (slen, dpos, dlen, ulen, flag, typcd) = struct.unpack(self.ENTRYSTRUCT, 
                                                  s[p:p+entrylen]) 
      nmlen = slen - entrylen 
      p = p + entrylen
      (nm,) = struct.unpack(repr(nmlen)+'s', s[p:p+nmlen])
      p = p + nmlen 
      self.data.append((dpos, dlen, ulen, flag, typcd, nm[:-1]))

  def tobinary(self):
    """Return self as a binary string."""
    import string
    entrylen = struct.calcsize(self.ENTRYSTRUCT)
    rslt = []
    for (dpos, dlen, ulen, flag, typcd, nm) in self.data:
      nmlen = len(nm) + 1       # add 1 for a '\0'
      rslt.append(struct.pack(self.ENTRYSTRUCT+repr(nmlen)+'s',
        nmlen+entrylen, dpos, dlen, ulen, flag, typcd, nm+'\0'))
    return string.join(rslt, '')

  def add(self, dpos, dlen, ulen, flag, typcd, nm):
    """Add an entry to the table of contents.
    
       DPOS is data position.
       DLEN is data length.
       ULEN is the uncompressed data len.
       FLAG says if the data is compressed.
       TYPCD is the "type" of the entry (used by the C code)
       NM is the entry's name."""
    self.data.append((dpos, dlen, ulen, flag, typcd, nm))

  def get(self, ndx):
    """return the toc entry (tuple) at index NDX"""
    return self.data[ndx]

  def __getitem__(self, ndx):
    return self.data[ndx]

  def find(self, name):
    """Return the index of the toc entry with name NAME.
    
       Return -1 for failure."""
    for i in range(len(self.data)):
      if self.data[i][-1] == name:
        return i
    return -1

class CArchive(archive.Archive):
  """An Archive subclass that an hold arbitrary data.
  
     Easily handled from C or from Python."""
  MAGIC = 'MEI\014\013\012\013\015'
  HDRLEN = 0
  TOCTMPLT = CTOC
  TRLSTRUCT = '8siii'
  TRLLEN = 20
  LEVEL = 9
  def __init__(self, path=None, start=0, len=0):
    """Constructor.
    
       PATH is path name of file (create an empty CArchive if path is None).
       START is the seekposition within PATH.
       LEN is the length of the CArchive (if 0, then read till EOF). """
    self.len = len
    archive.Archive.__init__(self, path, start)

  def checkmagic(self):
    """Verify that self is a valid CArchive.
    
        Magic signature is at end of the archive."""
    #magic is at EOF; if we're embedded, we need to figure where that is
    if self.len:
      self.lib.seek(self.start+self.len, 0)
    else:
      self.lib.seek(0, 2)
    filelen = self.lib.tell()
    if self.len:
      self.lib.seek(self.start+self.len-self.TRLLEN, 0)
    else:
      self.lib.seek(-self.TRLLEN, 2)
    (magic, totallen, tocpos, toclen) = struct.unpack(self.TRLSTRUCT, 
                                                self.lib.read(self.TRLLEN))
    if magic != self.MAGIC:
      raise RuntimeError, "%s is not a valid %s archive file" \
                % (self.path, self.__class__.__name__)
    self.pkgstart = filelen - totallen
    if self.len:
      if totallen != self.len or self.pkgstart != self.start:
        raise RuntimeError, "Problem with embedded archive in %s" % self.path
    self.tocpos, self.toclen = tocpos, toclen

  def loadtoc(self):
    """Load the table of contents into memory."""
    self.toc = self.TOCTMPLT()
    self.lib.seek(self.pkgstart+self.tocpos)
    tocstr = self.lib.read(self.toclen)
    self.toc.frombinary(tocstr)

  def extract(self, name):
    """Get the contents of an entry.
    
       NAME is an entry name.
       Return the tuple (ispkg, contents).
       For non-Python resoures, ispkg is meaningless (and 0).
       Used by the import mechanism."""
    if type(name) == type(''):
      ndx = self.toc.find(name)
      if ndx == -1:
        return None
    else:
      ndx = name
    (dpos, dlen, ulen, flag, typcd, nm) = self.toc.get(ndx)
    self.lib.seek(self.pkgstart+dpos)
    rslt = self.lib.read(dlen)
    if flag == 1:
      rslt = zlib.decompress(rslt)
    if typcd == 'M':
      return (1, rslt)
    return (0, rslt)

  def contents(self):
    """Return the names of the entries"""
    rslt = []
    for (dpos, dlen, ulen, flag, typcd, nm) in self.toc:
      rslt.append(nm)
    return rslt

  def add(self, entry):
    """Add an ENTRY to the CArchive.
    
       ENTRY must have:
         entry[0] is name (under which it will be saved).
         entry[1] is fullpathname of the file.
         entry[2] is a flag for it's storage format (0==uncompressed,
         1==compressed, 2==Python source format)
         entry[3] is the entry's type code."""
    (nm, pathnm, flag, typcd) = entry[:4]
    if flag == 2:
        s = open(pathnm, 'r').read()
        s = s + '\n\0'
    else:
        s = open(pathnm, 'rb').read()
    ulen = len(s)
    if flag == 1:
      s = zlib.compress(s, self.LEVEL)
    dlen = len(s)
    where = self.lib.tell()
    if typcd == 'm':
      if strop.find(pathnm, '.__init__.py') > -1:
        typcd = 'M'
    self.toc.add(where, dlen, ulen, flag, typcd, nm)
    self.lib.write(s)

  def save_toc(self, tocpos):
    """Save the table of contents to disk."""
    self.tocpos = tocpos
    tocstr = self.toc.tobinary()
    self.toclen = len(tocstr)
    self.lib.write(tocstr)

  def save_trailer(self, tocpos):
    """Save the trailer to disk.
    
       CArchives can be opened from the end - the trailer points
       back to the start. """
    totallen = tocpos + self.toclen + self.TRLLEN
    trl = struct.pack(self.TRLSTRUCT, self.MAGIC, totallen, 
                      tocpos, self.toclen)
    self.lib.write(trl)

  def openEmbedded(self, name):
    """Open a CArchive of name NAME embedded within this CArchive."""
    ndx = self.toc.find(name)
    if ndx == -1:
      raise KeyError, "Member '%s' not found in %s" % (name, self.path)
    (dpos, dlen, ulen, flag, typcd, nm) = self.toc.get(ndx)
    if flag:
      raise ValueError, "Cannot open compressed archive %s in place"
    return CArchive(self.path, self.pkgstart+dpos, dlen)
