from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
import numpy as np
import shutil
from input_functions import create_dict_from_file, read_csv_files_in_folder

START_TIME = 0
STOP_TIME = 4*86400
STEP_SIZE = 60


def simulate_custom_input(main_filename, preprocess_filename, variable_mapping_1, variable_mapping_2, variable_mapping_3, preprocess_input):

    # read the model description main_fmu
    main_model_description = read_model_description(main_filename)

    # collect the value references main_fmu
    vrs_main = {}
    for variable in main_model_description.modelVariables:
        vrs_main[variable.name] = variable.valueReference

    # extract the main_fmu
    main_unzipdir = extract(main_filename)
    main_fmu = FMU2Slave(guid=main_model_description.guid,
                    unzipDirectory=main_unzipdir,
                    modelIdentifier=main_model_description.coSimulation.modelIdentifier,
                    instanceName='instance1')
    # initialize main_fmu
    main_fmu.instantiate()
    main_fmu.setupExperiment(startTime=START_TIME, stopTime=STOP_TIME)
    main_fmu.enterInitializationMode()
    main_fmu.exitInitializationMode()


    # read the model description preprocess
    preprocess_model_description = read_model_description(preprocess_filename)
    vrs_preprocess = {}
    for variable in preprocess_model_description.modelVariables:
        vrs_preprocess[variable.name] = variable.valueReference

    # extract the preprocess FMU
    preprocess_unzipdir = extract(preprocess_filename)
    preprocess_fmu = FMU2Slave(guid=preprocess_model_description.guid,
                    unzipDirectory=preprocess_unzipdir,
                    modelIdentifier=preprocess_model_description.coSimulation.modelIdentifier,
                    instanceName='instance2')
    # initialize preprocess fmu
    preprocess_fmu.instantiate()
    preprocess_fmu.setupExperiment(startTime=START_TIME, stopTime=STOP_TIME)
    preprocess_fmu.enterInitializationMode()
    preprocess_fmu.exitInitializationMode()


    time = START_TIME
    rows = [] 
    # simulation loop
    while time < STOP_TIME:
        # NOTE: the FMU.get*() and FMU.set*() functions take lists of
        # value references as arguments and return lists of values
        for key, value in variable_mapping_1.items():
            main_fmu.setReal([vrs_main[key]], preprocess_fmu.getReal([vrs_preprocess[value]]))

        for key, value in variable_mapping_2.items():
            preprocess_fmu.setReal([vrs_preprocess[key]], main_fmu.getReal([vrs_main[value]]))
        
        for key, value in variable_mapping_3.items():
            preprocess_fmu.setReal([vrs_preprocess[key]], [preprocess_input.at[(int)(time/60), value]])

        # perform one step
        main_fmu.doStep(currentCommunicationPoint=time, communicationStepSize=STEP_SIZE)
        preprocess_fmu.doStep(currentCommunicationPoint=time, communicationStepSize=STEP_SIZE)
        
        time += STEP_SIZE       

        # append the results
        [Flow_R274_H] =  preprocess_fmu.getReal([vrs_preprocess["Flow_R274_H"]])
        [T_WC275] = main_fmu.getReal([vrs_main["T_WC275"]])
        rows.append((time, Flow_R274_H, T_WC275))
        

    main_fmu.terminate()
    main_fmu.freeInstance()

    preprocess_fmu.terminate()
    preprocess_fmu.freeInstance()

    # clean up
    shutil.rmtree(main_unzipdir, ignore_errors=True)
    shutil.rmtree(preprocess_unzipdir, ignore_errors=True)

    # convert the results to a structured NumPy array
    result = np.array(rows, dtype=np.dtype([('time', np.float64), ('preprocess_Flow_R274_H', np.float64), ('main_T_WC275', np.float64)]))

    plot_result(result)

    return time





if __name__ == '__main__':
    fmu_filename_1 = './inputs/fmu/UMAR.fmu'
    fmu_filename_2 = './inputs/fmu/preprocess.fmu'
    mapping_dict_1 = create_dict_from_file("./inputs/mappings/mapping_umar_from_preprocess.txt")
    mapping_dict_2 = create_dict_from_file("./inputs/mappings/mapping_preprocess_from_umar.txt")
    mapping_dict_3 = create_dict_from_file("./inputs/mappings/mapping_preprocess_from_data.txt")
    preprocess_input = read_csv_files_in_folder("./inputs/data")
    simulate_custom_input(fmu_filename_1, fmu_filename_2, mapping_dict_1, mapping_dict_2, mapping_dict_3, preprocess_input)