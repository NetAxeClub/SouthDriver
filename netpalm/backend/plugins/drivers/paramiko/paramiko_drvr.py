import logging

from paramiko import SSHClient, AutoAddPolicy
from netpalm.backend.core.confload.confload import config
from netpalm.backend.core.driver.netpalm_driver import NetpalmDriver
from netpalm.backend.core.utilities.rediz_meta import write_meta_error

log = logging.getLogger(__name__)


class paramko(NetpalmDriver):
    driver_name = "paramiko"

    def __init__(self, **kwargs):
        self.kwarg = kwargs.get("args", False)
        self.connection_args = kwargs.get("connection_args", False)
        #  support IOSXR commit labels
        self.commit_label = None
        if self.kwarg:
            if commit_label := self.kwarg.get("commit_label", None):
                self.commit_label = commit_label
                del self.kwarg["commit_label"]
        self.enable_mode = kwargs.get("enable_mode", False)

    def connect(self):
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            paramikoses = ssh.connect(**self.connection_args)
            return paramikoses
        except Exception as e:
            write_meta_error(e)

    def sendcommand(self, session, command):
        try:
            if self.enable_mode:
                session.enable()
            result = {}
            for commands in command:
                # 连接服务器
                stdin, stdout, stderr = session.exec_command(commands)
                # 执行命令
                result = stdout.read()
                # 关闭连接
                if self.kwarg:
                    # normalise the ttp template name for ease of use
                    if "ttp_template" in self.kwarg.keys():
                        if isinstance(self.kwarg['ttp_template'], list):
                            _index = command.index(commands)
                            template_name = (
                                    config.ttp_templates
                                    + self.kwarg['ttp_template'][_index]
                                    + ".ttp"
                            )
                            self.kwarg["ttp_template"] = template_name
                        else:
                            template_name = (
                                config.ttp_templates
                                + self.kwarg["ttp_template"]
                                + ".ttp"
                            )
                            self.kwarg["ttp_template"] = template_name
                    stdin, stdout, stderr = session.exec_command(commands)
                    result[commands] = stdout.read().decode()
                else:
                    stdin, stdout, stderr = session.exec_command(commands)
                    result[commands] = stdout.read().decode()
            return result
        except Exception as e:
            write_meta_error(e)

    def config(self, session, command="", enter_enable=False, dry_run=False):
        try:
            if type(command) == list:
                comm = command
            else:
                comm = command.splitlines()

            if enter_enable:
                session.enable()

            if self.kwarg:
                response = session.send_config_set(comm, **self.kwarg)
            else:
                response = session.send_config_set(comm)

            # if not dry_run:
            #     response += self.__try_commit_or_save(session)

            result = {}
            result["changes"] = response.split("\n")
            return result

        except Exception as e:
            write_meta_error(e)


    def logout(self, session):
        try:
            response = session.close()
            return response
        except Exception as e:
            write_meta_error(e)
