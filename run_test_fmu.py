from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
import numpy as np
import shutil


def simulate_custom_input(show_plot=True):

    # define the model name and simulation parameters
    fmu_filename = 'test.fmu'
    start_time = 0
    stop_time = 10*86400
    step_size = 900


    # read the model description
    model_description = read_model_description(fmu_filename)

    # collect the value references
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference


    # get the value references for the variables we want to get/set
    Q_var   = vrs['Q']      
    TRooMea = vrs['TRooMea']  
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
        Qval = 0 if time % 100000 < 50000 else 1000

        fmu.setReal([Q_var], [Qval])
        
        # perform one step
        fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)
        [sim_Q, sim_TRooMea] = fmu.getReal([Q_var, TRooMea])
        # advance the time
        time += step_size
        
        # get the values for 'inputs' and 'outputs'
        

        # append the results
        rows.append((time, Qval, sim_TRooMea))

    fmu.terminate()
    fmu.freeInstance()

    # clean up
    shutil.rmtree(unzipdir, ignore_errors=True)

    # convert the results to a structured NumPy array
    result = np.array(rows, dtype=np.dtype([('time', np.float64), ('Q', np.float64), ('TRooMea', np.float64)]))

    # plot the results
    if show_plot:
        plot_result(result)

    return time


if __name__ == '__main__':

    simulate_custom_input()