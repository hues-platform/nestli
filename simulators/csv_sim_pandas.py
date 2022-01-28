import pandas as pd

import mosaik_api

DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'

SENTINEL = object()


class CSV(mosaik_api.Simulator):
    def __init__(self):
        super().__init__({'models': {}})
        self.start_date = None
        self.data = None
        self.attrs = None
        self.cache = None
        self.sid = None
        self.eid = None
        
    def init(self, sid, time_resolution, sim_start, datafile, date_format=DATE_FORMAT,
             continuous=True):
        self.sid = sid
        self.time_res = pd.Timedelta(time_resolution, unit='seconds')
        start_date = self.start_date = pd.to_datetime(sim_start, format=date_format)
        self.next_date = self.start_date

        # Check if first line is the header with column names (our attributes)
        # or a model name:
        with open(datafile) as f:
            first_line = f.readline()
        if len(first_line.split(',')) == 1:
            header = 1
        else:
            header = 0

        data = self.data = pd.read_csv(datafile, index_col=0, parse_dates=True,
                                       header=header)
        data.rename(columns=lambda x: x.strip(), inplace=True)

        self.attrs = [attr.strip() for attr in data.columns]

        self.meta['type'] = 'hybrid'
        if continuous:
            non_persistent = []
        else:
            non_persistent = True
        self.meta['models']['Data'] = {
            'public': True,
            'params': [],
            'attrs': self.attrs,
            'non-persistent': non_persistent,
        }

        # Find first relevant value:
        if continuous:
            first_index = data.index.get_loc(start_date, method='ffill')
            self.next_index = first_index
        else:
            first_index = data.index.get_loc(start_date, method='bfill')
            first_date = data.index[first_index]
            if first_date == start_date:
                self.next_index = first_index
            else:
                self.next_index = -1

        return self.meta

    def create(self, num, model):
        if model != 'Data':
            raise ValueError('Invalid model "%s" % model')

        if num > 1 or self.eid is not None:
            raise ValueError(f"Only one entity allowed for simulator {self.sid}.")

        self.eid = 'csv-0'
        entities = [
            {'eid': self.eid,
             'type': model,
             'rel': [],
            }]

        return entities

    def step(self, time, inputs, max_advance):
        data = self.data
        if self.next_index >= 0:
            current_row = data.iloc[self.next_index]
            self.cache = dict(current_row)
        else:
            self.cache = {}
        self.next_index += 1
        try:
            next_date = self.data.index[self.next_index]
            next_step = int((next_date - self.start_date)/self.time_res)
        except IndexError:
            next_step = max_advance

        return next_step

    def get_data(self, outputs):
        data = {}
        attrs = outputs.get(self.eid, [])
        for attr in attrs:
            value = self.cache.get(attr, SENTINEL)
            if value != SENTINEL:
                data[attr] = value

        if data:
            data = {self.eid: data}

        if 'csv-1' in self.eid:
            print('CSV: ', data)

        return data


