# How to use threadzip #

threadzip.py --help<br>
threadunzip.py --help<br>
<br>
<h1>Examples</h1>

Suppose you have a command that generates a datastream on stdout.<br>
<code>tar cf - somedir</code>

Suppose you want to compress it very quickly.  Suppose you are on a machine with a Quad core processor, Xeon (hyperthreaded, for 8 possible threads)<br>
<code>tar cf - somedir | threadzip.py -t 8 --fast &gt; somedir.tar.tz</code>

Suppose you want it compressed as small as possible.  (Typically 2x to 4x longer compression time, and about 2% smaller result.  Your mileage may vary, depending on the data you're compressing.)<br>
<code>tar cf - somedir | threadzip.py -t 8 --best &gt; somedir.tar.tz</code>

Either way, you want to extract it afterward...<br>
<code>cat somedir.tar.tz | threadunzip.py -t 8 | tar tf -</code><br>
or<br>
<code>threadunzip.py -t 8 &lt; somedir.tar.tz | tar tf -</code><br>