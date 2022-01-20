# DTpy
DTpy is a co-simulation environment for benchmarking the performance of BACS (building automation and control systems). In its core, DTpy is a calibrated EnergyPlus model of the living lab UMAR (urban mining and recycling) at NEST, Empa. see: https://www.empa.ch/web/nest/urban-mining

The calibrated EnergyPlus model is wrapped into an FMU (fucntional mock-up unit) using the EnergyPlusToFMU tool. see: https://simulationresearch.lbl.gov/fmu/EnergyPlus/export/

The model is calibrated on measurements that are collected at 1-minute intervals, and thus runs at the same temporal resolution. The HVAC system can be controlled by oversteering the setpoint temperature in each room. It is also possible to evaluate the robustness of the controller by manipulating weather conditions and building operation.
