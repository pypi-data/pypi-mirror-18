import statsd

_connection = None


def connect_statsd(host='localhost', port=8125, prefix=None):
    global _connection
    _connection = statsd.StatsClient(host=host, port=port, prefix=prefix)


def timer(stat, rate=1):
    return _connection.timer(stat, rate)


def timing(stat, delta, rate=1):
    """Send new timing information. `delta` is in milliseconds.

    :param stat:
    :param delta:
    :param rate:
    :return:
    """
    _connection.timing(stat, delta, rate)


def incr(stat, count=1, rate=1):
    """Increment a stat by `count`."""
    _connection.incr(stat, count, rate)


def gauge(stat, value, rate=1, delta=False):
    """Set a gauge value.

    :param stat:
    :param value:
    :param rate:
    :param delta:
    :return:
    """
    _connection.gauge(stat, value, rate, delta)
