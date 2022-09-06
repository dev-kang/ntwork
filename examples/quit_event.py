# -*- coding: utf-8 -*-
import sys
import time
import ntwork


wework = ntwork.WeWork()

# 打开pc微信, smart: 是否管理已经登录的微信
wework.open(smart=True)

global_quit_flag = False


# 微信进程关闭通知
@wework.msg_register(ntwork.MT_RECV_WEWORK_QUIT_MSG)
def on_wework_quit(wework_instace):
    print("###################")
    global global_quit_flag
    global_quit_flag = True


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
while True:
    if global_quit_flag:
        break
    time.sleep(0.5)

ntwork.exit_()
sys.exit()
