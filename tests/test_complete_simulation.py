from nestli.manager.Manager import Manager
import os
from pathlib import Path
import pytest
import sys


_TEST_CFG_PATH = os.path.dirname(__file__) / Path("./resources/test_config.yml")


@pytest.mark.skipif(sys.platform != "win32", reason="E+ not running on git ci")
def test_simulation():
    example_manager = Manager(_TEST_CFG_PATH)

    example_manager.build_simulation()
    example_manager.run()
