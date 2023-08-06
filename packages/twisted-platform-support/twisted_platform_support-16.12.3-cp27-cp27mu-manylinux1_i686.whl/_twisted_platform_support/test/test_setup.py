# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for the setup file.
"""

import os

from setuptools.dist import Distribution
from twisted.trial.unittest import TestCase

from _twisted_platform_support import _setup
from _twisted_platform_support._setup import (
    ConditionalExtension, getSetupArgs
)


class SetupTests(TestCase):
    """
    Tests for L{getSetupArgs}.
    """

    def test_conditionalExtensions(self):
        """
        Will return the arguments with a custom build_ext which knows how to
        check whether they should be built.
        """
        good_ext = ConditionalExtension("whatever", ["whatever.c"],
                                        condition=lambda b: True)
        bad_ext = ConditionalExtension("whatever", ["whatever.c"],
                                       condition=lambda b: False)

        args = getSetupArgs(extensions=[good_ext, bad_ext])

        # ext_modules should be set even though it's not used.  See comment
        # in getSetupArgs
        self.assertEqual(args["ext_modules"], [good_ext, bad_ext])
        cmdclass = args["cmdclass"]
        build_ext = cmdclass["build_ext"]
        builder = build_ext(Distribution())
        builder.prepare_extensions()
        self.assertEqual(builder.extensions, [good_ext])

    def test_win32Definition(self):
        """
        When building on Windows NT, the WIN32 macro will be defined as 1 on
        the extensions.
        """
        ext = ConditionalExtension("whatever", ["whatever.c"],
                                   define_macros=[("whatever", 2)])

        args = getSetupArgs(extensions=[ext])

        builder = args["cmdclass"]["build_ext"](Distribution())
        self.patch(os, "name", "nt")
        builder.prepare_extensions()
        self.assertEqual(ext.define_macros, [("whatever", 2), ("WIN32", 1)])


class FakeModule(object):
    """
    A fake module, suitable for dependency injection in testing.
    """
    def __init__(self, attrs):
        """
        Initializes a fake module.

        @param attrs: The attrs that will be accessible on the module.
        @type attrs: C{dict} of C{str} (Python names) to objects
        """
        self._attrs = attrs

    def __getattr__(self, name):
        """
        Gets an attribute of this fake module from its attrs.

        @raise AttributeError: When the requested attribute is missing.
        """
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError()


fakeCPythonPlatform = FakeModule({"python_implementation": lambda: "CPython"})
fakeOtherPlatform = FakeModule({"python_implementation": lambda: "lvhpy"})


class WithPlatformTests(TestCase):
    """
    Tests for L{_checkCPython} when used with a (fake) C{platform} module.
    """
    def test_cpython(self):
        """
        L{_checkCPython} returns C{True} when C{platform.python_implementation}
        says we're running on CPython.
        """
        self.assertTrue(_setup._checkCPython(platform=fakeCPythonPlatform))

    def test_other(self):
        """
        L{_checkCPython} returns C{False} when
        C{platform.python_implementation} says we're not running on CPython.
        """
        self.assertFalse(_setup._checkCPython(platform=fakeOtherPlatform))
