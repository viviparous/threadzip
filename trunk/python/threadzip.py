#!/usr/bin/python
# 
# Copyright 2011 Edward Harvey
# 
# This file is part of threadzip.
# 
# Threadzip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Threadzip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Threadzip.  If not, see <http://www.gnu.org/licenses/>.
#

from threading import Thread
import sys, zlib, getopt

VERSION="1.2"

try:
  import pylzma
  pylzmaAvailable=True
except:
  pylzmaAvailable=False

try:
  import bz2
  bz2Available=True
except:
  bz2Available=False

class CompressClass(Thread):
  def __init__ (self,data,compressionlevel=5,compresslib="zlib"):
    Thread.__init__(self)
    self.exception=False
    self.data=data
    self.datacompressed=""
    self.compressionlevel=compressionlevel
    self.compresslib=compresslib
    self.supportedlibs=["lzma","zlib","bz2","none"]
    if compresslib not in self.supportedlibs:
      assert False, "threadzip CompressClass called with unsupported compresslib '"+str(compresslib)+"'"
    if compresslib=="lzma" and not pylzmaAvailable:
      assert False, "threadzip CompressClass called with lzma, but pylzma not available"
    if compresslib=="bz2" and not bz2Available:
      assert False, "threadzip CompressClass called with bz2, but bz2 not available"

  def getException(self):
    return self.exception

  def getSupportedLibs(self):
    return self.supportedlibs

  def getOutput(self):
    return self.datacompressed

  def run(self):
    try:
      if self.compresslib=="lzma":
        self.datacompressed=pylzma.compress(self.data,algorithm=self.compressionlevel)
      elif self.compresslib=="zlib":
        self.datacompressed=zlib.compress(self.data,self.compressionlevel)
      elif self.compresslib=="bz2":
        self.datacompressed=bz2.compress(self.data,self.compressionlevel)
      elif self.compresslib=="none":
        self.datacompressed=self.data
    except:
      self.exception=True
      raise

def usage():
  print "threadzip version "+str(VERSION)
  print """

usage: threadzip [-htb] 
 -h --help        display this message
 -t --threads     specify the number of threads.  Default is 2.
 -b --blocksize   number of bytes to give to each thread to compress.  Default is 5M
                  could also append suffixes:
                  k  1,000
                  K  1,024
                  m  1,000,000
                  M  1,048,576
 --lzma           use lzma (like 7-zip or xz) instead of zlib (like gzip/pigz) 
 --bz2            use bz2 (like bzip2 or pbzip2) instead of zlib (like gzip/pigz)
 -#               compressionlevel

                  if using zlib: integer from 1 to 9.  1 is fastest, 9 is best compression
                  default is 5

                  if using lzma: integer from 0 to 2.  0 is fastest, 2 is best compression
                  default is 2

                  if using bz2: integer from 1 to 9.  1 is fastest, 9 is best compression
                  default is 9

 --fast           fastest compression. synonymous to -1 if zlib, -0 if lzma, -1 if bz2
 --best           best compression. synonymous to -9 if zlib, -2 if lzma, -9 if bz2
"""

def encode32(x):
  # Takes an integer in the range 0 to 2**32 and returns the binary encoded 32-bit string representation
  # encode32(4294967295) returns '\xff\xff\xff\xff'
  return hex(x)[2:].zfill(8).decode('hex')

def threadzip(threads=2, blocksize=5*2**20, compressionlevel=5, compresslib="zlib"):
  compressors=[]

  # Exception will be raised if compresslib is not in list of supported compresslibs
  # Creating an instance of the class, and letting it be immediately destroyed afterward.
  CompressClass("",compressionlevel=1,compresslib=compresslib)

  # First 10 bytes of any stream identify the threadzip / threadunzip version number, to accomodate for smarter packing in future.
  if compresslib=="lzma":
    sys.stdout.write( '%10s' % ('1.2lzma') )
  elif compresslib=="zlib":
    sys.stdout.write( '%10s' % ('1.2zlib') )
  elif compresslib=="bz2":
    sys.stdout.write( '%10s' % ('1.2bz2') )
  elif compresslib=="none":
    sys.stdout.write( '%10s' % ('1.2none') )

  data=""
  keepGoing=True
  while keepGoing:
    data = sys.stdin.read(blocksize)
    if data == "":
      keepGoing=False
    present=CompressClass(data,compressionlevel,compresslib)
    compressors.append(present)
    present.start()
    if len(compressors)==threads:
      present=compressors.pop(0)
      present.join()
      if present.getException():
        assert False, "child thread raised exception. abort"
      output=present.getOutput()
      if len(output)>=2**32:
        assert False, "a compressed chunk exceeded "+str(2**32)+" bytes. use a smaller blocksize or higher compression level"
      else:
        sys.stdout.write( encode32(len(output)) + output )
  while len(compressors)>0:
    present=compressors.pop(0)
    present.join()
    output=present.getOutput()
    if len(output)>2**32:
      assert False, "a compressed chunk exceeded "+str(2**32)+" bytes. use a smaller blocksize or higher compression level"
    else:
      sys.stdout.write( encode32(len(output)) + output )

  return 0

def main():
  # default threads is 2
  threads = 2
  # default blocksize is 5M
  blocksize=5*2**20
  compressionlevel=None
  fast=False
  best=False
  # default compression is zlib
  compresslib="zlib"

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:b:0123456789", ["help", "threads=", "blocksize=", "fast", "best", "lzma", "bz2", "none"])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-t", "--threads"):
      threads = a
    elif o in ("-b", "--blocksize"):
      blocksize = a
    elif o in ("-0"):
      compressionlevel=0
    elif o in ("-1"):
      compressionlevel=1
    elif o in ("-2"):
      compressionlevel=2
    elif o in ("-3"):
      compressionlevel=3
    elif o in ("-4"):
      compressionlevel=4
    elif o in ("-5"):
      compressionlevel=5
    elif o in ("-6"):
      compressionlevel=6
    elif o in ("-7"):
      compressionlevel=7
    elif o in ("-8"):
      compressionlevel=8
    elif o in ("-9"):
      compressionlevel=9
    elif o in ("--fast"):
      fast=True
    elif o in ("--best"):
      best=True
    elif o in ("--lzma"):
      compresslib="lzma"
    elif o in ("--bz2"):
      compresslib="bz2"
    elif o in ("--none"):
      compresslib="none"
    else:
      assert False, "unhandled option"

  try:
    threads=int(threads)
  except:
    assert False, "Threads specified must be integer"

  try:
    int(blocksize)
  except:
    # They didn't specify a purely integer blocksize.
    # Maybe they specified something with a suffix, of k or m or g
    try:
      intpart = int(blocksize[0:len(blocksize)-1])
      suffix = blocksize[len(blocksize)-1]
      if suffix == "k":
        blocksize=intpart*10**3
      elif suffix == "K":
        blocksize=intpart*2**10
      elif suffix == "m":
        blocksize=intpart*10**6
      elif suffix == "M":
        blocksize=intpart*2**20
      elif suffix == "g":
        blocksize=intpart*10**9
      elif suffix == "G":
        blocksize=intpart*2**30
      else:
        assert False, "Blocksize has no suffix; must be integer number of bytes, or have a suffix: k, K, m, M, g, G"
    except:
      assert False, "Blocksize has no int; must be integer number of bytes, or have a suffix: k, K, m, M, g, G"

  blocksize = int(blocksize)

  if fast==True:
    if compresslib=="lzma":
      compressionlevel=0
    elif compresslib=="zlib":
      compressionlevel=1
    elif compresslib=="bz2":
      compressionlevel=1
    elif compresslib=="none":
      compressionlevel=1
  elif best==True:
    if compresslib=="lzma":
      compressionlevel=2
    elif compresslib=="zlib":
      compressionlevel=9
    elif compresslib=="bz2":
      compressionlevel=9
    elif compresslib=="none":
      compressionlevel=9

  if compressionlevel==None:
    if compresslib=="lzma":
      compressionlevel=2
    elif compresslib=="zlib":
      compressionlevel=5
    elif compresslib=="bz2":
      compressionlevel=9
    elif compresslib=="none":
      compressionlevel=5

  return threadzip(threads,blocksize,compressionlevel,compresslib)

if __name__ == "__main__":
  sys.exit(main())
