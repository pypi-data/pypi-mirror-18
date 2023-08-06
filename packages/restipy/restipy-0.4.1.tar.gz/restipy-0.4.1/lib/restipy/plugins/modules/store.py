from restipy.core.modules import RestipyModule
from restipy.core import LocalStore

from os.path import expanduser
home = expanduser("~")

default_filename = '{}/.restipy/data.json'.format(home)

class StoreModule(RestipyModule):
    def execute(self, recipe, component):
        if not ('data' in component):
            raise Exception('No "data" found in component.')

        if not ('file' in component):
            filename = default_filename
        else:
            filename = component['filename']

        local_store = LocalStore(
            filename=filename,
            environment=self.environment
        )

        local_store.put(recipe['id'], component['data'])
