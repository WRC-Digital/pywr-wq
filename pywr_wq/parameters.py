import os
from pywr.parameters._parameters import Parameter
import numpy as np
import pandas


class WQConcentrationParameter(Parameter):
    """Parameter that obtains the current concentration of TDS from Pywr-WQ"""

    def __init__(self, model, node_name: str, determinand: str, **kwargs):
        super().__init__(model, **kwargs)
        self.node_name = node_name
        self.determinand = determinand        
        self._wq_model = None

    def setup(self):
        super().setup()
        # Find the references to the other model and one of its parameters.
        self._wq_model = self.model.parent.wq_model

    def value(self, ts, scenario_index):
        # TODO support multiple-scenarios
        return self._wq_model.get_concentration(self.node_name, self.determinand)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)

WQConcentrationParameter.register()