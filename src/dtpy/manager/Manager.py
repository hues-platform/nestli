import mosaik

from dtpy.common.input_functions import create_dict_from_file
from dtpy.manager import MOSAIK_CONFIG
from dtpy.common.config_loader import load_config, convert_entries_to_abs_pathes


class Manager:
    def __init__(self, config_file) -> None:
        self.cfg = load_config(config_file)
        convert_entries_to_abs_pathes(self.cfg, config_file)
        self.mosaik_cfg = MOSAIK_CONFIG

    def build_simulation(self):
        self.world = mosaik.World(
            self.mosaik_cfg, time_resolution=self.cfg["RESOLUTION"]
        )
        self.simulators = self.initialize_simulators()
        self.models = self.initialize_models()
        self.connect_signals()

    def run(self):
        self.world.run(until=self.cfg["END"], print_progress=True)

    def initialize_simulators(self):
        simulators = {}
        for sim, attributes in self.cfg["SIMULATORS"].items():
            if attributes["TYPE"] == "FMU":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    work_dir=attributes["PATH"],
                    fmu_name=attributes["NAME"],
                    model_name=attributes["NAME"],
                    instance_name=attributes["TYPE"] + "_Instance",
                    stop_time=self.cfg["END"],
                )
            elif attributes["TYPE"] == "CSV":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    sim_start=self.cfg["START"],
                    datafile=attributes["PATH"],
                )
            else:
                simulators[attributes["NAME"]] = self.world.start(attributes["TYPE"])
        return simulators

    def initialize_models(self):
        models = {}
        for sim, attributes in self.cfg["SIMULATORS"].items():
            if attributes["TYPE"] == "FMU":
                models[attributes["NAME"]] = self.simulators[
                    attributes["NAME"]
                ].FMU_Instance.create(1)
            elif attributes["TYPE"] == "CSV":
                models[attributes["NAME"]] = self.simulators[
                    attributes["NAME"]
                ].Data.create(1)
            else:
                models[attributes["NAME"]] = self.simulators[
                    attributes["NAME"]
                ].Monitor()
        return models

    def connect_signals(self):
        for mapping, attributes in self.cfg["MAPPINGS"].items():
            signal_source = self.models[attributes["FROM"]][0]
            signal_drain = self.models[attributes["TO"]]
            if not attributes["TO"] == "COLLECTOR":
                signal_drain = signal_drain[0]
            mapping_dict = create_dict_from_file(attributes["PATH"])

            cyclic_dependency = (
                attributes["FROM"] == "UMAR" and attributes["TO"] == "PREPROCESS"
            )
            if cyclic_dependency:
                for key, value in mapping_dict.items():
                    self.world.connect(
                        signal_source,
                        signal_drain,
                        (value, key),
                        time_shifted=True,
                        initial_data={value: 0.0},
                    )
            else:
                for key, value in mapping_dict.items():
                    self.world.connect(signal_source, signal_drain, (value, key))
