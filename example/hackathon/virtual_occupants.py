import numpy as np
import math
from scipy.stats import truncnorm


def chance_of_occupancy(occupant_presence, number_of_occupants):
    """
    this function returns the occupancy presence from a truncated probability distribution
    @param occupant_presence: a time-dependant array that defines the probability of occupants being at home at a given time
    @param number_of_occupants: the number of occupants who live in this home
    @return: a boolean array that indicates each occupant's presence at home
    """

    lower_limit = 0
    upper_limit = 1
    mu = occupant_presence
    sigma = 0.05

    probability_distribution = truncnorm((lower_limit - mu) / sigma, (upper_limit - mu) / sigma, loc=mu, scale=sigma)

    presence_schedule = np.round(probability_distribution.rvs(number_of_occupants), decimals=0)

    return presence_schedule


def chance_of_circulation(room_probabilities, number_of_occupants):
    """
    this function assigns an occupant to either the bedroom or the living room
    @param room_probabilities:
    @param number_of_occupants:
    @return:
    """

    random_positions = np.random.dirichlet(np.maximum(room_probabilities, 0.00000000000000000000001), 1)

    random_positions = np.round(random_positions)

    return random_positions


def occupant_function(
    current_simulation_time,
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
):
    """
    This function accepts features of both indoor and outdoor environment
    and returns occupants' response to the features.
    @param current_simulation_time: time of the simulation in seconds
    @param Weather_DryBulb_Temperature: Outdoor dry bulb temperature
    @param Weather_DewPoint_Temperature: Outdoor dew point temperature
    @param Weather_Relative_Humidity: Outdoor relative humidity
    @param Weather_Direct_SolarRadiation: Outdoor direct solar radiation on a horizontal plane
    @param Weather_Diffuse_SolarRadiation: Outdoor diffuse solar radiation on a horizontal plane
    @param Weather_Wind_Speed: Outdoor wind speed
    @param Weather_Wind_Direction: Outdoor wind direction
    @param SetPoint_UpperBound: The upper limit of thermostat (23 C at night and 25 C during the day)
    @param SetPoint_LowerBound: The lower limit of thermostat (22 C at night and 21 C during the day)
    @param R272_Air_Temperature: Indoor air temperature in Bedroom #1 (R272)
    @param R273_Air_Temperature: Indoor air temperature in the Living room (R273)
    @param R274_Air_Temperature: Indoor air temperature in Bedroom #2 (R274)
    @return:
        R272_Occupant_Operation: The heat gain from people, lights and equipment in Bedroom #1 (R272)
        R272_Shade_Override: Occupants' deployment of the window shades in Bedroom #1 (R272)
        R272_Window_Override: Occupants' opening of the window in Bedroom #1 (R272)
        R272_SetPoint_Override: Occupants' manual adjustment of the thermostat in Bedroom #1 (R272)
        R273_Occupant_Operation: The heat gain from people, lights and equipment in the Living room (R273)
        R273_Shade_Override: Occupants' deployment of the window shades in the Living room (R273)
        R273_Window1_Override: Occupants' opening of the first window in the Living room (R273)
        R273_Window2_Override: Occupants' opening of the second window in the Living room (R273)
        R273_SetPoint_Override: Occupants' manual adjustment of the thermostat in the Living room (R273)
        R274_Occupant_Operation: The heat gain from people, lights and equipment in Bedroom #2 (R274)
        R274_Shade_Override: Occupants' deployment of the window shades in Bedroom #2 (R274)
        R274_Window_Override: Occupants' opening of the window in Bedroom #2 (R274)
        R274_SetPoint_Override: Occupants' manual adjustment of the thermostat in Bedroom #2 (R274)
    """
    number_of_rooms = 3  # the numer of rooms in the house
    number_of_bedrooms = 2  # the number of bedrooms in the house
    number_of_occupants = 2  # the number of occupants that live in the house

    # converting the simulation time from seconds to the hour of the day (from 0 to 23)
    hour_of_simulation_time = int((np.mod(current_simulation_time, 86400)) / 3600)

    # an indicator of the sky's brightness based on the total (direct+diffuse) outdoor solar radiation
    brightness = (Weather_Diffuse_SolarRadiation + Weather_Direct_SolarRadiation) / 1186

    # a nominal daily schedule of occupants' presence in the livingroom each hour of the day
    livingroom_schedule = np.array([0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.05, 0.05])

    # a nominal daily schedule of occupants' activeness during each hour of the day
    activity_schedule = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.5, 1, 1, 0.75, 0.75, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.75, 0.5, 0.25, 0.1])

    # a nominal daily schedule of occupants' presence at home during each hour of the day
    presence_schedule = np.array([1, 1, 1, 1, 1, 1, 1, 0.5, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, 1, 1])

    # a nominal daily schedule of occupants' presence in the bedrooms as a function of their presence in the living room
    bedroom_schedule = 1 - livingroom_schedule

    # converting the schedule of the living room from hourly to seconds
    livingroom_schedule = np.repeat(livingroom_schedule, 60)
    livingroom_schedule = np.reshape(livingroom_schedule, 1440)
    livingroom_schedule = np.convolve(livingroom_schedule, np.ones(60), "same") / 60

    # converting the schedule of occupant's activity from hourly to seconds
    activity_schedule = np.repeat(activity_schedule, 60)
    activity_schedule = np.reshape(activity_schedule, 1440)
    activity_schedule = np.convolve(activity_schedule, np.ones(60), "same") / 60

    # converting the schedule of occupants' presence in the building from hourly to seconds
    presence_schedule = np.repeat(presence_schedule, 60)
    presence_schedule = np.reshape(presence_schedule, 1440)
    presence_schedule = np.convolve(presence_schedule, np.ones(60), "same") / 60
    presence_schedule = chance_of_occupancy(presence_schedule[hour_of_simulation_time], number_of_occupants)

    # converting the schedule of the bedroom from hourly to seconds
    bedroom_schedule = np.repeat(bedroom_schedule, 60)
    bedroom_schedule = np.reshape(bedroom_schedule, 1440)
    bedroom_schedule = np.convolve(bedroom_schedule, np.ones(60), "same") / 60

    # a placeholder for the position of the occupants based on each room (rows: occupants , columns: rooms)
    occupancy_matrix = np.zeros((number_of_occupants, number_of_rooms))

    # assigning each occupant to one bedroom (as a permanent room for stay)
    occupant_id = np.tile(np.arange(0, number_of_bedrooms, dtype=int), math.ceil(number_of_occupants / number_of_bedrooms))

    # Assigning each occupant to either the bedroom or the living room base on the time of the day
    for sweeping_occupants in range(number_of_occupants):
        typical_schedule = np.zeros((number_of_rooms))
        typical_schedule[occupant_id[sweeping_occupants]] = bedroom_schedule[hour_of_simulation_time * 60]
        if number_of_rooms > number_of_bedrooms:
            for number_of_nonbedrooms in range(number_of_rooms - number_of_bedrooms):
                typical_schedule[number_of_bedrooms] = livingroom_schedule[hour_of_simulation_time * 60]

        occupancy_matrix[sweeping_occupants, :] = presence_schedule[sweeping_occupants] * chance_of_circulation(typical_schedule, 1)

    # calculating the total occupants in each room
    R272_occupants = np.sum(occupancy_matrix[:, 0], axis=0)
    R274_occupants = np.sum(occupancy_matrix[:, 1], axis=0)
    R273_occupants = np.sum(occupancy_matrix[:, 2], axis=0)

    # assigning an activity to bedroom #1 (R272) base on the time of the day
    R272_gains_human = R272_occupants * activity_schedule[hour_of_simulation_time * 60]
    # assigning the satus of lights to each bedroom #1 (R272) based on the time of the day and the outdoor brightness
    R272_gain_lighting = R272_occupants * (1 - brightness)
    # assigning the status of equipment usage to bedroom #1 (R272) base on the time of the day
    R272_gain_equipment = R272_occupants * activity_schedule[hour_of_simulation_time] + 0.1
    # summing the heat gain from people, lights and equipment for bedroom #1 (R272)
    R272_Occupant_Operation = R272_gains_human + R272_gain_lighting + R272_gain_equipment
    # operating the window shade in bedroom #1 (R272) based on indoor air temperature and the outdoor brightness
    R272_Shade_Override = np.round(R272_occupants * np.maximum(R272_Air_Temperature - 26, 0) * brightness)
    # operating the window opening in bedroom #1 (R272) based on
    # the difference between indoor and outdoor air temperature, and the outdoor brightness
    R272_Window_Override = np.minimum(np.round(R272_occupants * np.maximum((R272_Air_Temperature - 26), 0)) * np.absolute(R272_Air_Temperature - Weather_DryBulb_Temperature), 1)
    # changing the thermostat of bedroom #1 (R272) based on indoor air temperature
    if R272_Air_Temperature > 26:
        R272_SetPoint_Override = 14
    elif R272_Air_Temperature < 20:
        R272_SetPoint_Override = 32
    else:
        R272_SetPoint_Override = np.NAN

    # see comments for Bedroom #1 above (lines 152 - 156)
    R273_gains_human = R273_occupants * activity_schedule[hour_of_simulation_time]
    R273_gain_lighting = R273_occupants * (1 - brightness)
    R273_gain_equipment = R273_occupants * activity_schedule[hour_of_simulation_time] + 0.2
    R273_Occupant_Operation = R273_gains_human + R273_gain_lighting + R273_gain_equipment
    R273_Shade_Override = np.round(R273_occupants * np.maximum(R273_Air_Temperature - 26, 0) * brightness)
    R273_Window1_Override = np.minimum(np.round(R273_occupants * np.maximum((R273_Air_Temperature - 26), 0)) * np.absolute(R273_Air_Temperature - Weather_DryBulb_Temperature), 1)
    R273_Window2_Override = np.minimum(np.round(R273_occupants * np.maximum((R273_Air_Temperature - 26), 0)) * np.absolute(R273_Air_Temperature - Weather_DryBulb_Temperature), 1)
    if R273_Air_Temperature > 26:
        R273_SetPoint_Override = 14
    elif R273_Air_Temperature < 20:
        R273_SetPoint_Override = 32
    else:
        R273_SetPoint_Override = np.NAN

    # see comments for Bedroom #1 above (lines 152 - 156)
    R274_gains_human = R274_occupants * activity_schedule[hour_of_simulation_time]
    R274_gain_lighting = R274_occupants * (1 - brightness)
    R274_gain_equipment = R274_occupants * activity_schedule[hour_of_simulation_time] + 0.1
    R274_Occupant_Operation = R274_gains_human + R274_gain_lighting + R274_gain_equipment
    R274_Shade_Override = np.round(R274_occupants * np.maximum(R274_Air_Temperature - 26, 0) * brightness)
    R274_Window_Override = np.minimum(np.round(R274_occupants * np.maximum((R274_Air_Temperature - 26), 0)) * np.absolute(R274_Air_Temperature - Weather_DryBulb_Temperature), 1)
    if R274_Air_Temperature > 26:
        R274_SetPoint_Override = 14
    elif R274_Air_Temperature < 20:
        R274_SetPoint_Override = 32
    else:
        R274_SetPoint_Override = np.NAN

    return (
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
    )
