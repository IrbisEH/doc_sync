import os
from pathlib import Path
from dotenv import load_dotenv


class ConfigManager:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

        # app relative paths
        self.dotenv_path = self.root_path / ".env"
        self.logs_path = self.root_path / ".logs"

        load_dotenv(dotenv_path=self.dotenv_path)

        self.server_mode = bool(int(os.getenv("SERVER_MODE", "0")))
        self.sync_folders = self.get_sync_folder_list()

    @staticmethod
    def get_sync_folder_list():
        res = []

        i = 0
        val = os.getenv(f"SYNC_FOLDER[{i}]", None)

        while val is not None:
            res.append(val)
            i += 1
            val = os.getenv(f"SYNC_FOLDER[{i}]", None)

        return res
