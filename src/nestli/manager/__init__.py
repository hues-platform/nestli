MOSAIK_CONFIG = {
    "FMU": {"python": "nestli.simulators.FmuAdapter:FmuAdapter"},
    "TABULAR_DATA": {"python": "nestli.simulators.TabularDataSimPandas:TabularData"},
    "COLLECTOR": {"python": "nestli.simulators.Collector:Collector"},
    "NAN_PLACEHOLDER": {"python": "nestli.simulators.NanPlaceholder:NanPlaceholder"},
    "CONSTANT_VALUE": {"python": "nestli.simulators.ConstantValue:ConstantValue"},
    "DATABASE_DATA": {"python": "nestli.simulators.DataBaseData:DataBaseData"},
    "PYTHON_FUNCTION": {"python": "nestli.simulators.PythonFunction:PythonFunction"},
    "DATABASE_DATA_FORECAST": {"python": "nestli.simulators.DataBaseDataForecast:DataBaseDataForecast"},
}

DATA_DOWNLOAD = "https://polybox.ethz.ch/index.php/s/QgaDRyA2oXoFs1C/download"
