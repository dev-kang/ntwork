# -*- coding: utf-8 -*-
import os
import sys
import time
os.environ['ntwork_LOG'] = "ERROR"

import ntwork

wework = ntwork.WeWork()

# 打开pc微信, smart: 是否管理已经登录的微信
wework.open(smart=True)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
