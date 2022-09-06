# -*- coding: utf-8 -*-
import sys
import time
import ntwork

try:
    import win32api
except ImportError:
    print("Error: this example require pywin32, use `pip install pywin32` install")
    sys.exit()

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


def exit_application():
    ntwork.exit_()
    sys.exit()


def on_exit(sig, func=None):
    exit_application()


# 当关闭cmd窗口时
win32api.SetConsoleCtrlHandler(on_exit, True)

# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
# 当Ctrl+C结束程序时
except KeyboardInterrupt:
    exit_application()
