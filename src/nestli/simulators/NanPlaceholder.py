import mosaik_api

meta = {
    "models": {},
    "type": "time-based",
}


class NanPlaceholder(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.eid = None

    def init(self, sid, time_resolution, attributes):
        self.sid = sid
        self.time_resolution = time_resolution
        self.meta["models"]["NaN"] = {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": attributes,
        }
        return self.meta

    def create(self, num, model):
        self.eid = "nan-placeholder-0"
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
                data[eid][attr] = float("nan")
        return data
