import os
import json
import subprocess

from app_py.app.ConfigManager import OsSystems
from app_py.app.ConfigManager import ConfigManager
from app_py.app.LogManager import LogManager
from app_py.app.Client import Connection


class App:
    def __init__(self, root_path):
        self.config = ConfigManager(root_path)
        self.log = LogManager(self.config.logs_path)
        self.last_state = self.read_state_file()
        self.current_state = {}
        self.upload_list = []

    def save_state_file(self):
        with open(self.config.state_file_path, 'w') as state_file:
            json.dump(self.current_state, state_file)

    def read_state_file(self):
        result = {}

        if not os.path.exists(self.config.state_file_path):
            if not os.path.exists(self.config.state_dir_path):
                os.makedirs(self.config.state_dir_path)
            with open(self.config.state_file_path, 'w', encoding='utf-8') as state_file:
                json.dump(result, state_file)
        else:
            with open(self.config.state_file_path, 'r', encoding='utf-8') as state_file:
                result = json.load(state_file)

        return result

    def upload_files(self):
        pass

    def sync(self):
        for root, dirs, file_names in os.walk(self.config.sync_client_folder):
            for file_name in file_names:
                file = os.path.join(root, file_name)
                file_t = os.path.getmtime(file)

                if file not in self.last_state or file_t != float(self.last_state[file]):
                    self.upload_list.append(file)

                self.current_state[file] = file_t

        self.save_state_file()