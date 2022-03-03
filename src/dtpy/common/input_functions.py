import json


def create_dict_from_file(filename):
    with open(filename) as f:
        data = f.read()
    js = json.loads(data)
    return js
