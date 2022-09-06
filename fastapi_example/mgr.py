# -*- coding: utf-8 -*-
import ntwork
import requests
from typing import Dict, Union
from ntwork.utils.singleton import Singleton
from utils import generate_guid
from exception import ClientNotExists


class ClientWeWork(ntwork.WeWork):
    guid: str = ""


class ClientManager(metaclass=Singleton):
    __client_map: Dict[str, ntwork.WeWork] = {}
    callback_url: str = ""

    def new_guid(self):
        """
        生成新的guid
        """
        while True:
            guid = generate_guid("wework")
            if guid not in self.__client_map:
                return guid

    def create_client(self):
        guid = self.new_guid()
        wework = ClientWeWork()
        wework.guid = guid
        self.__client_map[guid] = wework

        # 注册回调
        wework.on(ntwork.MT_ALL, self.__on_callback)
        wework.on(ntwork.MT_RECV_WEWORK_QUIT_MSG, self.__on_quit_callback)
        return guid

    def get_client(self, guid: str) -> Union[None, ntwork.WeWork]:
        client = self.__client_map.get(guid, None)
        if client is None:
            raise ClientNotExists(guid)
        return client

    def remove_client(self, guid):
        if guid in self.__client_map:
            del self.__client_map[guid]

    def __on_callback(self, wework, message):
        if not self.callback_url:
            return

        client_message = {
            "guid": wework.guid,
            "message": message
        }
        requests.post(self.callback_url, json=client_message)

    def __on_quit_callback(self, wework):
        self.__on_callback(wework, {"type": ntwork.MT_RECV_WEWORK_QUIT_MSG, "data": {}})
