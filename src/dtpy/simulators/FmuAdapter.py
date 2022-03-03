import itertools
import os
import shutil
import mosaik_api
import dtpy.simulators.parse_xml as parse_xml
from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from dtpy.simulators.fmi_logging import get_callbacks_logger

meta = {
    "type": "time-based",
    'models': {
    },
    'extra_methods': ['fmi_set', 'fmi_get']
}

'''
var_table = {
    'parameter': {
        'a': 'Real',
        'b': 'Integer',
        'c': 'Boolean',
        'd': 'String'
    },
    'input': {
        'x': 'Real',
        ...
    },
    'output': {
        ...
    }
}
'''


class FmuAdapter(mosaik_api.Simulator):
    '''Mosaik adapter for simulators following the FMI for Co-Simulation / ModelExchange standard.'''

    def __init__(self):
        super(FmuAdapter, self).__init__(meta)
        self.sid = None

        self._entities = {}
        self.eid_counters = {}

    def init(self, sid, work_dir=None, fmu_name=None, model_name=None, instance_name=None, time_resolution=1, logging_on=False,
             step_factor=1.0, var_table=None, translation_table=None,
             time_diff_resolution=1e-9, interactive=False, visible=False, stop_time_defined=False, stop_time=1):

        if work_dir is None or model_name is None or fmu_name is None or instance_name is None:
            raise RuntimeError("FMI Adapter has to be initialized with work_dir, fmu_name, model_name, instance_name!")
        self.sid = sid

        self.work_dir = work_dir  # path to directory of the FMU
        self.fmu_name = fmu_name
        self.model_name = model_name
        self.instance_name = instance_name
        self.step_size = time_resolution
        self.step_factor = step_factor  # Factor to translate mosaik integer time into FMI float time
        self.logging_on = logging_on
        #self.fmi_version = fmi_version

        # Co-simulation-specific variables:
        self.start_time = 0
        self.time_diff_resolution = time_diff_resolution
        self.interactive = interactive
        self.visible = visible
        self.stop_time_defined = stop_time_defined
        self.stop_time = stop_time


        # Extracting files from the .fmu (only needed at first use, but will not cause error later)
        path_to_fmu = os.path.join(self.work_dir, self.fmu_name + '.fmu')
        self.uri_to_extracted_fmu = extract(path_to_fmu, os.path.join(self.work_dir, self.fmu_name))
        
        self.model_description = read_model_description(path_to_fmu)
        self.vrs = {}
        for variable in self.model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference

        # FMU variables may be either given by the user or are read automatically from FMU description file:
        xmlfile = os.path.join(self.work_dir, self.fmu_name, 'modelDescription.xml')
        if var_table is None:
            self.var_table, self.translation_table = parse_xml.get_var_table(xmlfile)
        else:
            self.var_table = var_table
            self.translation_table = translation_table  # If variables are specified by hand, a translation table  #
            # also has to be given (in case some FMI variable names are not python-conform)

        self.fmi_type = "CoSimulation"
        
        self.adjust_var_table()  # Completing var_table and translation_table structure
        self.adjust_meta()  # Writing variable information into mosaik's meta
        return self.meta

    def create(self, num, model, **model_params):
        counter = self.eid_counters.setdefault(model, itertools.count())

        entities = []

        for i in range(num):
            eid = '%s_%s' % (model, next(counter))

            fmu = FMU2Slave(guid=self.model_description.guid,
                    unzipDirectory=self.uri_to_extracted_fmu,
                    modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                    instanceName=self.instance_name, fmiCallLogger=None)
            self._entities[eid] = fmu
            callbacks = get_callbacks_logger(self.logging_on)
            self._entities[eid].instantiate(visible=self.visible, loggingOn=self.logging_on, callbacks=callbacks)
            self._entities[eid].setupExperiment(startTime=self.start_time, stopTime=self.stop_time)
            self._entities[eid].enterInitializationMode()
            self._entities[eid].exitInitializationMode()

            #self.set_values(eid, model_params, 'parameter')

            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs, max_advance):
        if self.fmi_type=="CoSimulation":
            # If no input data is provided, all entities are stepped:
            if inputs is None or inputs == {}:
                for fmu in self._entities.values():
                    fmu.doStep(t * self.step_factor, self.step_size * self.step_factor, True)

            else:
                for eid, attrs in inputs.items():
                    for attr, vals in attrs.items():
                        for val in vals.values():
                            self.set_values(eid, {attr: val}, 'input')

                    self._entities[eid].doStep(t * self.step_factor, self.step_size * self.step_factor, True)
                    
            return t + self.step_size

    def finalize(self):        
        for key, value in self._entities.items():
            value.terminate()
            value.freeInstance()
        shutil.rmtree(self.uri_to_extracted_fmu, ignore_errors=True)
        return super().finalize()


    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.get_value(eid, attr)

        return data



    def adjust_var_table(self):
        '''Help function that completes the structure of var_table and translation_tabel. Both require listing of
        the three variable types, parameter, input and output.'''
        self.var_table.setdefault('parameter', {})
        self.var_table.setdefault('input', {})
        self.var_table.setdefault('output', {})

        # A translation table is needed since sometimes FMU variable names are not accepted by mosaik 
        # (e.g. containing a period)
        self.translation_table.setdefault('parameter', {})
        self.translation_table.setdefault('input', {})
        self.translation_table.setdefault('output', {})

    def adjust_meta(self):
        '''Help function that writes FMU variable names into the mosaik meta structure.'''
        # FMU inputs and outputs are translated to attributes in mosaik
        attr_list = list(self.translation_table['input'].keys())
        out_list = list(self.translation_table['output'].keys())
        attr_list.extend(out_list)

        self.meta['models'][self.instance_name] = {
            'public': True,
            'params': list(self.translation_table['parameter'].keys()),
            'attrs': attr_list
        }

    def set_values(self, eid, val_dict, var_type):
        '''Help function to set values to a given variable of an FMU. This is done via a "var_table" and a
        "translation_table" to avoid problems due to missmatching naming conventions in mosaik and FMI.'''
        for alt_name, val in val_dict.items():
            name = self.translation_table[var_type][alt_name]
            set_func = getattr(self._entities[eid], 'set' + self.var_table[var_type][name])
            set_stat = set_func([self.vrs[name]], [val])

    def get_value(self, eid, alt_attr):
        '''Help function to get values from given variables of an FMU.'''
        attr = self.translation_table['output'][alt_attr]
        get_func = getattr(self._entities[eid], 'get' + self.var_table['output'][attr])
        [val] = get_func([self.vrs[attr]])
        return val

    def fmi_set(self, entity, var_name, value, var_type='input'):
        '''Extra function to allow explicit setting by user in scenario file.'''
        var_dict = {var_name: value}
        self.set_values(entity.eid, var_dict, var_type)

    def fmi_get(self, entity, var_name):
        '''Extra function to allow explicit getting by user in scenario file.'''
        val = self.get_value(entity.eid, var_name)
        return val
