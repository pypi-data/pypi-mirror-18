# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.trial.unittest import TestCase
from twisted.python.compat import _PY3
from twisted.python.runtime import platform


class NoAPITestCase(TestCase):

    def test_no_api(self):
        """
        Nothing can be star imported from this package.
        """
        import _twisted_platform_support
        self.assertEqual(_twisted_platform_support.__all__, [])

    def test_sendmsg(self):
        """
        Sendmsg can be imported.
        """
        from _twisted_platform_support import _sendmsg
        _sendmsg

    if _PY3 or platform.isWindows():
        test_sendmsg.skip = "Not relevant on this platform."

    def test_raiser(self):
        """
        Raiser can be imported.
        """
        from _twisted_platform_support import _raiser
        _raiser

    def test_portmap(self):
        """
        Sendmsg can be imported.
        """
        from _twisted_platform_support import _portmap
        _portmap

    if _PY3 or platform.isWindows():
        test_portmap.skip = "Not relevant on this platform."

    def test_iocp(self):
        """
        IOCP can be imported.
        """
        from _twisted_platform_support import _iocp
        _iocp

    if not platform.isWindows():
        test_iocp.skip = "Not relevant on this platform."
