from nestli.common.input_functions import create_dict_from_file
import os
from pathlib import Path


_TEST_DICTIONARY_PATH = os.path.dirname(__file__) / Path("./ressources/test_dictionary.txt")


def test_config_loader():
    mapping = create_dict_from_file(_TEST_DICTIONARY_PATH)
    assert mapping["Hello"] == "Hello"
