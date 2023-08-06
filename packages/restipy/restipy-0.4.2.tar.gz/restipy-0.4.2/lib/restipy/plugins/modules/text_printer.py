from restipy.core.modules import RestipyModule

class TextPrinterModule(RestipyModule):
    def execute(self, recipe, module_params):
        if 'format' in module_params:
            string_format = module_params['format']
        else:
            string_format = default_string_format

        print string_format.format(output=result.output)
