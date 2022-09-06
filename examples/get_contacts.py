# -*- coding: utf-8 -*-
import sys
import time
import ntwork

wework = ntwork.WeWork()

# 打开pc微信, smart: 是否管理已经登录的微信
wework.open(smart=True)

# 等待登录
wework.wait_login()

# 获取内部(同事)列表并输出
contacts = wework.get_inner_contacts()
print("内部(同事)联系人列表: ")
print(contacts)

# 获取外部(客户)列表并输出
contacts = wework.get_external_contacts()
print("外部(客户)联系人列表: ")
print(contacts)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()

