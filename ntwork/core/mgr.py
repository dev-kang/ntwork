import json
import os.path
from ntwork.wc import wcprobe
from ntwork.utils.xdg import get_helper_file
from ntwork.exception import WeWorkVersionNotMatchError, WeWorkBindError
from ntwork.utils.singleton import Singleton
from ntwork.const import notify_type
from ntwork.utils.logger import get_logger
from ntwork import conf

log = get_logger("WeWorkManager")


class WeWorkMgr(metaclass=Singleton):
    __instance_list = []
    __instance_map = {}

    def __init__(self):
        self.set_wework_exe_path(conf.DEFAULT_WEWORK_EXE_PATH, conf.DEFAULT_WEWORK_VERSION)

        # init callbacks
        wcprobe.init_callback(self.__on_accept, self.__on_recv, self.__on_close)

    def set_wework_exe_path(self, wework_exe_path=None, wework_version=None):
        exe_path = ''
        if wework_exe_path is not None:
            exe_path = wework_exe_path

        if wework_version is None:
            version = wcprobe.get_install_wework_version()
        else:
            version = wework_version

        helper_file = get_helper_file(version)
        if not os.path.exists(helper_file):
            raise WeWorkVersionNotMatchError()

        log.info("initialize wework, version: %s", version)

        # init env
        wcprobe.init_env(helper_file, exe_path)

    def append_instance(self, instance):
        log.debug("new wework instance")
        self.__instance_list.append(instance)

    def __bind_wework(self, client_id, pid):
        bind_instance = None
        if client_id not in self.__instance_map:
            for instance in self.__instance_list:
                if instance.pid == pid:
                    instance.bind_client_id(client_id)
                    self.__instance_map[client_id] = instance
                    bind_instance = instance
                    break
        if bind_instance is None:
            raise WeWorkBindError()
        self.__instance_list.remove(bind_instance)

    def __on_accept(self, client_id):
        log.debug("accept client_id: %d", client_id)

    def __on_recv(self, client_id, data):
        message = json.loads(data)
        if message["type"] == notify_type.MT_READY_MSG:
            self.__bind_wework(client_id, message["data"]["pid"])
        else:
            self.__instance_map[client_id].on_recv(message)

    def __on_close(self, client_id):
        log.debug("close client_id: %d", client_id)
        if client_id in self.__instance_map:
            self.__instance_map[client_id].on_close()
