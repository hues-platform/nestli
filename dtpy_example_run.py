from dtpy.manager.Manager import Manager

example_manager = Manager("example_config.yml")

example_manager.build_simulation()
example_manager.run()