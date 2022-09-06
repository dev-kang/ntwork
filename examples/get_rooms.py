# -*- coding: utf-8 -*-
import sys
import time
import ntwork

wework = ntwork.WeWork()

# 打开pc微信, smart: 是否管理已经登录的微信
wework.open(smart=True)

# 等待登录
wework.wait_login()

# 获取群列表并输出
rooms = wework.get_rooms()
print("群列表: ")
print(rooms)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()

