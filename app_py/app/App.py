from app_py.app.ConfigManager import ConfigManager
from app_py.app.LogManager import LogManager
from app_py.app.Client import Client


class App:
    def __init__(self, root_path):
        self.config = ConfigManager(root_path)
        self.log = LogManager(self.config.logs_path)
        self.client = Client(self.config, self.log)

    def check_folder(self):
        pass

    def compare_folder(self):
        pass

    def sync_folder(self):
        pass

    def print_sync_folders(self):
        for idx, folder in enumerate(self.config.sync_folders):
            print(f"{idx + 1}. {folder}")