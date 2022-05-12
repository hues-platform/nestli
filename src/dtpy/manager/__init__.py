MOSAIK_CONFIG = {
    "FMU": {"python": "dtpy.simulators.FmuAdapter:FmuAdapter"},
    "TABULAR_DATA": {"python": "dtpy.simulators.TabularDataSimPandas:TabularData"},
    "COLLECTOR": {"python": "dtpy.simulators.Collector:Collector"},
    "NAN_PLACEHOLDER": {"python": "dtpy.simulators.NanPlaceholder:NanPlaceholder"},
    "CONSTANT_VALUE": {"python": "dtpy.simulators.ConstantValue:ConstantValue"},
}
