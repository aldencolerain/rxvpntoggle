import os
import json
from appdirs import AppDirs


class Settings:

    def __init__(self):
        self.dir = AppDirs("vpntoggle", "rx").user_data_dir
        self.path = os.path.join(self.dir, 'config.json')
        # ensure the config dir exists
        try:
            os.makedirs(self.dir)
        except FileExistsError:
            pass
        # ensure the config file exists
        open(self.path, 'a').close()
        # load config
        self.values = {}
        self.load()

    def load(self):
        with open(self.path, 'r') as file:
            values = json.load(file)
            if isinstance(self.values, dict):
                self.values = values
            else:
                print('Warning: Configuration file was malformed.')

    def set(self, key, value):
        self.values[key] = value
        with open(self.path, 'w') as file:
            json.dump(self.values, file)

    def configure(self):
        print(f'Saving to: {self.path}')
        print('')
        interface = input('Please enter name of wireguard interface (name of config file without file extension): ')
        self.set('interface', interface.strip())
        expected = input('Please enter expected ip address (will be checked using dig on opendns!): ')
        self.set('expected', expected.strip())
        external = input('Please enter external hostname on to ping to validate connection [default: google.com]: ')
        self.set('external', external.strip() or 'google.com')
        internal = input('Please enter internal hostname on vpn to ping to validate connection [default: none]: ')
        self.set('internal', internal.strip())

    def configured(self):
        return 'interface' in self.values

settings = Settings()
