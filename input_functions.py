import json
import os
import pandas as pd

def create_dict_from_file(filename):
    with open(filename) as f:
        data = f.read()
    js = json.loads(data)
    return js


def read_csv_files_in_folder(folder_path):
    output = pd.DataFrame()
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            output[filename.split(".")[0]] = pd.read_csv(os.path.join(folder_path, filename))
    return output