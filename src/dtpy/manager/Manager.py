import mosaik

from dtpy.common.input_functions import create_dict_from_file, build_data_frame_from_h5_directory, load_list_from_file
from dtpy.manager import MOSAIK_CONFIG
from dtpy.common.config_loader import load_config, convert_entries_to_abs_pathes
from dtpy.common.time_converter import get_seconds_from_date


class Manager:
    def __init__(self, config_file) -> None:
        self.cfg = load_config(config_file)
        convert_entries_to_abs_pathes(self.cfg, config_file)
        self.mosaik_cfg = MOSAIK_CONFIG

    def build_simulation(self):
        self.world = mosaik.World(self.mosaik_cfg, time_resolution=self.cfg["RESOLUTION"])
        self.simulators = self.initialize_simulators()
        self.models = self.initialize_models()
        self.connect_signals()

    def run(self):
        self.world.run(until=self.cfg["DURATION"], print_progress=True)

    def initialize_simulators(self):
        simulators = {}
        start_time = get_seconds_from_date(self.cfg["START_DAY"], self.cfg["START_MONTH"])
        stop_time = start_time + self.cfg["DURATION"]
        for sim, attributes in self.cfg["SIMULATORS"].items():
            if attributes["TYPE"] == "FMU":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    work_dir=attributes["PATH"],
                    fmu_name=attributes["NAME"],
                    model_name=attributes["NAME"],
                    instance_name=attributes["TYPE"] + "_Instance",
                    stop_time=stop_time,
                    start_time=start_time,
                    start_day=self.cfg["START_DAY"],
                    start_month=self.cfg["START_MONTH"]
                )
            elif attributes["TYPE"] == "TABULAR_DATA":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    start_time=start_time,
                    dataframe=build_data_frame_from_h5_directory(attributes["PATH"]),
                )
            elif attributes["TYPE"] == "NAN_PLACEHOLDER":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    attributes=load_list_from_file(attributes["PATH"]),
                )
            elif attributes["TYPE"] == "CONSTANT_VALUE_SIM":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    attributes=load_list_from_file(attributes["PATH"]),
                    value=attributes["VALUE"]
                )
            elif attributes["TYPE"] == "COLLECTOR":
                simulators[attributes["NAME"]] = self.world.start(attributes["TYPE"], output_folder=self.cfg["OUTPUT_FOLDER_PATH"])
            else:
                raise NotImplementedError(f"The Simulator {attributes['TYPE']} has not been implemented.")
        return simulators

    def initialize_models(self):
        models = {}
        for sim, attributes in self.cfg["SIMULATORS"].items():
            if "NUMBER_OF_MODELS" in attributes:
                num_of_models = attributes["NUMBER_OF_MODELS"]
            else:
                num_of_models = 1
            if attributes["TYPE"] == "FMU":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].FMU_Instance.create(num_of_models)
            elif attributes["TYPE"] == "TABULAR_DATA":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].Data.create(num_of_models)
            elif attributes["TYPE"] == "NAN_PLACEHOLDER":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].NaN.create(num_of_models)
            elif attributes["TYPE"] == "CONSTANT_VALUE_SIM":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].CONST.create(num_of_models)
            elif attributes["TYPE"] == "COLLECTOR":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].Monitor()
            else:
                raise NotImplementedError(f"The SimulatorType {attributes['TYPE']} has not been defined.")
        return models

    def connect_signals(self):
        for mapping, attributes in self.cfg["MAPPINGS"].items():
            signal_source_list = self.models[attributes["FROM"]]
            signal_drain_list = self.models[attributes["TO"]]

            source_index = attributes["FROM_INDEX"] if ("FROM_INDEX" in attributes) else 0
            drain_index = attributes["TO_INDEX"] if ("TO_INDEX" in attributes) else 0

            signal_source = signal_source_list[source_index]
            signal_drain = signal_drain_list if (attributes["TO"] == "COLLECTOR") else signal_drain_list[drain_index]

            mapping_dict = create_dict_from_file(attributes["PATH"])

            if "CIRCULAR_DEPENDENDY" in attributes and attributes["CIRCULAR_DEPENDENDY"]:
                for key, value in mapping_dict.items():
                    self.world.connect(
                        signal_source,
                        signal_drain,
                        (value, key),
                        time_shifted=True,
                        initial_data={value: attributes["INITIAL_VALUES"][key]},
                    )
            else:
                for key, value in mapping_dict.items():
                    self.world.connect(signal_source, signal_drain, (value, key))
