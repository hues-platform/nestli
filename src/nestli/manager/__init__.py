MOSAIK_CONFIG = {
    "FMU": {"python": "nestli.simulators.FmuAdapter:FmuAdapter"},
    "TABULAR_DATA": {"python": "nestli.simulators.TabularDataSimPandas:TabularData"},
    "COLLECTOR": {"python": "nestli.simulators.Collector:Collector"},
    "NAN_PLACEHOLDER": {"python": "nestli.simulators.NanPlaceholder:NanPlaceholder"},
    "CONSTANT_VALUE": {"python": "nestli.simulators.ConstantValue:ConstantValue"},
    "DATABASE_DATA": {"python": "nestli.simulators.DataBaseData:DataBaseData"},
    "OCCUPANT": {"python": "nestli.simulators.Occupant:Occupant"},
}

DATA_DOWNLOAD = "https://polybox.ethz.ch/index.php/s/GwRGak2YfMb8nXm/download"
