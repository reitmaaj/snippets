""" export configuration and defaults from JSON files """

import os
import sys
import json
import types
import pathlib


def _object_hook(value):
    return types.SimpleNamespace(**value)

def _resolve_default_conf_path():
    return pathlib.Path(__file__).parent / 'default.conf.json'

def _resolve_conf_path():
    for conf_path in (os.getenv('CONF_PATH'), 'conf.json',): # resolution order
        if not conf_path is None:
            return pathlib.Path(conf_path)

def _create_conf(default_conf_path, conf_path):
    with (default_conf_path.open() as df, conf_path.open() as cf):
        default_conf = json.load(df, object_hook=_object_hook)
        conf = json.load(cf, object_hook=_object_hook)
        return types.SimpleNamespace(**{**default_conf.__dict__,
                                        **conf.__dict__,})

sys.modules[__name__] = _create_conf(_resolve_default_conf_path(),
                                     _resolve_conf_path())
