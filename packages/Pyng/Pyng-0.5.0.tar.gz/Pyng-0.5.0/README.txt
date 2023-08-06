====
Pyng
====

Pyng is a collection of Python utility functions I've written over the years,
and that I keep wishing were available everywhere. Sadly, in many cases I've
simply pasted copies of individual functions as needed. But no more!

It's organized as follows:

* **dicts:** dict subsets, dict searching

* **exc:** manipulate exceptions, e.g. reraise, retry

* **genio:** generator-based file I/O, loosely related to Java file streams

* **graph:** filter DAG represented as dict of (key, otherkeys)

* **iters:** generic iterator functionality, akin to itertools

* **relwalk:** os.walk() filtered to produce pathnames relative to the
  starting directory

* **replacefile:** filter a text file in-place

* **toposort:** topological sort of DAG represented as dict of (key, otherkeys)

Please see the individual docstrings for more information.
