import json
import subprocess

from app_py.app.ConfigManager import OsSystems
from app_py.app.ConfigManager import ConfigManager
from app_py.app.LogManager import LogManager
from app_py.app.Client import Client

class App:
    GET_DATA_CMD = {
        'ubuntu': f'find [PATH] -mindepth 1 -type f -exec stat -c \'{{"name":"%n","last_modified":"%Y"}}\' {{}} + | jq -s \'reduce .[] as $item ({{}}; .[$item.name] = $item)\'',
        'mac': f'find [PATH] -mindepth 1 -type f -exec stat -f \'{{"name":"%N","last_modified":"%m"}}\' {{}} + | jq -s \'reduce .[] as $item ({{}}; .[$item.name] = $item)\''
    }

    def __init__(self, root_path):
        self.config = ConfigManager(root_path)
        self.log = LogManager(self.config.logs_path)
        self.client = Client(self.config, self.log)

    def get_local_state(self):
        result = None

        try:
            cmd = self.GET_DATA_CMD[self.config.os]
            cmd = cmd.replace('[PATH]', str(self.config.sync_client_folder))
            response = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            output = response.stdout
            errors = response.stderr

            if errors:
                raise Exception(errors)

            data = json.loads(output)

            result = {key.replace(f'{str(self.config.sync_client_folder)}/', ''): value for key, value in data.items()}

        except Exception as e:
            if self.config.debug:
                print(e)

        return result

    def get_server_state(self):
        result = None

        try:
            self.client.connect_ssh()

            cmd = self.GET_DATA_CMD[OsSystems.ubuntu]
            cmd = cmd.replace('[PATH]', str(self.config.sync_server_folder))
            _, stdout, stderr = self.client.ssh_client.exec_command(cmd)

            output = stdout.read().decode('utf-8')
            errors = stderr.read().decode('utf-8')

            if errors:
                raise Exception(errors)

            data = json.loads(output)

            result = {key.replace(f'{str(self.config.sync_server_folder)}/', ''): value for key, value in data.items()}

        except Exception as e:
            if self.config.debug:
                print(e)

        return result

    def sync(self):
        server_state = self.get_server_state()
        local_state = self.get_local_state()

