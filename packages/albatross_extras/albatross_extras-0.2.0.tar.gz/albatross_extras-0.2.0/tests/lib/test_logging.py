import unittest
from albatross_extras.lib import logging
import io
import json

class LoggingTest(unittest.TestCase):
    def test_logging(self):
        logger = logging.get_logger('test_logger')
        assert logger.handlers
        assert isinstance(logger.handlers[0].formatter, logging.JsonFormatter)
        stream = io.StringIO()
        logger.handlers[0].stream = stream
        logger.info("Something happened", {
            'some': 'great metadata'
        })
        stream.seek(0)
        result = json.load(stream)
        assert result['ts']
        assert result['msg'] == 'Something happened'
        assert result['some'] == 'great metadata'
        assert result['level'] == 'info'
        assert result['process'] == 'MainProcess'
