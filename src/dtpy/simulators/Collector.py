"""
A simple data collector that prints all data when the simulation finishes.

"""
import collections
import os
import pandas as pd
import mosaik_api
import datetime as dt


META = {
    "type": "event-based",
    "models": {
        "Monitor": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [],
        },
    },
}


class Collector(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))

    def init(self, sid, time_resolution, output_folder, start_date: dt.datetime):
        self.output_folder = output_folder
        self.start_time = start_date
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Monitor.")

        self.eid = "Monitor"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        timestamp = dt.timedelta(seconds=time) + self.start_time
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr][timestamp] = value

        return None

    def finalize(self):
        print("Collected data saved at:")
        for sim, sim_data in sorted(self.data.items()):
            print(os.path.join(self.output_folder, sim + "_output.csv"))
            sim_df = pd.DataFrame()
            for attr, values in sorted(sim_data.items()):
                var_df = pd.DataFrame.from_dict(values, orient="index", columns=[attr])
                sim_df = pd.concat([sim_df, var_df], axis=1)
            sim_df.to_csv(os.path.join(self.output_folder, sim + "_output.csv"))
