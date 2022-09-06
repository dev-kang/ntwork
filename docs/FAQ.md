## WeWorkVersionNotMatchError异常
如果出现`ntwork.exception.WeWorkVersionNotMatchError异常`异常, 请确认是否安装github上指定的企业微信版本，如果确认已经安装，还是报错，可以在代码中添加以下代码，跳过微信版本检测
```python
import ntwork
ntwork.set_wework_exe_path(wework_version='4.0.8.6027') 
```

## 如何多开

新建多个ntwork.wework实例，然后调用open方法：
```python
import ntwork

# 多开3个微信
for i in range(3):
    wework = ntwork.WeWork()
    wework.open(smart=False)
```
更完善的多实例管理查看[fastapi_example例子](./fastapi_example)

## 如何监听输出所有的消息

```python
# 注册监听所有消息回调
import ntwork


@wework.msg_register(ntwork.MT_ALL)
def on_recv_text_msg(wework_instance: ntwork.WeWork, message):
    print("########################")
    print(message)
```
完全例子查看[examples/msg_register_all.py](../examples/msg_register_all.py)

## 如何关闭ntwork的日志

`os.environ['NTWORK_LOG'] = "ERROR"` 要在`import ntwork`前执行
```python
# -*- coding: utf-8 -*-
import os
import sys
import time
os.environ['NTWORK_LOG'] = "ERROR"

import ntwork
```

## 如何正常的关闭Cmd窗口

先使用`pip install pywin32` 安装pywin32模块, 然后在代码中添加以下代码， 完整例子查看[examples/cmd_close_event.py](../examples/cmd_close_event.py)
```python
import sys
import ntwork
import win32api

def on_exit(sig, func=None):
    ntwork.exit_()
    sys.exit()


# 当关闭cmd窗口时
win32api.SetConsoleCtrlHandler(on_exit, True)
```


## pyinstaller打包exe
使用pyinstaller打包ntwork项目，需要添加`--collect-data=ntwork`选项

打包成单个exe程序
```bash
pyinstaller -F --collect-data=ntwork main.py
```

将所有的依赖文件打包到一个目录中
```bash
pyinstaller -y --collect-data=ntwork main.py
```
