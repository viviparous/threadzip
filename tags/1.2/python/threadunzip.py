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

class deCompressClass(Thread):
  def __init__ (self,data,compresslib):
    Thread.__init__(self)
    self.data=data
    self.datadecompressed=""
    self.compresslib=compresslib
    self.supportedlibs=["lzma","zlib","bz2","none"]
    if compresslib not in self.supportedlibs:
      assert False, "threadunzip deCompressClass called with unsupported compresslib '"+str(compresslib)+"'"
    if compresslib=="lzma" and not pylzmaAvailable:
      assert False, "threadunzip deCompressClass called with lzma, but pylzma not available"
    if compresslib=="bz2" and not bz2Available:
      assert False, "threadunzip deCompressClass called with bz2, but bz2 not available"

  def getOutput(self):
    return self.datadecompressed

  def run(self):
    if self.compresslib=="lzma":
      self.datadecompressed=pylzma.decompress(self.data)
    elif self.compresslib=="zlib":
      self.datadecompressed=zlib.decompress(self.data)
    elif self.compresslib=="bz2":
      self.datadecompressed=bz2.decompress(self.data)
    elif self.compresslib=="none":
      self.datadecompressed=self.data

def usage():
  print "threadunzip version "+str(VERSION)
  print """

usage: threadunzip [-htb] 
 -h --help        display this message
 -t --threads     specify the number of threads.  Suggested values are 1 to 8.  Default is 2.
"""

def decode32(data):
  # Takes the binary encoded 32-bit string representation of an integer, and returns the integer
  # decode32('\xff\xff\xff\xff') returns 4294967295
  return int(data.encode('hex'),16)

def threadunzip(threads=2):
  decompressors=[]

  # First 10 bytes of any stream identify the threadzip / threadunzip version number, to accomodate for smarter packing in future.
  data=sys.stdin.read(10)
  if data=="%10s"%('1.0'):
    compresslib="zlib"
    streamversion="1.0"
  elif data=="%10s"%('1.1lzma'):
    compresslib="lzma"
    streamversion="1.1"
  elif data=="%10s"%('1.2lzma'):
    compresslib="lzma"
    streamversion="1.2"
  elif data=="%10s"%('1.1zlib'):
    compresslib="zlib"
    streamversion="1.1"
  elif data=="%10s"%('1.2zlib'):
    compresslib="zlib"
    streamversion="1.2"
  elif data=="%10s"%('1.2bz2'):
    compresslib="bz2"
    streamversion="1.2"
  elif data=="%10s"%('1.2none'):
    compresslib="none"
    streamversion="1.2"
  else:
    sys.stderr.write("Error: this version of threadunzip doesn't recognize this data stream.\n")
    sys.exit(1)

  while True:
    if streamversion=="1.0":
      blocksize=sys.stdin.read(10)
      if blocksize == "":
        break
      blocksize=int(blocksize)
    elif streamversion in ("1.1", "1.2"):
      blocksize=sys.stdin.read(4)
      if blocksize == "":
        break
      blocksize=decode32(blocksize)
    data = sys.stdin.read(blocksize)
    if len(data) != blocksize:
      assert False, "data stream must be corrupt. expected "+str(blocksize)+" bytes, and got "+str(len(data))
    present=deCompressClass(data,compresslib)
    decompressors.append(present)
    present.start()
    if len(decompressors)==threads:
      present=decompressors.pop(0)
      present.join()
      sys.stdout.write(present.getOutput())
  while len(decompressors)>0:
    present=decompressors.pop(0)
    present.join()
    sys.stdout.write(present.getOutput())

  return 0

def main():
  # default threads is 2
  threads = 2

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "threads="])
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
    else:
      assert False, "unhandled option"

  try:
    threads=int(threads)
  except:
    assert False, "Threads specified must be integer"

  return threadunzip(threads)

if __name__ == "__main__":
  sys.exit(main())
