from dtpy.common.config_loader import load_config
import os
from pathlib import Path


_TEST_CFG_PATH = os.path.dirname(__file__) / Path("./ressources/test_config.yml")


def test_config_loader():
    config = load_config(_TEST_CFG_PATH)
    assert config["RESOLUTION"] == 60
