# nestli
nestli is the virtual sister of the NEST demonstrator at Empa. It is a co-simulation environment for benchmarking the performance of BACS (building automation and control systems). In its core, nestli is a calibrated EnergyPlus model of the UMAR living lab. see: https://www.empa.ch/web/nest/urban-mining

![Picture1](https://user-images.githubusercontent.com/27851066/169803496-275ed8fc-7d1b-42e6-a0a7-f27f7dc456c5.png)

The calibrated EnergyPlus model is wrapped into an FMU (fucntional mock-up unit) using the EnergyPlusToFMU tool. see: https://simulationresearch.lbl.gov/fmu/EnergyPlus/export/

The model is calibrated on measurements that are collected at 1-minute intervals, and thus runs at the same temporal resolution. The HVAC system can be controlled by overriding the setpoint temperature in each room. It is also possible to evaluate the robustness of the controller by manipulating weather conditions and building operation.

![Picture3](https://user-images.githubusercontent.com/27851066/177743252-245372b8-5d8f-46c5-a06d-f375e4154ec1.png)

## Installation
The installation consists of 3 Steps.

1. EnergyPlus
2. Python
3. install the nestli package

Further installation informations are in the pdf documentation.

## Usage
A simple example of how to use the package is given in the **example** folder. Just run the file nestli_example_run.py where the config example_config.yml specifies all the parameters.
