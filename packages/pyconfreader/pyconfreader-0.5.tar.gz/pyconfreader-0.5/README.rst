============
pyconfreader
============

Overview
========

A library for reading config files written in Python. Since Python
config files are not sandboxed, you should only read config files that
you trust.

By controlling the globals, locals, and builtins that are passed in to
tthe config file, you can 'pre-populate' the config file with values,
and you can control (to a very limited extent) what Python features
are available to the config file.

Two interfaces are provided:

* A low-level interface for that takes strings.

* A high-level interfaces that supports nested configuration files.

In addition, there is a simple function to convert dicts to
namedtuples.

Typical usage
=============

Low-level interface
-------------------

High-level interface
--------------------

to_namedtuple
-------------
