from restipy.renderer import SilentUndefined

import jmespath as _jmespath
import yaml as _yaml
import json as _json

def jmespath(data, expr, **kwargs):
    return _jmespath.search(expr, data, kwargs)

def yaml(data, **kwargs):
    if type(data) is SilentUndefined:
        return

    return _yaml.safe_dump(data)

def json(data, **kwargs):
    if type(data) is SilentUndefined:
        return

    return _json.dumps(data, **kwargs)

def from_yaml(data):
    if type(data) is SilentUndefined:
        return

    return _yaml.load(data)

def from_json(data):
    if type(data) is SilentUndefined:
        return

    return _json.loads(data)
