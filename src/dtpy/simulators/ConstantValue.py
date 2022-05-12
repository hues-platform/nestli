from typing import Dict
import mosaik_api

SENTINEL = object()

meta = {
    "models": {},
    "type": "time-based",
}


class ConstantValue(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.eid = None

    def init(self, sid, time_resolution, constant_values: Dict):
        self.sid = sid
        self.time_resolution = time_resolution
        data = self.data = constant_values

        self.attrs = [key for key, _ in data.items()]
        self.meta["models"]["CONST"] = {
            "public": True,
            "params": [],
            "attrs": self.attrs,
            "non-persistent": [],
        }

        return self.meta

    def create(self, num, model):
        self.eid = "const-0"
        entities = [
            {
                "eid": self.eid,
                "type": model,
                "rel": [],
            }
        ]
        return entities

    def step(self, time, inputs, max_advance):
        return time + self.time_resolution

    def get_data(self, outputs):
        data = {}
        attrs = outputs.get(self.eid, [])
        for attr in attrs:
            value = self.data.get(attr, SENTINEL)
            if value != SENTINEL:
                data[attr] = value

        if data:
            data = {self.eid: data}

        return data
