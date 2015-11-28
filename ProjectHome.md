# threadzip #
Implemented in python.

Parallel threaded arbitrary compression algorithms.  Currently implemented: zlib (default), and lzma.  Hopefully coming soon:  bzip2, lzo, and "none" for testing purposes.  ;-)

### Which compression algorithms? ###
  * zlib:  like gzip and zip (medium speed, medium strength compression)
  * lzma:  like 7-zip and xz  (slow, strongest compression)
  * bzip2: like bzip2  ;-)  (very slow, fairly strong compression)
  * lzo:   like lzop  (fast, weak compression) (not yet available in threadzip)
  * none:  like none  ;-)  (very fast, zero compression)

### Why python? ###
Python is everywhere.  Compatible with basically every OS on every platform.  It helps develop the code rapidly, and gain widespread usability.  zlib is included by default with every python, and bz2 is included with every python 2.3 and up.  Other algorithms (pylzma and lzo) require python add-ons which are, so far in my experience, available and easily installed on every platform.  They're not distributed with python by default, due to licensing compatibility issues or similar.

### Why threadzip? ###
Here's threadzip compared to major alternatives:
  * xz:  Right now (Jan 2012) xz still has not implemented parallel threading.  They've promised it is high priority and coming soon... for the last few years.  As soon as it DOES come, it's bound to be great.  But I'm tired of waiting.  Apparently I'm not alone, because people created pxz and lxz for the same purpose.  For me, those were not satisfactorily multi-platform available.
  * 7zip (p7zip and variants):  Some implementations are only multithreaded on windows.  There are multithreaded implementations on solaris & linux & osx, but platform compatibility and availability is poor.  If you find what you want using these on the platforms you care about, these are good alternatives.  But I didn't find what I wanted.  Also, the syntax is terrible if you want to use it as an in-line pipe filter.
  * pigz:  Now it's available in solaris (opencsw, blastwave) and linux (epel for rhel5/centos5, and standard apt repositories for debian/ubuntu) and osx (macports).  But it's not available for rhel4/centos4, and it's rather difficult to build if you try.  (I successfully built it on rhel4, so email me and ask for instructions if you want.) _Point of note: python apparently implements threads differently than pigz.  On solaris, pigz performs slightly better than threadzip.  On linux up to the number of cores, pigz slightly outperforms threadzip.  But if you have hyperthreaded processors, then pigz is limited to the number of cores, while threadzip is limited to the number of threads.  Which means threadzip can go around 25% faster than pigz._
  * pbzip2:  It's well made and highly available on any platform.  Problem is bzip2.  It's just so darn slow...  Both the "fast compression" and "best compression" settings of pbzip2 are slower and weaker than the "fast" setting of lzma.  As far as I'm concerned, fast lzma obsoletes bzip2.  But you may like pbzip2 just because it's so highly available.