
MOSAIK_CONFIG = {
    'FMU': {'python': 'dtpy.simulators.FmuAdapter:FmuAdapter'
    },
    'CSV': {
        'python': 'dtpy.simulators.csv_sim_pandas:CSV'
    },
    'COLLECTOR': {
        'python': 'dtpy.simulators.Collector:Collector'
    }
}