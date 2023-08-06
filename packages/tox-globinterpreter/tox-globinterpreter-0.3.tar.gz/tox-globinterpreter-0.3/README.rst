
Usage:
======

- ``tox --scan`` shows previously found name to executable path mappings.
- ``tox --scan PATTERN1 PATTERN2`` searches the patterns for python executables
  and stores paths found in that way for future use by ``tox``

This allows you to easily specify multiple python executables for ``tox`` to
use. Without the need for permanently or temporarily adding their paths to
your ``$PATH``, which does
have unacceptable side effects in all cases, except for direct commandline
invocation of ``tox`` via an alias (as you can guess not my typical usage).

On Windows the executables can be found via the registry. Therefore specifying
PATTERNS to find executables is unnecessary and relatively cumbersome.
``tox --scan registry`` will scan the registry for executable paths and
add provide these for future runs. This finally allows it to run ``tox`` on
windows without the need to clutter ``C:\`` with python installs.


Installation
============

Since tox 2.0 the plugin mechanism based on ``pluggy`` is included in ``tox``.
You can just do:

    pip install tox_globinterpreter

If you install ``pytest`` (``pip install pytest``) to test this module
itself, and you use the bash shell, make sure you rehash bash (``hash -r`` or
re-activate the virtual environment.


Default tox interpreter finding behaviour
=========================================

Non-Windows
-----------

``tox`` searches through the ``$PATH`` specified paths for python executables
(ToDo: check).

For many Linux distributions the system python (and more recently pythons, as
both 2.7.x and 3.4.X are used by system utilities as Linux distributions
slowly moves to Python3) cannot be replaced by a newer micro version without
a lot of hassle. These newer micro versions should be installed in some
"other" directory e.g. ``/opt/python/2.7.9``. Its ``bin`` directory cannot
be added to the normal PATH during startup as this will break some
system programs relying on the older python micro version (and its additionally
installed libraries).

This directory can temporarily be added to each invocation of ``tox`` by
making an alias for ``tox``, but that doesn't work if ``tox`` is called from
a Makefile. And aliasing ``make`` to include that path can break invocations
of system utilities from the same Makefile.


Windows
-------

On Windows ``tox`` looks for installations in ``C:\\python?.?`` and
determines the version based on the directory name (ToDo: check).

This doesn't work when you have the python interpreters installed in the non
default location, e.g. necessary when you want 64 and 32 bit versions
installed, or when you have them installed under the more correct
``C:\Program Files\`` or similar directory.

tox_globinterpreter plugin extensions
=====================================

Non-Windows
-----------

``tox_globinterpreter`` adds one commandline option to ``tox``: ``--scan``.
If invoked with arguments, these arguments should be a pattern, or list of
patterns that will be ``globb``-ed and ``shlex``-ed to form a mapping
of base names to paths to python binaries that is then stored globally
per user for future
usage (under $XDG_CONFIG_HOME/tox, defaulting to ~/.config/tox).
E.g.::

  tox --scan '/opt/python/2.?/bin/python?.?' ../../../opt/python/pypy*/bin/pypy

(please note that only the second argument is not expanded by the shell, the
first is quoted and expanded by ``tox_globinterpreter``).

If ``tox --scan`` is invoked without arguments, then the currently
stored mapping (base name to executable)is printed out. E.g.::

  python2.7 /opt/python/2.7/bin/python2.7
  pypy /opt/python/pypy-2.5.0/bin/pypy

(if the same base name is found multiple times, the **first** one in the list
is used).

If the environment variable ``TOX_INTERPRETER_GLOBS`` is set this
will cause the python binaries to be searched for using the patterns
specified by that environment variable (expanded and searched every time).

If ``TOX_INTERPRETER_GLOBS`` is set it prevents the use of the `--scan`-ned
list, and either of them is set, the normal search through PATH is not
done.

During ``--scan``-ning the base name (``py27``) to be used in the ``envlist``
in ``tox.ini``, is determined based on the name of the binary if this
includes a version number (``python2.7``). if the binary equals ``python``
the base name (including version) is determined by invoking the interpreter.
When expanding ``TOX_INTERPRETER_GLOBS``, this invocation to determine
version information is currently considered too expensive.

Windows
-------

``tox_globinterpreter`` adds commandline options to ``tox``, the
primary one of which is: ``--scan``.

On windows you should specify
``--scan c:/python/*/python.exe c:/pypy*/*/*/pyp.exe`` first to create a
mapping of base names to paths. This doesn't get them from the registry
as the registry is incomplete (only one of both 64 and 32 bit version
of a particular CPython is registered, pypy is not registered at all).

If ``tox --scan`` is invoked without arguments, then the currently
stored mapping is printed out. E.g.::

  python2.7 c:\python\2.7\python2.7.exe
  python2.7 c:\python\2.7-32\python2.7.exe

If you have 64 and 32 bit versions installed select the `-32` version by
doing::

  tox -r --32

(This might be supported in ``tox`` itself at some point, currently you cannot
specify ``py27-32`` as the ``32`` part is never handed to
``tox_get_python_executable``)


History
=======

I originally implemented the possibility to specify the list of interpreters
as a patch for ``tox`` for which I put in a PR that lingered for two years
(with repeated updates) until I was asked to update it (once more, but this
time by the author of tox). Shortly after the plugin interface was provided
and this plugin for ``tox`` replaces the earlier PR requests ``tox``.
