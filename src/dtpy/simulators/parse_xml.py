import xml.etree.ElementTree as ETree

def get_var_table(filename):
    '''This function reads the XML description file of an FMU, extracts the variable
    information and stores it in dict structures for the mosaik adapter to read.'''
    var_table = {}
    translation_table = {}

    base = ETree.parse(filename).getroot()
    mvars = base.find('ModelVariables')

    for var in mvars.findall('ScalarVariable'):
        causality = var.get('causality')
        name = var.get('name')
        if causality in ['input', 'output', 'parameter']:
            var_table.setdefault(causality, {})
            translation_table.setdefault(causality, {})
            # Mosaik requires python-conform variable naming (no periods)
            if '.' in name:
                alt_name = name.replace('.', '_')
            else:
                alt_name = name
            translation_table[causality][alt_name] = name
            
            # In practice, input variables may sometimes be used as
            # parameters and vice versa (typically due to unclear FMU design)
            if causality == 'input':
                var_table.setdefault('parameter', {})
                translation_table.setdefault('parameter', {})
                translation_table['parameter'][alt_name] = name
            if causality == 'parameter':
                var_table.setdefault('input', {})
                translation_table.setdefault('input', {})
                translation_table['input'][alt_name] = name

            # 
            specs = list(var)
            for spec in specs:
                if spec.tag in ['Real', 'Integer', 'Boolean', 'String']:
                    var_table[causality][name] = spec.tag
                    # See above (parameters <--> inputs):
                    if causality == 'input':
                        var_table['parameter'][name] = spec.tag
                    if causality == 'parameter':
                        var_table['input'][name] = spec.tag
                    continue

    return var_table, translation_table


def get_fmi_version(filename):
    base = ETree.parse(filename).getroot()
    version = base.get('fmiVersion')
    version = version.split('.')[0]
    return version
