import logging
import numpy as np
import datetime as dt


class PythonController:
    """
    Template for controller written in Python. Please add your controller directly here.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.R272_Occupant_Override = np.NAN
        self.R272_Shade_Override = np.NAN
        self.R272_Window_Override = np.NAN
        self.R272_SetPoint_Override = np.NAN
        self.R273_Occupant_Override = np.NAN
        self.R273_Shade1_Override = np.NAN
        self.R273_Shade2_Override = np.NAN
        self.R273_Shade3_Override = np.NAN
        self.R273_Window1_Override = np.NAN
        self.R273_Window2_Override = np.NAN
        self.R273_SetPoint_Override = np.NAN
        self.R274_Occupant_Override = np.NAN
        self.R274_Shade_Override = np.NAN
        self.R274_Window_Override = np.NAN
        self.R274_SetPoint_Override = np.NAN
        self.R275_SetPoint_Override = np.NAN
        self.R276_SetPoint_Override = np.NAN

    def control(
        self,
        current_simulation_time: dt.datetime,
        Weather_DryBulb_Temperature,
        Weather_DewPoint_Temperature,
        Weather_Relative_Humidity,
        Weather_Direct_SolarRadiation,
        Weather_Diffuse_SolarRadiation,
        Weather_Wind_Speed,
        Weather_Wind_Direction,
        SetPoint_UpperBound,
        SetPoint_LowerBound,
        R272_Air_Temperature,
        R273_Air_Temperature,
        R274_Air_Temperature,
        R275_Air_Temperature,
        R276_Air_Temperature,
        Air_Conditioning_Mode,
        District_Network_Temperature,
    ):
        """
        Inputs are values communicated and coordinated by mosaik.
        Inputs:
        self                            : Previous state of the controller
        current_simulation_time         : The time (datetime object)
        Weather_DryBulb_Temperature     : Current outdoor drybulb temperature
        Weather_DewPoint_Temperature    : Current outdoor dewpoint temperature
        Weather_Relative_Humidity       : Current outdoor relative humidity
        Weather_Direct_SolarRadiation   : Current outdoor direct horizontal solar radiation
        Weather_Diffuse_SolarRadiation  : Current outdoor diffuse horizontal solar radiation
        Weather_Wind_Speed              : Current outdoor wind speed
        Weather_Wind_Direction          : Current outdoor wind direction
        SetPoint_UpperBound             : The upper bound of thermal comfort
        SetPoint_LowerBound             : The lower bound of thermal comfort
        R272_Air_Temperature            : Current indoor air temperature in room R272
        R273_Air_Temperature            : Current indoor air temperature in room R273
        R274_Air_Temperature            : Current indoor air temperature in room R274
        R275_Air_Temperature            : Current indoor air temperature in room R275
        R276_Air_Temperature            : Current indoor air temperature in room R276
        Air_Conditioning_Mode           : Current state of air conditioning (Heating=1, Off=0, Cooling=-1)
        District_Network_Temperature    : Current temperature of water in the district network (for both heating and cooling mode)

        You may replace the following values with your control decisions.
        Outputs:
        self.R272_Occupant_Override : Manipulating the internal gains from occupants' activities in Room 272
        self.R272_Shade_Override    : Manipulating the operation of the shading in room R272
        self.R272_Window_Override   : Manipulating the operation of the window in room R272
        self.R272_SetPoint_Override : Manipulating the setpoint temperature  in room R272
        self.R273_Occupant_Override : Manipulating the internal gains from occupants' activities in Room 273
        self.R273_Shade1_Override    : Manipulating the operation of the shading in room R273
        self.R273_Shade2_Override    : Manipulating the operation of the shading in room R273
        self.R273_Shade3_Override    : Manipulating the operation of the shading in room R273
        self.R273_Window1_Override  : Manipulating the operation of window 1 in room R273
        self.R273_Window2_Override  : Manipulating the operation of window 2 in room R273
        self.R273_SetPoint_Override : Manipulating the setpoint temperature  in room R273
        self.R274_Occupant_Override : Manipulating the internal gains from occupants' activities in Room 274
        self.R274_Shade_Override    : Manipulating the operation of the shading in room R274
        self.R274_Window_Override   : Manipulating the operation of the window in room R274
        self.R274_SetPoint_Override : Manipulating the setpoint temperature  in room R274
        self.R275_SetPoint_Override : Manipulating the setpoint temperature  in room R275
        self.R276_SetPoint_Override : Manipulating the setpoint temperature  in room R276
        """

        # An example of overwriting/controlling the setpoint temperature for rooms R272, R273 and R274:
        # In this example the controller keeps the indoor air temperature near the lower comfort bound
        # The controller executes every 15 minutes and holds the last value in between executions
        if np.mod(current_simulation_time.minute, 15) == 0:

            if R272_Air_Temperature < SetPoint_LowerBound:
                self.R272_SetPoint_Override = 32
            else:
                self.R272_SetPoint_Override = 12

            if R273_Air_Temperature < SetPoint_LowerBound:
                self.R273_SetPoint_Override = 32
            else:
                self.R273_SetPoint_Override = 12

            if R274_Air_Temperature < SetPoint_LowerBound:
                self.R274_SetPoint_Override = 32
            else:
                self.R274_SetPoint_Override = 12

        # Return the control decisions to be fed to the building.
        return (
            self.R272_Occupant_Override,
            self.R272_Shade_Override,
            self.R272_Window_Override,
            self.R272_SetPoint_Override,
            self.R273_Occupant_Override,
            self.R273_Shade1_Override,
            self.R273_Shade2_Override,
            self.R273_Shade3_Override,
            self.R273_Window1_Override,
            self.R273_Window2_Override,
            self.R273_SetPoint_Override,
            self.R274_Occupant_Override,
            self.R274_Shade_Override,
            self.R274_Window_Override,
            self.R274_SetPoint_Override,
            self.R275_SetPoint_Override,
            self.R276_SetPoint_Override,
        )
