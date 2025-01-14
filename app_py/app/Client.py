import paramiko


# TODO: попробовать обернуть в декортаторы супер похожий код в функциях/ нужна обертка


class Client:
    def __init__(self, config_manager, log_manager):
        self.config = config_manager
        self.log = log_manager

        self.ssh_client = None
        self.sftp_client = None
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def connect_ssh(self):
        self.ssh_client = paramiko.client.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(
            self.config.server_host,
            username=self.config.server_username,
            password=self.config.server_password,
        )

    def connect_sftp(self):
        if self.ssh_client is None:
            self.connect_ssh()
        self.sftp_client = self.ssh_client.open_sftp()

    def send_file(self, close_conn=True):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

        if self.sftp_client is not None and close_conn:
            self.ssh_client.close()

    def receive_file(self, close_conn=True):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

        if self.sftp_client is not None and close_conn:
            self.ssh_client.close()

    def get_files_data(self, close_conn=True):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

        if self.sftp_client is not None and close_conn:
            self.ssh_client.close()

    def check_connection(self, close_conn=True):
        try:
            if self.ssh_client is None:
                self.connect_ssh()

            stdin, stdout, stderr = self.ssh_client.exec_command('df')

            print('stdout:')
            print(stdout.read().decode('utf-8'))

            print('stderr:')
            print(stderr.read().decode('utf-8'))

        except Exception as e:
            if self.config.debug:
                print(e)

        if self.ssh_client is not None and close_conn:
            self.ssh_client.close()