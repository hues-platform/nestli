import mosaik_api

meta = {
    "models": {},
    "type": "time-based",
}


class ConstantValueSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.eid = None

    def init(self, sid, time_resolution, attributes, value):
        self.sid = sid
        self.time_resolution = time_resolution
        self.meta["models"]["CONST"] = {"public": True, "any_inputs": True, "params": [], "attrs": attributes}
        self.value = value
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
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.value
        return data
