Imporganizer
============

Organize Python imports according to PEP8.


Installation
============

Imporganizer relies on a patched version of [Rope](https://github.com/kevinjqiu/rope). To install, clone the repo, and install with:

```bash
pip install -r requirements.txt
pip install -e .
```

Usage
=====

```bash
$ organize_import --help
usage: organize_import [-h] [-d] target

positional arguments:
  target

optional arguments:
  -h, --help     show this help message and exit
  -d, --dry-run  If set, only preview the changes
```

When `-d` is passed, a preview is displayed and no real change is committed.

Consider the following highly contrived example python source code:

```python
# foo.py
from foo import bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8 as quux, quux1, quux2, quux3, quux4


bar1 = bar2 = bar3 = bar4 = bar5 = bar6 = bar6 = quux
quux1 = quux2 = quux3 = quux4
```

```bash
organize_import -d foo.py

--- a/sample.py
+++ b/sample.py
@@ -1,4 +1,4 @@
-from foo import bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8 as quux, quux1, quux2, quux3, quux4
+from foo import bar1, bar2, bar3, bar4, bar5, bar6, bar8 as quux, quux1, quux2, quux3, quux4


 bar1 = bar2 = bar3 = bar4 = bar5 = bar6 = bar6 = quux

 --- a/sample.py
 +++ b/sample.py
 @@ -1,4 +1,6 @@
 -from foo import bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8 as quux, quux1, quux2, quux3, quux4
 +from foo import (
 +    bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8 as quux, quux1, quux2,
 +    quux3, quux4)


  bar1 = bar2 = bar3 = bar4 = bar5 = bar6 = bar6 = quux

```

When you're sure of the change, run the command without `-d` flag:

```bash
$ organize_import foo.py
```

and the changes are stored.


License
=======
GPL (GNU General Public License)
