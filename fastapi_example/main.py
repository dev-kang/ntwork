# -*- coding: utf-8 -*-
import uvicorn
from functools import wraps
from fastapi import FastAPI
from mgr import ClientManager
from down import get_local_path
from exception import MediaNotExistsError, ClientNotExists
import models
import ntwork


def response_json(status=0, data=None, msg=""):
    return {
        "status": status,
        "data": {} if data is None else data,
        "msg": msg
    }


class catch_exception:
    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except ntwork.WeWorkNotLoginError:
                return response_json(msg="wework instance not login")
            except ntwork.WeWorkBindError:
                return response_json(msg="wework bind error")
            except ntwork.WeWorkVersionNotMatchError:
                return response_json(msg="wework version not match, install require wework version")
            except MediaNotExistsError:
                return response_json(msg="file_path or url error")
            except ClientNotExists as e:
                return response_json(msg="client not exists, guid: %s" % e.guid)
            except Exception as e:
                return response_json(msg=str(e))

        return wrapper


client_mgr = ClientManager()
app = FastAPI(title="NtWork fastapi完整示例",
              description="NtWork项目地址: https://github.com/smallevilbeast/ntwork")


@app.post("/client/create", summary="创建实例", tags=["Client"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_create():
    guid = client_mgr.create_client()
    return response_json(1, {"guid": guid})


@app.post("/client/open", summary="打开企业微信", tags=["Client"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_open(model: models.ClientOpenReqModel):
    ret = client_mgr.get_client(model.guid).open(model.smart)
    return response_json(1 if ret else 0)


@app.post("/global/set_callback_url", summary="设置接收通知地址", tags=["Global"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_set_callback_url(model: models.CallbackUrlReqModel):
    client_mgr.callback_url = model.callback_url
    return response_json(1)


@app.post("/user/get_profile", summary="获取自己的信息", tags=["User"],
          response_model=models.ResponseModel)
@catch_exception()
async def user_get_profile(model: models.ClientReqModel):
    data = client_mgr.get_client(model.guid).get_self_info()
    return response_json(1, data)


@app.post("/contact/get_inner_contacts", summary="获取同事列表", tags=["Contact"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_contacts(model: models.GetInnerContactsReqModel):
    data = client_mgr.get_client(model.guid).get_inner_contacts(model.page_num,
                                                                model.page_size)
    return response_json(1, data)


@app.post("/contact/get_external_contacts", summary="获取客户列表", tags=["Contact"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_contacts(model: models.GetExternalContactsReqModel):
    data = client_mgr.get_client(model.guid).get_external_contacts(model.page_num,
                                                                   model.page_size)
    return response_json(1, data)


@app.post("/contact/get_contact_detail", summary="获取指定联系人详细信息", tags=["Contact"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_contact_detail(model: models.GetContactDetailReqModel):
    data = client_mgr.get_client(model.guid).get_contact_detail(model.user_id)
    return response_json(1, data)


@app.post("/room/get_rooms", summary="获取群列表", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_rooms(model: models.GetRoomsReqModel):
    data = client_mgr.get_client(model.guid).get_rooms()
    return response_json(1, data)


@app.post("/room/get_room_members", summary="获取群成员列表", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_room_members(model: models.GetRoomMembersReqModel):
    data = client_mgr.get_client(model.guid).get_room_members(model.conversation_id,
                                                              model.page_num, model.page_size)
    return response_json(1, data)


@app.post("/msg/send_text", summary="发送文本消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def msg_send_text(model: models.SendTextReqModel):
    ret = client_mgr.get_client(model.guid).send_text(model.conversation_id, model.content)
    return response_json(1 if ret else 0)


@app.post("/msg/send_room_at", summary="发送群@消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_room_at(model: models.SendRoomAtReqModel):
    ret = client_mgr.get_client(model.guid).send_room_at_msg(model.conversation_id,
                                                             model.content,
                                                             model.at_list)
    return response_json(1 if ret else 0)


@app.post("/msg/send_card", summary="发送名片", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_card(model: models.SendCardReqModel):
    ret = client_mgr.get_client(model.guid).send_card(model.conversation_id,
                                                      model.user_id)
    return response_json(1 if ret else 0)


@app.post("/msg/send_link_card", summary="发送链接卡片消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_link_card(model: models.SendLinkCardReqModel):
    ret = client_mgr.get_client(model.guid).send_link_card(model.conversation_id,
                                                           model.title,
                                                           model.desc,
                                                           model.url,
                                                           model.image_url)
    return response_json(1 if ret else 0)


@app.post("/msg/send_image", summary="发送图片", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_image(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_image(model.conversation_id, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_file", summary="发送文件", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_file(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_file(model.conversation_id, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_video", summary="发送视频", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_video(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_video(model.conversation_id, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_gif", summary="发送GIF", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_gif(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_gif(model.conversation_id, file_path)
    return response_json(1 if ret else 0)


if __name__ == '__main__':
    uvicorn.run(app=app)
