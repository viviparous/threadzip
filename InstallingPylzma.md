# Installing pylzma #

homepage:
http://www.joachim-bauch.de/projects/pylzma/

download page:
http://pypi.python.org/pypi/pylzma

download file:
http://pypi.python.org/packages/source/p/pylzma/pylzma-0.4.4.tar.gz#md5=a2be89cb2288174ebb18bec68fa559fb

To install:
> First, install python-dev

> Note:  Does not work on python2.3 due to absence of hashlib sha256.
> Works on python2.6

```
    cd /tmp
    tar xzf pylzma-0.4.4.tar.gz
    cd pylzma-0.4.4/
```

> And now:
```
    python setup.py build
```

> It should have created a directory like this:  build/lib.linux-x86\_64-2.6<br>
<blockquote>cd into that directory.</blockquote>

<blockquote>Byte-compile py7zlib:<br>
Launch python<br>
import py7zlib</blockquote>

<blockquote>Figure out your python path:  launch python.  import sys.  sys.path<br>
Copy these files into the site-packages directory.  Something like this:<br>
<pre><code>    chmod 644 py7zlib.py<br>
    chmod 644 py7zlib.pyc<br>
    chmod 755 pylzma.so<br>
    cp -p py7zlib.pyc py7zlib.py pylzma.so /usr/local/lib/python2.6/site-packages<br>
</code></pre></blockquote>

<blockquote>Now, whenever somebody launches python, they can "import pylzma" and/or "import py7zlib"