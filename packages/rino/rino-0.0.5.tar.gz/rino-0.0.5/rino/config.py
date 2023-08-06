import click
import json
import os

default_config = {}

config_file_name = 'rino.json'

def get_config_path():
    dir_path = os.getcwd()
    return os.path.join(dir_path, config_file_name)

def set(key, val):
    config_path = get_config_path()

    if not os.path.exists(config_path):
        with open(config_path, 'w') as outfile:
            outfile.write(json.dumps(default_config))
            return False

    else:
        conf = json.loads(open(config_path, 'r').read())
        conf[key] = val
        with open(config_path, 'w') as outfile:
            outfile.write(json.dumps(conf))
        return True


def get(key):
    config_path = get_config_path()

    if not os.path.exists(config_path):
        return None

    else:
        conf = json.loads(open(config_path, 'r').read())
        if key in conf:
            return conf[key]
        else:
            return False
