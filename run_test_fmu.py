from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
import numpy as np
import shutil


def simulate_custom_input(show_plot=True):

    # define the model name and simulation parameters
    fmu_filename = 'UMAR.fmu'
    start_time = 0
    stop_time = 10*86400
    step_size = 60


    # read the model description
    model_description = read_model_description(fmu_filename)

    # collect the value references
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference


    # get the value references for the variables we want to get/set
    DryBulb_T = vrs['DryBulb_T']
    DewPoint_T = vrs['DewPoint_T']
    Rel_Hum = vrs['Rel_Hum']
    Diff_Rad = vrs['Diff_Rad']
    Dir_Rad = vrs['Dir_Rad']
    Wind_Spd = vrs['Wind_Spd']
    Wind_Dir = vrs['Wind_Dir']
    Occ_R272 = vrs['Occ_R272']
    Occ_R273 = vrs['Occ_R273']
    Occ_R274 = vrs['Occ_R274']
    Flow_272_H = vrs['Flow_272_H']
    Flow_272_C = vrs['Flow_272_C']
    Flow_273_H = vrs['Flow_273_H']
    Flow_273_C = vrs['Flow_273_C']
    Flow_274_H = vrs['Flow_274_H']
    Flow_274_C = vrs['Flow_274_C']
    Flow_275_H = vrs['Flow_275_H']
    Flow_275_C = vrs['Flow_275_C']
    Flow_276_H = vrs['Flow_276_H']
    Flow_276_C = vrs['Flow_276_C']
    DH_pump_flow = vrs['DH_pump_flow']
    DC_pump_flow = vrs['DC_pump_flow']
    Shade_272 = vrs['Shade_272']
    Shade_273 = vrs['Shade_273']
    Shade_274 = vrs['Shade_274']
    WIN_272 = vrs['WIN_272']
    WIN1_273 = vrs['WIN1_273']
    WIN2_273 = vrs['WIN2_273']
    WIN_274 = vrs['WIN_274']
    SP_272 = vrs['SP_272']
    SP_273 = vrs['SP_273']
    SP_274 = vrs['SP_274']
    SP_275 = vrs['SP_275']
    SP_276 = vrs['SP_276']
    DH_supply_temperature = vrs['DH_supply_temperature']
    DC_supply_temperature = vrs['DC_supply_temperature']
    DH_plnt_switch = vrs['DH_plnt_switch']
    DC_plnt_switch = vrs['DC_plnt_switch']

    Outlet_Bed272 = vrs['Outlet_Bed272']
    Inlet_Bed272 = vrs['Inlet_Bed272']
    Outlet_Living273 = vrs['Outlet_Living273']
    Inlet_Living273 = vrs['Inlet_Living273']
    Outlet_Bed274 = vrs['Outlet_Bed274']
    Inlet_Bed274 = vrs['Inlet_Bed274']
    Outlet_WC275 = vrs['Outlet_WC275']
    Inlet_WC275 = vrs['Inlet_WC275']
    Outlet_WC276 = vrs['Outlet_WC276']
    Inlet_WC276 = vrs['Inlet_WC276']
    T_Bed272 = vrs['T_Bed272']
    Sol_Bed272 = vrs['Sol_Bed272']
    T_Living273 = vrs['T_Living273']
    Sol_Living273 = vrs['Sol_Living273']
    T_Bed274 = vrs['T_Bed274']
    Sol_Bed274 = vrs['Sol_Bed274']
    T_WC275 = vrs['T_WC275']
    T_WC276 = vrs['T_WC276']
    DH_supply_t = vrs['DH_supply_t']
    DH_return_temperature = vrs['DH_return_temperature']
    DH_supply_flow = vrs['DH_supply_flow']
    DC_supply_t = vrs['DC_supply_t']
    DC_return_temperature = vrs['DC_return_temperature']
    DC_supply_flow = vrs['DC_supply_flow']


# extract the FMU
    unzipdir = extract(fmu_filename)

    fmu = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.coSimulation.modelIdentifier,
                    instanceName='instance1')

    # initialize
    fmu.instantiate()
    fmu.setupExperiment(startTime=start_time, stopTime=stop_time)
    fmu.enterInitializationMode()
    fmu.exitInitializationMode()

    time = start_time

    rows = []  # list to record the results

    # simulation loop
    while time < stop_time:

        # NOTE: the FMU.get*() and FMU.set*() functions take lists of
        # value references as arguments and return lists of values

        # set the input
        DryBulb_T1 = 0 if time % 100000 < 50000 else 1
        DewPoint_T1 = 0 if time % 100000 < 50000 else 1
        Rel_Hum1 = 0 if time % 100000 < 50000 else 1
        Diff_Rad1 = 0 if time % 100000 < 50000 else 1
        Dir_Rad1 = 0 if time % 100000 < 50000 else 1
        Wind_Spd1 = 0 if time % 100000 < 50000 else 1
        Wind_Dir1 = 0 if time % 100000 < 50000 else 1
        Occ_R2721 = 0 if time % 100000 < 50000 else 1
        Occ_R2731 = 0 if time % 100000 < 50000 else 1
        Occ_R2741 = 0 if time % 100000 < 50000 else 1
        Flow_272_H1 = 0 if time % 100000 < 50000 else 1
        Flow_272_C1 = 0 if time % 100000 < 50000 else 1
        Flow_273_H1 = 0 if time % 100000 < 50000 else 1
        Flow_273_C1 = 0 if time % 100000 < 50000 else 1
        Flow_274_H1 = 0 if time % 100000 < 50000 else 1
        Flow_274_C1 = 0 if time % 100000 < 50000 else 1
        Flow_275_H1 = 0 if time % 100000 < 50000 else 1
        Flow_275_C1 = 0 if time % 100000 < 50000 else 1
        Flow_276_H1 = 0 if time % 100000 < 50000 else 1
        Flow_276_C1 = 0 if time % 100000 < 50000 else 1
        DH_pump_flow1 = 0 if time % 100000 < 50000 else 1
        DC_pump_flow1 = 0 if time % 100000 < 50000 else 1
        Shade_2721 = 0 if time % 100000 < 50000 else 1
        Shade_2731 = 0 if time % 100000 < 50000 else 1
        Shade_2741 = 0 if time % 100000 < 50000 else 1
        WIN_2721 = 0 if time % 100000 < 50000 else 1
        WIN1_2731 = 0 if time % 100000 < 50000 else 1
        WIN2_2731 = 0 if time % 100000 < 50000 else 1
        WIN_2741 = 0 if time % 100000 < 50000 else 1
        SP_2721 = 0 if time % 100000 < 50000 else 1
        SP_2731 = 0 if time % 100000 < 50000 else 1
        SP_2741 = 0 if time % 100000 < 50000 else 1
        SP_2751 = 0 if time % 100000 < 50000 else 1
        SP_2761 = 0 if time % 100000 < 50000 else 1
        DH_supply_temperature1 = 0 if time % 100000 < 50000 else 1
        DC_supply_temperature1 = 0 if time % 100000 < 50000 else 1
        DH_plnt_switch1 = 0 if time % 100000 < 50000 else 1
        DC_plnt_switch1 = 0 if time % 100000 < 50000 else 1

        fmu.setReal([DryBulb_T], [DryBulb_T1])
        fmu.setReal([DewPoint_T], [DewPoint_T1])
        fmu.setReal([Rel_Hum], [Rel_Hum1])
        fmu.setReal([Diff_Rad], [Diff_Rad1])
        fmu.setReal([Dir_Rad], [Dir_Rad1])
        fmu.setReal([Wind_Spd], [Wind_Spd1])
        fmu.setReal([Wind_Dir], [Wind_Dir1])
        fmu.setReal([Occ_R272], [Occ_R2721])
        fmu.setReal([Occ_R273], [Occ_R2731])
        fmu.setReal([Occ_R274], [Occ_R2741])
        fmu.setReal([Flow_272_H], [Flow_272_H1])
        fmu.setReal([Flow_272_C], [Flow_272_C1])
        fmu.setReal([Flow_273_H], [Flow_273_H1])
        fmu.setReal([Flow_273_C], [Flow_273_C1])
        fmu.setReal([Flow_274_H], [Flow_274_H1])
        fmu.setReal([Flow_274_C], [Flow_274_C1])
        fmu.setReal([Flow_275_H], [Flow_275_H1])
        fmu.setReal([Flow_275_C], [Flow_275_C1])
        fmu.setReal([Flow_276_H], [Flow_276_H1])
        fmu.setReal([Flow_276_C], [Flow_276_C1])
        fmu.setReal([DH_pump_flow], [DH_pump_flow1])
        fmu.setReal([DC_pump_flow], [DC_pump_flow1])
        fmu.setReal([Shade_272], [Shade_2721])
        fmu.setReal([Shade_273], [Shade_2731])
        fmu.setReal([Shade_274], [Shade_2741])
        fmu.setReal([WIN_272], [WIN_2721])
        fmu.setReal([WIN1_273], [WIN1_2731])
        fmu.setReal([WIN2_273], [WIN2_2731])
        fmu.setReal([WIN_274], [WIN_2741])
        fmu.setReal([SP_272], [SP_2721])
        fmu.setReal([SP_273], [SP_2731])
        fmu.setReal([SP_274], [SP_2741])
        fmu.setReal([SP_275], [SP_2751])
        fmu.setReal([SP_276], [SP_2761])
        fmu.setReal([DH_supply_temperature], [DH_supply_temperature1])
        fmu.setReal([DC_supply_temperature], [DC_supply_temperature1])
        fmu.setReal([DH_plnt_switch], [DH_plnt_switch1])
        fmu.setReal([DC_plnt_switch], [DC_plnt_switch1])

        # perform one step
        fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)
        # [sim_Q, sim_TRooMea] = fmu.getReal([DryBulb_T1, DewPoint_T1, Rel_Hum1, Diff_Rad1, Dir_Rad1, Wind_Spd1,
        #                                     Wind_Dir1, Occ_R2721, Occ_R2731, Occ_R2741, Flow_272_H1, Flow_272_C1,
        #                                     Flow_273_H1, Flow_273_C1, Flow_274_H1, Flow_274_C1, Flow_275_H1,
        #                                     Flow_275_C1, Flow_276_H1, Flow_276_C1, DH_pump_flow1, DC_pump_flow1,
        #                                     Shade_2721, Shade_2731, Shade_2741, WIN_2721, WIN1_2731, WIN2_2731,
        #                                     WIN_2741, SP_2721, SP_2731, SP_2741, SP_2751, SP_2761,
        #                                     DH_supply_temperature1, DC_supply_temperature1, DH_plnt_switch1,
        #                                     DC_plnt_switch1, TRooMea])
        Outlet_Bed2721 = fmu.getReal([Outlet_Bed272])
        Inlet_Bed2721 = fmu.getReal([Inlet_Bed272])
        Outlet_Living2731 = fmu.getReal([Outlet_Living273])
        Inlet_Living2731 = fmu.getReal([Inlet_Living273])
        Outlet_Bed2741 = fmu.getReal([Outlet_Bed274])
        Inlet_Bed2741 = fmu.getReal([Inlet_Bed274])
        Outlet_WC2751 = fmu.getReal([Outlet_WC275])
        Inlet_WC2751 = fmu.getReal([Inlet_WC275])
        Outlet_WC2761 = fmu.getReal([Outlet_WC276])
        Inlet_WC2761 = fmu.getReal([Inlet_WC276])
        T_Bed2721 = fmu.getReal([T_Bed272])
        Sol_Bed2721 = fmu.getReal([Sol_Bed272])
        T_Living2731 = fmu.getReal([T_Living273])
        Sol_Living2731 = fmu.getReal([Sol_Living273])
        T_Bed2741 = fmu.getReal([T_Bed274])
        Sol_Bed2741 = fmu.getReal([Sol_Bed274])
        T_WC2751 = fmu.getReal([T_WC275])
        T_WC2761 = fmu.getReal([T_WC276])
        DH_supply_t1 = fmu.getReal([DH_supply_t])
        DH_return_temperature1 = fmu.getReal([DH_return_temperature])
        DH_supply_flow1 = fmu.getReal([DH_supply_flow])
        DC_supply_t1 = fmu.getReal([DC_supply_t])
        DC_return_temperature1 = fmu.getReal([DC_return_temperature])
        DC_supply_flow1 = fmu.getReal([DC_supply_flow])

    # advance the time
        time += step_size
        
        # get the values for 'inputs' and 'outputs'
        

        # append the results
        rows.append((time, DryBulb_T1, DewPoint_T1, Rel_Hum1, Diff_Rad1, Dir_Rad1, Wind_Spd1, Wind_Dir1, Occ_R2721,
                     Occ_R2731, Occ_R2741, Flow_272_H1, Flow_272_C1, Flow_273_H1, Flow_273_C1, Flow_274_H1,
                     Flow_274_C1, Flow_275_H1, Flow_275_C1, Flow_276_H1, Flow_276_C1, DH_pump_flow1, DC_pump_flow1,
                     Shade_2721, Shade_2731, Shade_2741, WIN_2721, WIN1_2731, WIN2_2731, WIN_2741, SP_2721, SP_2731,
                     SP_2741, SP_2751, SP_2761, DH_supply_temperature1, Outlet_Bed2721, Inlet_Bed2721,
                     Outlet_Living2731, Inlet_Living2731, Outlet_Bed2741, Inlet_Bed2741, Outlet_WC2751,
                     Inlet_WC2751, Outlet_WC2761, Inlet_WC2761, T_Bed2721,  Sol_Bed2721, T_Living2731, Sol_Living2731,
                     T_Bed2741, Sol_Bed2741, T_WC2751, T_WC2761, DH_supply_t1, DH_return_temperature1,
                     DH_supply_flow1, DC_supply_t1, DC_return_temperature1, DC_supply_flow1))

    fmu.terminate()
    fmu.freeInstance()

    # clean up
    shutil.rmtree(unzipdir, ignore_errors=True)

    # convert the results to a structured NumPy array
    # result = np.array(rows, dtype=np.dtype([('time', np.float64), ('Q', np.float64), ('TRooMea', np.float64)]))

    # plot the results
    # if show_plot:
    #     plot_result(result)

    return time


if __name__ == '__main__':

    simulate_custom_input()