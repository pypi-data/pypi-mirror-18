2.0.dev0
========

* Switched from distutils to setuptools.
* Switched from hg to git.
* Minimal changes to pass onslaught, eg PEP8 checks.
* Maintained full unittest coverage (no regressions).

2.0
===

* Bumped the version to be large enough to supercede the old 1.<HG HASH>
  style versions.  New releases will always use PEP 0440 compliant versions.

0.2
===

* Moved the unittests into concon.py; now the sdist has only a single
  python file.  (Also modified them to ensure full code coverage.)

* Removed the automated VERSION generation; now we manually track versions
  with hg branches and tags, and they are PEP 0440 compliant.
