import json
import pandas as pd
import os
import numpy as np
import h5py


def create_dict_from_file(filename):
    with open(filename) as f:
        data = f.read()
    js = json.loads(data)
    return js


def load_list_from_file(filename):
    with open(filename) as f:
        return json.load(f)


def build_data_frame_from_h5_directory(directory):
    output = pd.DataFrame()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".h5"):
            output[filename.split(".")[0]] = pd.DataFrame(np.array(h5py.File(os.path.join(directory, filename))["data"])).transpose()
    return output
