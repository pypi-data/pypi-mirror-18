import json, os

class LocalStore:
    def __init__(self, filename, environment='default'):
        self.filename = filename
        self.environment = environment
        self.load()

    def get_data(self):
        if not self.data:
            self.data = {}

        if not self.environment in self.data:
            self.data[self.environment] = {}

        return self.data[self.environment]

    def set_data(self, data):
        if self.environment in self.data:
            self.data = {
                self.environment: data
            }
        else:
            self.data[self.environment] = {data}

    def load(self):
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))

        with open(self.filename, 'a+') as in_file:
            try:
                self.data = json.load(in_file)
            except:
                self.data = {}

    def dump(self):
        with open(self.filename, 'w+') as out_file:
            json.dump(self.data, out_file)
