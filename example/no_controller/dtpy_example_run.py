from dtpy.manager.Manager import Manager
from dtpy.common.config_loader import abs_path

import os


def __abs_path(path):
    return abs_path(path, os.path.abspath(__file__))


example_manager = Manager(__abs_path("example_config.yml"))

example_manager.build_simulation()
example_manager.run()
