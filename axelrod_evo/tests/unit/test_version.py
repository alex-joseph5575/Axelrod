"""Tests the version number."""

import unittest

import axelrod_evo as axl


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertIsInstance(axl.__version__, str)
