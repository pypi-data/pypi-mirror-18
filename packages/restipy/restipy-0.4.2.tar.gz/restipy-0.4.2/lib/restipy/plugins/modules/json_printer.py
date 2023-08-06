import json, functools

from functools import partial

from restipy.core.modules import RestipyModule

class JsonPrinterModule(RestipyModule):
    def execute(self, recipe, module_params):
        if not ('data' in module_params):
            raise Exception('You must supply "data" for print.')

        dumps = json.dumps
        if 'args' in module_params:
            dumps = partial(json.dumps, **module_params['args'])
        print dumps(module_params['data'])
