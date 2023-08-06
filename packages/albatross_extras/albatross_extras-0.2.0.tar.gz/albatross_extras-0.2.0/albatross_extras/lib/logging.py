import logging
import sys
import traceback
import json
import datetime


def get_logger(name):
    logger = logging.getLogger(name)
    logger.parent = None
    log_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = JsonFormatter()
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    return logger


def _default_json_handler(obj):
    if isinstance(obj, (datetime.date, datetime.time)):
        return obj.isoformat()
    elif isinstance(obj, Exception):
        return "%s: %s" % (type(obj).__name__, obj.message)
    elif isinstance(obj, (int, float, bool)):
        return obj
    return str(obj)


class JsonFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as json strings.
    extra values will be formatted as str() if nor supported by
    json default encoder
    """
    def format(self, record):
        data = (record.args or {}).copy()
        data['ts'] = datetime.datetime.utcnow()
        data['level'] = record.levelname.lower()
        data['process'] = record.processName
        if isinstance(record.msg, str):
            data['msg'] = record.msg
        else:
            data['msg'] = _default_json_handler(record.msg)
            if isinstance(record.msg, Exception):
                data['traceback'] = traceback.format_exc()

        return json.dumps(data, default=_default_json_handler, separators=(',', ':'))
