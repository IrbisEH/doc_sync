import paramiko


# TODO: попробовать обернуть в декортаторы супер похожий код в функциях/ нужна обертка
# TODO: или использовать контекст


class Connection:
    def __init__(self, config_manager, log_manager):
        self.config = config_manager
        self.log = log_manager

        self.ssh_client = None
        self.sftp_client = None
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def __enter__(self):
        if self.sftp_client is None:
            self.connect_sftp()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sftp_client is not None:
            self.sftp_client.close()
        # TODO: изучить нужно ли закрывать
        if self.ssh_client is not None:
            self.ssh_client.close()
        return False

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

    def exec_cmd(self, cmd):
        result = None

        try:
            if self.ssh_client is None:
                self.connect_ssh()

            print(cmd)

            _, stdout, stderr = self.ssh_client.exec_command(cmd)

            result = stdout.read().decode('utf-8')
            errors = stderr.read().decode('utf-8')

            print(result)
            print(errors)

            if errors:
                raise Exception(errors)

        except Exception as e:
            if self.config.debug:
                print(e)

        return result

    def send_file(self):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

    def receive_file(self):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

    def get_files_data(self):
        try:
            if self.sftp_client is None:
                self.connect_sftp()

        except Exception as e:
            if self.config.debug:
                print(e)

    def check_connection(self):
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
