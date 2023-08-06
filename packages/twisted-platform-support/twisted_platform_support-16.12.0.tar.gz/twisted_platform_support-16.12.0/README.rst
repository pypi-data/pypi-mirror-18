Twisted Platform Support
========================

What is this?
-------------

Code that allows Twisted to work on platforms where Python does not have complete bindings for everything Twisted needs.
For example, this includes:

- I/O Completion Ports for Windows ("IOCPReactor")
- ``sendmsg`` support for Python 2
- other C used in testing.


How do I get it?
----------------

Just ``pip install twisted[platform_support]``.
