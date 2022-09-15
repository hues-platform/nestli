import json
from typing import Dict, List
from urllib.request import urlopen
import pandas as pd
import os
import numpy as np
import h5py
from io import BytesIO
from zipfile import ZipFile


def create_dict_from_file(filename) -> Dict:
    """Reads a json file and returns Dictionary of contents."""
    with open(filename) as f:
        data = f.read()
    js = json.loads(data)
    return js


def load_list_from_file(filename) -> List:
    """Reads a json file and returns List of contents."""
    with open(filename) as f:
        return json.load(f)


def build_data_frame_from_h5_directory(directory) -> pd.DataFrame:
    """Reads all h5 files in a directory to a Dataframe and returns it."""
    output = pd.DataFrame()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".h5"):
            output[filename.split(".")[0]] = pd.DataFrame(np.array(h5py.File(os.path.join(directory, filename))["data"])).transpose()
    return output


def download_and_unzip(url, extract_to):
    """Loads a Zip file from a url and extracts it."""
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)
