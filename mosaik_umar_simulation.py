import mosaik
import os
from input_functions import create_dict_from_file


# Specify simulator configurations
sim_config = {
    'FMU': {'python': 'simulators.FmuAdapter:FmuAdapter'
    },
    'CSV': {
        'python': 'simulators.csv_sim_pandas:CSV'
    },
    'Collector': {
        'python': 'simulators.Collector:Collector'
    }
}

# Set scenario parameters:
END = 2 * 24 * 60 * 60
START = '2020-01-01 00:00:00'
INPUT_DATA = "simulators/ressources/all.csv"

# Set up the "world" of the scenario
world = mosaik.World(sim_config, time_resolution=60)

# Initialize the simulators
umar_simulator = world.start('FMU', work_dir=os.path.join(os.getcwd(),"inputs/fmu"), fmu_name="UMAR", model_name="UMAR", instance_name="FMU_Instance", stop_time=END)

preprocess_simulator = world.start('FMU', work_dir=os.path.join(os.getcwd(),"inputs/fmu"), fmu_name="preprocess", model_name="Preprocess", instance_name="FMU_Instance", stop_time=END)

CSV_simulator = world.start('CSV', sim_start=START, datafile=INPUT_DATA)

collector = world.start('Collector')


# Instantiate model entities
umar_model = umar_simulator.FMU_Instance.create(1)
preprocess_model = preprocess_simulator.FMU_Instance.create(1)
CSV_data_model = CSV_simulator.Data.create(1)
monitor = collector.Monitor()

mapping_from_preprocess_to_umar = create_dict_from_file("./inputs/mappings/mapping_umar_from_preprocess.txt")
mapping_from_umar_to_preprocess = create_dict_from_file("./inputs/mappings/mapping_preprocess_from_umar.txt")
mapping_from_csv_to_preprocess = create_dict_from_file("./inputs/mappings/mapping_preprocess_from_data.txt")

for key, value in mapping_from_preprocess_to_umar.items():
    world.connect(preprocess_model[0], umar_model[0], (value, key))

for key, value in mapping_from_umar_to_preprocess.items():
    world.connect(umar_model[0], preprocess_model[0], (value, key), time_shifted=True, initial_data={value:0.0})

for key, value in mapping_from_csv_to_preprocess.items():
    world.connect(CSV_data_model[0], preprocess_model[0], (value, key))

world.connect(umar_model[0], monitor, "T_WC275")

world.run(until=END, print_progress=True)
