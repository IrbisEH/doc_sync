import os
import platform
from pathlib import Path
from dotenv import load_dotenv


class OsSystems:
    mac = 'mac'
    ubuntu = 'ubuntu'


class ConfigManager:
    PLATFORMS = {
        'darwin': OsSystems.mac
    }
    def __init__(self, root_path):
        self.os = self.PLATFORMS.get(platform.system().lower(), OsSystems.ubuntu)

        self.root_path = Path(root_path)

        # app relative paths
        self.dotenv_path = self.root_path / ".env"
        self.logs_path = self.root_path / ".logs"
        self.state_dir_path = self.root_path / ".state"
        self.state_file_path = self.state_dir_path / "state.json"

        load_dotenv(dotenv_path=self.dotenv_path)

        self.debug = bool(int(os.getenv("DEBUG", "0")))
        self.server_mode = bool(int(os.getenv("SERVER_MODE", "0")))

        self.sync_client_folder = Path(os.getenv("SYNC_CLIENT_FOLDER"))
        self.sync_server_folder = Path(os.getenv("SYNC_SERVER_FOLDER"))

        self.server_host = os.getenv("SERVER_HOST")
        self.server_username = os.getenv("SERVER_USERNAME")
        self.server_password = os.getenv("SERVER_PASSWORD")
