import pyee
import json
from ntwork.core.mgr import WeWorkMgr
from ntwork.const import notify_type, send_type
from threading import Event
from ntwork.wc import wcprobe
from ntwork.utils import generate_guid
from ntwork.utils import logger
from ntwork.exception import WeWorkNotLoginError
from functools import wraps
from typing import (
    List,
    Union,
    Tuple
)

log = logger.get_logger("WeWorkInstance")


class ReqData:
    __response_message = None
    msg_type: int = 0
    request_data = None

    def __init__(self, msg_type, data):
        self.msg_type = msg_type
        self.request_data = data
        self.__wait_event = Event()

    def wait_response(self, timeout=None):
        self.__wait_event.wait(timeout)
        return self.get_response_data()

    def on_response(self, message):
        self.__response_message = message
        self.__wait_event.set()

    def get_response_data(self):
        if self.__response_message is None:
            return None
        return self.__response_message["data"]


class WeWork:
    client_id: int = 0
    pid: int = 0
    status: bool = False
    login_status: bool = False

    def __init__(self):
        WeWorkMgr().append_instance(self)
        self.__wait_login_event = Event()
        self.__req_data_cache = {}
        self.__msg_event_emitter = pyee.EventEmitter()
        self.__login_info = {}

    def on(self, msg_type, f):
        return self.__msg_event_emitter.on(str(msg_type), f)

    def msg_register(self, msg_type: Union[int, List[int], Tuple[int]]):
        if not (isinstance(msg_type, list) or isinstance(msg_type, tuple)):
            msg_type = [msg_type]

        def wrapper(f):
            wraps(f)
            for event in msg_type:
                self.on(event, f)
            return f

        return wrapper

    def on_close(self):
        self.login_status = False
        self.status = False
        self.__msg_event_emitter.emit(str(notify_type.MT_RECV_WEWORK_QUIT_MSG), self)

        message = {
            "type": notify_type.MT_RECV_WEWORK_QUIT_MSG,
            "data": {}
        }
        self.__msg_event_emitter.emit(str(notify_type.MT_ALL), self, message)

    def bind_client_id(self, client_id):
        self.status = True
        self.client_id = client_id

    def on_recv(self, message):
        log.debug("on recv message: %s", message)
        msg_type = message["type"]
        extend = message.get("extend", None)
        if msg_type == notify_type.MT_USER_LOGIN_MSG:
            self.login_status = True
            self.__wait_login_event.set()
            self.__login_info = message.get("data", {})
            log.info("login success, name: %s", self.__login_info["username"])
        elif msg_type == notify_type.MT_USER_LOGOUT_MSG:
            self.login_status = False
            log.info("logout, pid: %d", self.pid)

        if extend is not None and extend in self.__req_data_cache:
            req_data = self.__req_data_cache[extend]
            req_data.on_response(message)
            del self.__req_data_cache[extend]
        else:
            self.__msg_event_emitter.emit(str(msg_type), self, message)
            self.__msg_event_emitter.emit(str(notify_type.MT_ALL), self, message)

    def wait_login(self, timeout=None):
        log.info("wait login...")
        self.__wait_login_event.wait(timeout)

    def open(self, smart=False):
        self.pid = wcprobe.open(smart)
        log.info("open wework pid: %d", self.pid)
        return self.pid != 0

    def attach(self, pid: int):
        self.pid = pid
        log.info("attach wework pid: %d", self.pid)
        return wcprobe.attach(pid)

    def detach(self):
        log.info("detach wework pid: %d", self.pid)
        return wcprobe.detach(self.pid)

    def __send(self, msg_type, data=None, extend=None):
        if not self.login_status:
            raise WeWorkNotLoginError()

        message = {
            'type': msg_type,
            'data': {} if data is None else data,
        }
        if extend is not None:
            message["extend"] = extend
        message_json = json.dumps(message)
        log.debug("communicate wework pid: %d,  data: %s", self.pid, message)
        return wcprobe.send(self.client_id, message_json)

    def __send_sync(self, msg_type, data=None, timeout=10):
        req_data = ReqData(msg_type, data)
        extend = self.__new_extend()
        self.__req_data_cache[extend] = req_data
        self.__send(msg_type, data, extend)
        return req_data.wait_response(timeout)

    def __new_extend(self):
        while True:
            guid = generate_guid("req")
            if guid not in self.__req_data_cache:
                return guid

    def __repr__(self):
        return f"WeWorkInstance(pid: {self.pid}, client_id: {self.client_id})"

    def get_login_info(self):
        """
        获取登录信息
        """
        return self.__login_info

    def get_self_info(self):
        """
        获取自己个人信息跟登录信息类似
        """
        return self.__send_sync(send_type.MT_GET_SELF_MSG)

    def get_inner_contacts(self, page_num=1, page_size=500):
        """
        获取内部(同事)联系人列表
        """
        data = {
            'page_num': page_num,
            'page_size': page_size
        }
        return self.__send_sync(send_type.MT_GET_INNER_CONTACTS_MSG, data)

    def get_external_contacts(self, page_num=1, page_size=500):
        """
        获取外部(客户)联系人列表
        """
        data = {
            'page_num': page_num,
            'page_size': page_size
        }
        return self.__send_sync(send_type.MT_GET_EXTERNAL_CONTACTS_MSG, data)

    def get_contact_detail(self, user_id: str):
        """
        获取联系人详细信息
        """
        data = {
            'user_id': user_id
        }
        return self.__send_sync(send_type.MT_GET_CONTACT_DETAIL_MSG, data)

    def get_rooms(self, page_num=1, page_size=500):
        """
        获取群列表
        """
        data = {
            'page_num': page_num,
            'page_size': page_size
        }
        return self.__send_sync(send_type.MT_GET_ROOMS_MSG, data)

    def get_room_members(self, conversation_id: str,  page_num: int = 1, page_size: int = 500):
        """
        获取群成员列表
        """
        data = {
            'conversation_id': conversation_id,
            'page_num': page_num,
            'page_size': page_size
        }
        return self.__send_sync(send_type.MT_GET_ROOM_MEMBERS_MSG, data)

    def send_text(self, conversation_id: str, content: str):
        """
        发送文本消息
        """
        data = {
            'conversation_id': conversation_id,
            'content': content
        }
        return self.__send(send_type.MT_SEND_TEXT_MSG, data)

    def send_room_at_msg(self, conversation_id: str, content: str, at_list: List[str]):
        """
        发送群@消息
        """
        data = {
            'conversation_id': conversation_id,
            'content': content,
            'at_list': at_list
        }
        return self.__send(send_type.MT_SEND_ROOM_AT_MSG, data)

    def send_card(self, conversation_id: str, user_id: str):
        """
        发送名片
        """
        data = {
            'conversation_id': conversation_id,
            'user_id': user_id
        }
        return self.__send(send_type.MT_SEND_CARD_MSG, data)

    def send_link_card(self, conversation_id: str, title: str, desc: str, url: str, image_url: str):
        """
        发送链接卡片
        """
        data = {
            'conversation_id': conversation_id,
            'title': title,
            'desc': desc,
            'url': url,
            'image_url': image_url
        }
        return self.__send(send_type.MT_SEND_LINK_MSG, data)

    def send_image(self, conversation_id: str, file_path: str):
        """
        发送图片
        """
        data = {
            'conversation_id': conversation_id,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_IMAGE_MSG, data)

    def send_file(self, conversation_id: str, file_path: str):
        """
        发送文件
        """
        data = {
            'conversation_id': conversation_id,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_FILE_MSG, data)

    #
    def send_video(self, conversation_id: str, file_path: str):
        """
        发送视频
        """
        data = {
            'conversation_id': conversation_id,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_VIDEO_MSG, data)

    def send_gif(self, conversation_id: str, file_path: str):
        """
        发送gif:
        """
        data = {
            'conversation_id': conversation_id,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_GIF_MSG, data)

    def c2c_cdn_download(self, file_id: str, aes_key: str, file_size: int, file_type: int, save_path: str):
        """
        下载c2c类型的cdn文件
        """
        data = {
            'file_id': file_id,
            'aes_key': aes_key,
            'file_size': file_size,
            'file_type': file_type,
            "save_path": save_path
        }
        return self.__send_sync(send_type.MT_C2CCDN_DOWNLOAD_MSG, data)

    def wx_cdn_download(self, url: str, auth_key: str, size: int, save_path):
        """
        下载wx类型的cdn文件，以https开头
        """
        data = {
            'url': url,
            'auth_key': auth_key,
            'size': size,
            'save_path': save_path
        }
        return self.__send_sync(send_type.MT_WXCDN_DOWNLOAD_MSG, data)


