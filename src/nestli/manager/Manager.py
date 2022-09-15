import os
from typing import Dict
import mosaik
import logging
import datetime as dt

from nestli.common.input_functions import create_dict_from_file, build_data_frame_from_h5_directory, load_list_from_file, download_and_unzip
from nestli.manager import DATA_DOWNLOAD, MOSAIK_CONFIG
from nestli.common.config_loader import (
    load_config,
    convert_entries_to_abs_pathes,
    validate_config,
)


class Manager:
    """This is the main class of nestli. It initializes simulators and starts the simulation. The configuration is being read from the config file."""

    def __init__(self, config_file):
        """
        :param config_file: path of a config file
        """
        self.cfg = load_config(config_file)
        convert_entries_to_abs_pathes(self.cfg, config_file)
        validate_config(self.cfg)
        self.mosaik_cfg = MOSAIK_CONFIG
        self.init_logger()
        self.logger = logging.getLogger(__name__)

    def build_simulation(self):
        """Initializes all that is necessary for the simulation."""
        self.world = mosaik.World(self.mosaik_cfg, time_resolution=self.cfg["RESOLUTION"])
        self.simulators = self.initialize_simulators()
        self.models = self.initialize_models()
        self.connect_signals()

    def run(self):
        """Starts the mosaik simulation. The end of the simulation has to be declared in the config with the DURATION field."""
        self.logger.info("Starting simulation")
        self.world.run(until=self.cfg["DURATION"], print_progress=True, lazy_stepping=True)

    def initialize_simulators(self) -> Dict:
        """Initializes the different simulators according to the config."""
        simulators = {}
        start_date = dt.datetime.strptime(self.cfg["START"], r"%Y-%m-%d")
        for sim, attributes in self.cfg["SIMULATORS"].items():
            if attributes["TYPE"] == "FMU":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    work_dir=attributes["PATH"],
                    fmu_name=attributes["NAME"],
                    model_name=attributes["NAME"],
                    instance_name=attributes["TYPE"] + "_Instance",
                    duration=self.cfg["DURATION"],
                    start_date=start_date,
                )
            elif attributes["TYPE"] == "TABULAR_DATA":
                # ToDo
                # if data already in attributes["PATH"], build df
                # otherwise request and unzip and save, then build df
                # give df and date to simulator
                if not any(fname.endswith(".h5") for fname in os.listdir(attributes["PATH"])):
                    download_and_unzip(DATA_DOWNLOAD, attributes["PATH"])
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    start_date=start_date,
                    dataframe=build_data_frame_from_h5_directory(attributes["PATH"]),
                )
            elif attributes["TYPE"] == "DATABASE_DATA":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    start_date=start_date,
                )
            elif attributes["TYPE"] == "NAN_PLACEHOLDER":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    attributes=load_list_from_file(attributes["PATH"]),
                )
            elif attributes["TYPE"] == "CONSTANT_VALUE":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    constant_values=create_dict_from_file(attributes["PATH"]),
                )
            elif attributes["TYPE"] == "COLLECTOR":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    output_folder=self.cfg["OUTPUT_FOLDER_PATH"],
                    start_date=start_date,
                )
            elif attributes["TYPE"] == "OCCUPANT":
                simulators[attributes["NAME"]] = self.world.start(
                    attributes["TYPE"],
                    start_date=start_date,
                    path=attributes["PATH"],
                )
            else:
                raise NotImplementedError(f"The Simulator {attributes['TYPE']} has not been implemented.")
        return simulators

    def initialize_models(self) -> Dict:
        """Initializes the number of models per simulator according to the config. Default is 1 model."""
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
            elif attributes["TYPE"] == "DATABASE_DATA":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].Data.create(num_of_models)
            elif attributes["TYPE"] == "NAN_PLACEHOLDER":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].NaN.create(num_of_models)
            elif attributes["TYPE"] == "CONSTANT_VALUE":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].CONST.create(num_of_models)
            elif attributes["TYPE"] == "COLLECTOR":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].Monitor()
            elif attributes["TYPE"] == "OCCUPANT":
                models[attributes["NAME"]] = self.simulators[attributes["NAME"]].Occupant.create(num_of_models)
            else:
                raise NotImplementedError(f"The SimulatorType {attributes['TYPE']} has not been defined.")
        return models

    def connect_signals(self):
        """Connects signals from simulator to simulator according to the mappings declared in the config under 'MAPPINGS'."""
        for mapping, attributes in self.cfg["MAPPINGS"].items():
            signal_source_list = self.models[attributes["FROM"]]
            for mapping_from_source, mapping_attributes in attributes["MAPPINGS"].items():
                signal_drain_list = self.models[mapping_attributes["TO"]]

                source_index = attributes["INDEX"] if ("INDEX" in attributes) else 0
                drain_index = mapping_attributes["INDEX"] if ("INDEX" in mapping_attributes) else 0

                signal_source = signal_source_list[source_index]
                signal_drain = signal_drain_list if (mapping_attributes["TO"] == "COLLECTOR") else signal_drain_list[drain_index]

                mapping_dict = mapping_attributes["VARIABLES"]

                if "CIRCULAR_DEPENDENDY" in mapping_attributes and mapping_attributes["CIRCULAR_DEPENDENDY"]:
                    for source_attribute, drain_attribute in mapping_dict.items():
                        if isinstance(drain_attribute, list):
                            for elem in drain_attribute:
                                self.world.connect(
                                    signal_source,
                                    signal_drain,
                                    (source_attribute, elem),
                                    time_shifted=True,
                                    initial_data={source_attribute: mapping_attributes["INITIAL_VALUES"][source_attribute]},
                                )
                        else:
                            self.world.connect(
                                signal_source,
                                signal_drain,
                                (source_attribute, drain_attribute),
                                time_shifted=True,
                                initial_data={source_attribute: mapping_attributes["INITIAL_VALUES"][source_attribute]},
                            )
                else:
                    for source_attribute, drain_attribute in mapping_dict.items():
                        if isinstance(drain_attribute, list):
                            for elem in drain_attribute:
                                self.world.connect(signal_source, signal_drain, (source_attribute, elem))
                        else:
                            self.world.connect(signal_source, signal_drain, (source_attribute, drain_attribute))

    def init_logger(self):
        """Initializes the logger and logging to a file."""
        file_handler = logging.FileHandler(self.cfg["OUTPUT_FOLDER_PATH"] + "/simulation.log")
        formatter = logging.Formatter("%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
