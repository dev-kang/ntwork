# -*- coding: utf-8 -*-
import sys
import time
import ntwork

wework = ntwork.WeWork()

# 打开pc企业微信, smart: 是否管理已经登录的微信
wework.open(smart=True)


# 注册消息回调
@wework.msg_register(ntwork.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wework_instance: ntwork.WeWork, message):
    data = message["data"]
    sender_user_id = data["sender"]
    self_user_id = wework_instance.get_login_info()["user_id"]
    conversation_id: str = data["conversation_id"]

    # 判断消息不是自己发的并且不是群消息时，回复对方
    if sender_user_id != self_user_id and not conversation_id.startswith("R:"):
        wework_instance.send_text(conversation_id=conversation_id, content=f"你发送的消息是: {data['content']}")


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
