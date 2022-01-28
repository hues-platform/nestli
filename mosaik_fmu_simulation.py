import mosaik
import os


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
END = 24 * 60 * 60
START = '2020-01-01 00:00:00'
INPUT_DATA = "simulators/ressources/Q_data.csv"

# Set up the "world" of the scenario
world = mosaik.World(sim_config, time_resolution=900)

# Initialize the simulators
fmusim = world.start('FMU', work_dir=os.path.join(os.getcwd(),"inputs/fmu"), fmu_name="test", model_name="FMU", instance_name="FMU_Instance")

DNIdata = world.start('CSV', sim_start=START, datafile=INPUT_DATA)

collector = world.start('Collector')


# Instantiate model entities
fmu_model = fmusim.FmuModel.create(1)
solar_data = DNIdata.Data.create(1)
monitor = collector.Monitor()

world.connect(solar_data[0], fmu_model[0], 'Q')
world.connect(fmu_model[0], monitor, "TRooMea")

world.run(until=END, print_progress=True)
