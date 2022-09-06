# -*- coding: utf-8 -*-
import sys
import time
import ntwork

wework = ntwork.WeWork()

# 打开pc企业微信, smart: 是否管理已经登录的微信
wework.open(smart=True)


# 注册监听所有消息回调
@wework.msg_register(ntwork.MT_ALL)
def on_recv_text_msg(wework_instance: ntwork.WeWork, message):
    print("########################")
    print(message)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
