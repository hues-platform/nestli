###########
Usage
###########

Overview
###########
The simulation is handled, initialized and started my the Manager class.

To run a simulation, you need to start a Manager instance with a config file. The config file specifies all simulation parameters.

Script
---------
The following python script is all that is needed for a simulation. 

.. code-block:: python

    example_manager = Manager("example_config.yml")
    example_manager.build_simulation()
    example_manager.run()


Config file
-------------
The config file is a yaml file in which the simulation parameters are set. It first specifies some general parameters. 

.. code-block:: yaml

    OUTPUT_FOLDER_PATH: ""
    START: '2022-05-12'
    DURATION: 864000
    RESOLUTION: 60

For an EnergyPlus model the DURATION has to be a multiple of 86400 and the RESOLUTION must be the same as the model resolution.

After that all the simulators are specified. 
A PATH can either be absolute or relative to the config file folder path or if it is in the nestli package you can see the example below.

.. code-block:: yaml

    # The Simulators specify all the models in the simulation. Currently the following simulators are available:
    #   FMU:  This will create a simulator from an FMU. 
    #         PATH specifies the folder where the FMU is contained and NAME the filename.
    #   TABULAR_DATA: This will create a simulator from DATA in tabular form. The supported format is hdf5.
    #         PATH specifies the folder where the .h5 files are contained. The file name must correspond with the variable name of the data it containes.
    #   NAN_PLACEHOLDER: This simulator will create a NaN value to all connected entities.
    #         PATH specifies a file which containes all the variables you plan to connect to it.      
    #   COLLECTOR: This is a simple Data collector. It will save the data of all signals you connect to it and write them to a file after the simulation.
    #         No additional information is neccessary.
    
    SIMULATORS: 
        SIM1:
            NAME: "UMAR"
            TYPE: "FMU"
            PATH: "$nestli$./simulators/ressources/fmu"
            NUMBER_OF_MODELS: 5


Last all the connections between the simulators are defined. For each simulator you specify all the outgoing signals.

.. code-block:: yaml

    MAPPINGS:
        SIGNALS_OUTGOING_FROM_UMAR:
            FROM: SOURCE
            MAPPINGS:
                # A simple mapping
                MAPPING1:
                    TO: DESTINATION
                    VARIABLES:    
                        SOURCE_VARIABLE_NAME_1: DESTINATION_VARIABLE_NAME_1
                        SOURCE_VARIABLE_NAME_2: DESTINATION_VARIABLE_NAME_2
                # A mapping with circular dependency and multiple models and thus an index has to be specified
                MAPPING2:
                    TO: DESTINATION
                    INDEX: 0
                    CIRCULAR_DEPENDENDY: TRUE
                    INITIAL_VALUES:
                        SOURCE_VARIABLE_NAME: 24.5669
                    VARIABLES:    
                        SOURCE_VARIABLE_NAME: DESTINATION_VARIABLE_NAME


Run Simulation
###############

Local python
-------------
To run in locally you can just run the python file you created.

Docker
-------
To run with Docker you first need to create an image with:
::

    docker build . -t nestli

This is further described in the installation section.


You run a container specifying your source file path with PATH_TO_PROJECT_FOLDER with:
::
    
    docker run -it -v "PATH_TO_PROJECT_FOLDER:/example_folder" nestli

This folder must contain a python file called nestli_example_run.py and your config file and other files your simulation needs.
It will be copied to the container and the results will get copied back to it.