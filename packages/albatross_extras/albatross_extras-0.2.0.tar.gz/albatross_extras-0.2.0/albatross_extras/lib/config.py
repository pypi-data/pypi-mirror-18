"""Easily load configuration from yaml files.

Example usage:

    from albatross_extras.lib import config
    config.load_config('development.yaml')
    config.get('aws.access_secret')

Example file hierarchy:

--- config/base.yaml

aws:
    access_key: 123

--- config/development.yaml

extends:
    - config/base.yaml

aws:
    access_secret: 456

"""
from copy import deepcopy
import yaml

CONFIG = None


def deep_merge(base, overwrite):
    result = deepcopy(base)
    for k, v in overwrite.items():
        if k in result and isinstance(result[k], dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def _load_config(fname):
    with open(fname) as f:
        data = yaml.load(f)
    base_data = {}
    for fname in data.get('extends', []):
        to_merge = _load_config(fname)
        base_data = deep_merge(base_data, to_merge)
    return deep_merge(base_data, data)


def load_config(fname):
    global CONFIG
    CONFIG = _load_config(fname)


def get(key, default=None):
    keys = key.split('.')
    d = CONFIG
    for k in keys:
        d = d.get(k)
    return default if d is None else d
