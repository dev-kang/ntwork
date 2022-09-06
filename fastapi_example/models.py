from typing import Optional, List, Any
from pydantic import BaseModel


class ClientReqModel(BaseModel):
    guid: str


class ResponseModel(BaseModel):
    status: int
    msg: Optional[str] = ""
    data: Optional[Any] = None


class ClientOpenReqModel(ClientReqModel):
    smart: Optional[bool] = True
    show_login_qrcode: Optional[bool] = False


class CallbackUrlReqModel(BaseModel):
    callback_url: Optional[str] = ""


class GetContactDetailReqModel(ClientReqModel):
    user_id: str


class PageReqModel(ClientReqModel):
    page_num: Optional[int] = 1
    page_size: Optional[int] = 500


class GetInnerContactsReqModel(PageReqModel):
    pass


class GetExternalContactsReqModel(PageReqModel):
    pass


class GetRoomsReqModel(PageReqModel):
    pass


class GetRoomMembersReqModel(PageReqModel):
    conversation_id: str


class SendMsgReqModel(ClientReqModel):
    conversation_id: str


class SendTextReqModel(SendMsgReqModel):
    content: str


class SendRoomAtReqModel(SendTextReqModel):
    at_list: List[str]


class SendCardReqModel(SendMsgReqModel):
    user_id: str


class SendLinkCardReqModel(SendMsgReqModel):
    title: str
    desc: str
    url: str
    image_url: str


class SendMediaReqModel(SendMsgReqModel):
    file_path: Optional[str] = ""
    url: Optional[str] = ""
