import unittest
from albatross_extras.lib import util
from datetime import timezone


class UtilTest(unittest.TestCase):
    def test_util(self):
        assert isinstance(util.uuid4(), str)
        assert util.utcnow().tzinfo == timezone.utc
