# Installation Instructions #

The present release is dependent on Python.  You must have python installed.

**Unix / Linux / Mac OSX:**
  * Extract the bundle (threadzip.tar.gz, threadzip.tar.tz, or threadzip.zip)
  * Copy _threadzip.py_ and _threadunzip.py_ someplace on your PATH, such as /usr/local/bin
  * If necessary, ensure they have read & execute permissions:
> > `chmod a+rx /usr/local/bin/threadzip.py /usr/local/bin/threadunzip.py`
  * It is assumed your python is located at /usr/bin/python.  If this is not correct, it may be necessary to edit the first line of threadzip.py and threadunzip.py with your favorite text editor, to match the location of python within your system.  You can find the correct python location via _which python_


**Windows:**
  * Since the present implementation requires use of stdin/stdout, it only makes sense to install in something like cygwin.
  * Assuming you're installing in cygwin, just follow the Unix / Linux / Mac OSX instructions.