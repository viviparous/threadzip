#!/usr/bin/python
# 
# Copyright 2009 Edward Harvey
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

class CompressClass(Thread):
  def __init__ (self,data,compressionlevel=9):
    Thread.__init__(self)
    self.data=data
    self.datacompressed=""
    self.compressionlevel=compressionlevel

  def getOutput(self):
    return self.datacompressed

  def run(self):
    self.datacompressed=zlib.compress(self.data,self.compressionlevel)

def usage():
  print """
usage: threadzip [-htb] 
 -h --help        display this message
 -t --threads     specify the number of threads.  Suggested values are 1 to 8.  Default is 2.
 -b --blocksize   number of bytes to give to each thread to compress.  Default is 5M
                  could also append suffixes:
                  k  1,000
                  K  1,024
                  m  1,000,000
                  M  1,048,576
                  g  1,000,000,000
                  G  1,073,741,824
 -#               compressionlevel, integer from 1 to 9.  1 is fastest, 9 is best compression
                  default is 9 (best)
 --fast           synonymous to -1  fastest compression
 --best           synonymous to -9  best compression
"""

def threadzip(threads=2, blocksize=5*2**20, compressionlevel=9):
  compressors=[]

  # First 10 bytes of any stream identify the threadzip / threadunzip version number, to accomodate for smarter packing in future.
  sys.stdout.write( '%10s' % ('1.0') )

  data=""
  keepGoing=True
  while keepGoing:
    data = sys.stdin.read(blocksize)
    if data == "":
      keepGoing=False
    present=CompressClass(data,compressionlevel)
    compressors.append(present)
    present.start()
    if len(compressors)==threads:
      present=compressors.pop(0)
      present.join()
      output=present.getOutput()
      if len(output)>9999999999:
        assert False, "a compressed chunk exceeded 9999999999 bytes. use a smaller blocksize or higher compression level"
      else:
        sys.stdout.write( '%10d%s' % (len(output),output) )
  while len(compressors)>0:
    present=compressors.pop(0)
    present.join()
    output=present.getOutput()
    if len(output)>9999999999:
      assert False, "a compressed chunk exceeded 9999999999 bytes. use a smaller blocksize or higher compression level"
    else:
      sys.stdout.write( '%10d%s' % (len(output),output) )

  return 0

def main():
  # default threads is 2
  threads = 2
  # default blocksize is 5M
  blocksize=5*2**20
  # default compressionlevel is 9
  compressionlevel=9

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:b:123456789", ["help", "threads=", "blocksize=", "fast", "best"])
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
    elif o in ("-1", "--fast"):
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
    elif o in ("-9", "--best"):
      compressionlevel=9
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

  return threadzip(threads,blocksize,compressionlevel)

if __name__ == "__main__":
  sys.exit(main())
