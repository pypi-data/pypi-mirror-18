pyramid_bpython_curses
======================

`bpython <http://bpython-interpreter.org/>`_ bindings for
`Pyramid <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_ in a curses variant (for Windows).

Installation
------------

::

  $ pip install pyramid_bpython_curses

Usage
-----

Ensure the shell is available::

  $ pshell --list-shells
  Available shells:
    bpython_curses
    python

The shell should be auto-selected when running ``pshell``::

  $ pshell development.ini

However, if there are multiple shells you can also be explicit::

  $ pshell -p bpython_curses development.ini
