import mosaik_api
import datetime as dt
import logging
from importlib import import_module

ATTRIBUTES = [
    "Weather_DryBulb_Temperature",
    "Weather_DewPoint_Temperature",
    "Weather_Relative_Humidity",
    "Weather_Direct_SolarRadiation",
    "Weather_Diffuse_SolarRadiation",
    "Weather_Wind_Speed",
    "Weather_Wind_Direction",
    "SetPoint_UpperBound",
    "SetPoint_LowerBound",
    "R272_Air_Temperature",
    "R273_Air_Temperature",
    "R274_Air_Temperature",
    "R275_Air_Temperature",
    "R276_Air_Temperature",
    "Air_Conditioning_Mode",
    "District_Network_Temperature",
    "R272_SetPoint_Override",
    "R272_Occupant_Override",
    "R272_Window_Override",
    "R272_Shade_Override",
    "R273_SetPoint_Override",
    "R273_Occupant_Override",
    "R273_Window1_Override",
    "R273_Window2_Override",
    "R273_Shade1_Override",
    "R273_Shade2_Override",
    "R273_Shade3_Override",
    "R274_SetPoint_Override",
    "R274_Occupant_Override",
    "R274_Window_Override",
    "R274_Shade_Override",
    "R275_SetPoint_Override",
    "R276_SetPoint_Override",
]


class PythonFunction(mosaik_api.Simulator):
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
        self.meta["models"]["PythonFunction"] = {
            "public": True,
            "params": [],
            "attrs": self.attrs,
            "non-persistent": [],
        }
        module_path, class_name = path.rsplit(".", 1)
        module = import_module(module_path)
        pythonclass = getattr(module, class_name)

        self.controller = pythonclass()
        return self.meta

    def create(self, num, model):
        self.eid = "pythonfunction-0"
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
        self.logger.debug(f"Controller Python Step: {self.current_simulation_time}")
        self.input_data = {}
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.input_data[attr] = value

        (
            R272_Occupant_Override,
            R272_Shade_Override,
            R272_Window_Override,
            R272_SetPoint_Override,
            R273_Occupant_Override,
            R273_Shade1_Override,
            R273_Shade2_Override,
            R273_Shade3_Override,
            R273_Window1_Override,
            R273_Window2_Override,
            R273_SetPoint_Override,
            R274_Occupant_Override,
            R274_Shade_Override,
            R274_Window_Override,
            R274_SetPoint_Override,
            R275_SetPoint_Override,
            R276_SetPoint_Override,
        ) = self.controller.control(
            self.current_simulation_time,
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
            self.input_data["R275_Air_Temperature"],
            self.input_data["R276_Air_Temperature"],
            self.input_data["Air_Conditioning_Mode"],
            self.input_data["District_Network_Temperature"],
        )

        # These output values must be provided. The default is what you see below.
        self.output_data = {
            "R272_SetPoint_Override": R272_SetPoint_Override,
            "R273_SetPoint_Override": R273_SetPoint_Override,
            "R274_SetPoint_Override": R274_SetPoint_Override,
            "R275_SetPoint_Override": R275_SetPoint_Override,
            "R276_SetPoint_Override": R276_SetPoint_Override,
            "R272_Occupant_Override": R272_Occupant_Override,
            "R272_Window_Override": R272_Window_Override,
            "R272_Shade_Override": R272_Shade_Override,
            "R273_Occupant_Override": R273_Occupant_Override,
            "R273_Window1_Override": R273_Window1_Override,
            "R273_Window2_Override": R273_Window2_Override,
            "R273_Shade1_Override": R273_Shade1_Override,
            "R273_Shade2_Override": R273_Shade2_Override,
            "R273_Shade3_Override": R273_Shade3_Override,
            "R274_Occupant_Override": R274_Occupant_Override,
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
