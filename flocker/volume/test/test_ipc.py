# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Unit tests for IPC."""

from __future__ import absolute_import

from unittest import TestCase as PyTestCase

from zope.interface.verify import verifyObject

from .._ipc import INode, FakeNode
from ...testtools import assertNoFDsLeaked


def make_inode_tests(fixture):
    """
    Create a TestCase for ``INode``.

    :param fixture: A fixture that returns a :class:`INode` provider.
    """
    class INodeTests(PyTestCase):
        """Tests for :class:`INode` implementors.

        May be functional tests depending on the fixture.
        """
        def test_interface(self):
            """
            The tested object provides :class:`INode`.
            """
            node = fixture(self)
            self.assertTrue(verifyObject(INode, node))

        def test_no_fd_leakage(self):
            """No file descriptors are leaked by ``run()``."""
            node = fixture(self)
            with assertNoFDsLeaked(self):
                with node.run([b"cat"]):
                    pass

        def test_exceptions_pass_through(self):
            """Exceptions raised in the context manager are not swallowed."""
            node = fixture(self)
            with self.assertRaises(RuntimeError):
                with node.run([b"cat"]):
                    raise RuntimeError()

        def test_no_fd_leakage_exceptions(self):
            """No file descriptors are leaked by ``run()`` if exception is
            raised within the context manager."""
            node = fixture(self)
            with assertNoFDsLeaked(self):
                try:
                    with node.run([b"cat"]):
                        raise RuntimeError()
                except RuntimeError:
                    pass

        def test_writeable(self):
            """The returned object is writeable."""
            node = fixture(self)
            with node.run([b"cat"]) as writer:
                writer.write(b"hello")
                writer.write(b"there")

    return INodeTests


class FakeINodeTests(make_inode_tests(lambda t: FakeNode())):
    """``INode`` tests for ``FakeNode``."""
