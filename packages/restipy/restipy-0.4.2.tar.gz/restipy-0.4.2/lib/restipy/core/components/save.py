class SaveComponent:
    def __init__(self, args):
        self.args = args

    def process(self, recipe, input_data, result):
        save_name = recipe['id']
        if 'save' in recipe:
            save_params = recipe['save']

            if type(save_params) is str:
                input_data[save_params] = result.output
            elif type(save_params is dict):
                if 'name' in save_params:
                    save_name = save_params['name']

                if 'jmespath' in save_params:
                    import jmespath
                    path = save_params['jmespath']
                    input_data[save_name] = jmespath.search(path, result.output)
                else:
                    input_data[save_name] = result.output


        else:
            input_data[save_name] = result.output
