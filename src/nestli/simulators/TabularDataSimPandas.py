import logging
import mosaik_api
import datetime as dt


class TabularData(mosaik_api.Simulator):
    def __init__(self):
        super().__init__({"models": {}})
        self.start_date = None
        self.data = None
        self.attrs = None
        self.cache = None
        self.sid = None
        self.eid = None

    def init(self, sid, time_resolution, start_date, dataframe, continuous=True):
        self.sid = sid
        self.time_resolution = time_resolution

        data = self.data = dataframe

        data.rename(columns=lambda x: x.strip(), inplace=True)

        self.attrs = [attr.strip() for attr in data.columns]

        self.meta["type"] = "hybrid"
        if continuous:
            non_persistent = []
        else:
            non_persistent = True
        self.meta["models"]["Data"] = {
            "public": True,
            "params": [],
            "attrs": self.attrs,
            "non-persistent": non_persistent,
        }
        self.logger = logging.getLogger(__name__)
        # ToDo: Search for start index
        self.start_date = start_date
        start_time = (start_date - dt.datetime(year=2019, month=1, day=1)).total_seconds()
        self.next_index = (int)(start_time / time_resolution)

        return self.meta

    def create(self, num, model):
        if model != "Data":
            raise ValueError('Invalid model "%s" % model')

        if num > 1 or self.eid is not None:
            raise ValueError(f"Only one entity allowed for simulator {self.sid}.")

        self.eid = "tabular_data-0"
        entities = [
            {
                "eid": self.eid,
                "type": model,
                "rel": [],
            }
        ]

        return entities

    def step(self, time, inputs, max_advance):
        self.logger.debug(f"Data Step: {self.start_date + dt.timedelta(seconds=time)}")

        data = self.data
        if self.next_index >= 0:
            current_row = data.iloc[self.next_index]
            self.cache = dict(current_row)
        else:
            self.cache = {}
        self.next_index += 1

        next_step = time + self.time_resolution
        return next_step

    def get_data(self, outputs):
        data = {}
        attrs = outputs.get(self.eid, [])
        for attr in attrs:
            value = self.cache.get(attr)
            data[attr] = value
        if data:
            data = {self.eid: data}
        return data
