import unittest
from albatross_extras.lib import config

class ConfigTest(unittest.TestCase):
    def test_config(self):
        config.load_config('tests/config/test.yaml')
        assert config.get('base') == 1
        assert config.get('test') == 2
        assert config.get('nested.key1') == 'did-overwrite'
        assert config.get('nested.key2') == 'stays-nested'
        assert config.get('nested.key3') is None
