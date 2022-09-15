import mosaik_api
import datetime as dt
import logging
import sys


ATTRIBUTES = [
    "Weather_DryBulb_Temperature",
    "Weather_DewPoint_Temperature",
    "Weather_Relative_Humidity",
    "Weather_Direct_SolarRadiation",
    "Weather_Diffuse_SolarRadiation",
    "Weather_Wind_Speed",
    "Weather_Wind_Direction",
    "R272_Air_Temperature",
    "R273_Air_Temperature",
    "R274_Air_Temperature",
    "SetPoint_UpperBound",
    "SetPoint_LowerBound",
    "R272_Shade",
    "R273_Shade",
    "R274_Shade",
    "R272_Window",
    "R273_Window1",
    "R273_Window2",
    "R274_Window",
    "R272_Occupancy",
    "R273_Occupancy",
    "R274_Occupancy",
    "R272_SetPoint_Override",
    "R272_Occupant_Operation",
    "R272_Window_Override",
    "R272_Shade_Override",
    "R273_SetPoint_Override",
    "R273_Occupant_Operation",
    "R273_Window1_Override",
    "R273_Window2_Override",
    "R273_Shade_Override",
    "R274_SetPoint_Override",
    "R274_Occupant_Operation",
    "R274_Window_Override",
    "R274_Shade_Override",
]


class Occupant(mosaik_api.Simulator):
    def __init__(self):
        super().__init__({"models": {}})
        self.attrs = None
        self.sid = None
        self.eid = None

    def init(self, sid, time_resolution, start_date, path):
        self.sid = sid
        self.time_resolution = time_resolution
        self.current_simulation_time = start_date
        self.attrs = ATTRIBUTES
        self.logger = logging.getLogger(__name__)

        self.meta["type"] = "time-based"
        self.meta["models"]["Occupant"] = {
            "public": True,
            "params": [],
            "attrs": self.attrs,
            "non-persistent": [],
        }
        sys.path.append(path)
        from virtual_occupants import occupant_function

        self.occupant_function = occupant_function
        return self.meta

    def create(self, num, model):
        self.eid = "occupant-0"
        entities = [
            {
                "eid": self.eid,
                "type": model,
                "rel": [],
            }
        ]
        return entities

    def step(self, t, inputs, max_advance):
        # You can add debug statements with the logger as follows
        self.logger.info(f"Occupant Step: {self.current_simulation_time}")
        self.input_data = {}
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.input_data[attr] = value

        (
            R272_Occupant_Operation,
            R272_Shade_Override,
            R272_Window_Override,
            R272_SetPoint_Override,
            R273_Occupant_Operation,
            R273_Shade_Override,
            R273_Window1_Override,
            R273_Window2_Override,
            R273_SetPoint_Override,
            R274_Occupant_Operation,
            R274_Shade_Override,
            R274_Window_Override,
            R274_SetPoint_Override,
        ) = self.occupant_function(
            t,
            self.input_data["Weather_DryBulb_Temperature"],
            self.input_data["Weather_DewPoint_Temperature"],
            self.input_data["Weather_Relative_Humidity"],
            self.input_data["Weather_Direct_SolarRadiation"],
            self.input_data["Weather_Diffuse_SolarRadiation"],
            self.input_data["Weather_Wind_Speed"],
            self.input_data["Weather_Wind_Direction"],
            self.input_data["SetPoint_UpperBound"],
            self.input_data["SetPoint_LowerBound"],
            self.input_data["R272_Air_Temperature"],
            self.input_data["R273_Air_Temperature"],
            self.input_data["R274_Air_Temperature"],
        )

        # These output values must be provided. The default is what you see below.
        self.output_data = {
            "R272_SetPoint_Override": R272_SetPoint_Override,
            "R273_SetPoint_Override": R273_SetPoint_Override,
            "R274_SetPoint_Override": R274_SetPoint_Override,
            "R272_Occupant_Operation": R272_Occupant_Operation,
            "R272_Window_Override": R272_Window_Override,
            "R272_Shade_Override": R272_Shade_Override,
            "R273_Occupant_Operation": R273_Occupant_Operation,
            "R273_Window1_Override": R273_Window1_Override,
            "R273_Window2_Override": R273_Window2_Override,
            "R273_Shade_Override": R273_Shade_Override,
            "R274_Occupant_Operation": R274_Occupant_Operation,
            "R274_Window_Override": R274_Window_Override,
            "R274_Shade_Override": R274_Shade_Override,
        }
        self.current_simulation_time = self.current_simulation_time + dt.timedelta(minutes=1)
        return t + self.time_resolution

    def get_data(self, outputs):
        data = {}
        attrs = outputs.get(self.eid, [])
        for attr in attrs:
            value = self.output_data.get(attr)
            data[attr] = value
        if data:
            data = {self.eid: data}
        return data

    def finalize(self):
        return super().finalize()
