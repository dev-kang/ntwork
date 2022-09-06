<h1 align="center">ntwork</h1>
<p align="center">
    <a href="https://github.com/smallevilbeast/ntwork/releases"><img src="https://img.shields.io/badge/release-0.1.1-blue.svg?" alt="release"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-brightgreen.svg?" alt="License"></a>
</p>




## 介绍

- 基于pc企业微信的api接口
- 支持收发文本、群@、名片、图片、文件、视频、链接卡片等
  
## 支持的微信版本下载
- [WeCom_4.0.8.6027.exe](https://dldir1.qq.com/wework/work_weixin/WeCom_4.0.8.6027.exe)

## 帮助文档
- 查看 [常见问题](docs/FAQ.md)
- 查看 [常用示例](examples)
- 查看 [ntworkHttp接口示例](fastapi_example)  
- 加入群聊 [NtWork交流群](https://jq.qq.com/?_wv=1027&k=y8d0wpXJ)

## 安装

```bash
pip install ntwork
```
国内源安装
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ntwork
```

## 简单入门实例

有了ntwork，如果你想要给文件传输助手发一条信息，只需要这样

```python
# -*- coding: utf-8 -*-
import sys
import ntwork

wework = ntwork.WeWork()

# 打开pc企业微信, smart: 是否管理已经登录的企业微信
wework.open(smart=True)

# 等待登录
wework.wait_login()

# 向文件助手发送一条消息
wework.send_text(conversation_id="FILEASSIST", content="hello, NtWork")

try:
    while True:
        pass
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
```

## 获取联系人和群列表
```python
# -*- coding: utf-8 -*-
import sys
import ntwork

wework = ntwork.WeWork()

# 打开pc企业微信, smart: 是否管理已经登录的微信
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


# 获取群列表并输出
rooms = wework.get_rooms()
print("群列表: ")
print(rooms)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
```

## 监听消息并自动回复

```python
# -*- coding: utf-8 -*-
import sys
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


try:
    while True:
        pass
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()
```

## 使用fastapi框架实现的web api接口

通过fastapi的swagger在线文档可以很方便的管理ntwork接口

[查看fastapi_example例子](./fastapi_example)

![vfazT0.jpg](https://s1.ax1x.com/2022/09/06/v7zFv4.jpg)


## 使用pyxcgui界面库实现的简单例子

![vcnRfg.jpg](https://s1.ax1x.com/2022/09/06/v7vWT0.jpg)

代码如下：

```python
import xcgui
import ntwork
from xcgui import XApp, XWindow


class ntworkWindow(XWindow):
    def __init__(self):
        super(ntworkWindow, self).__init__()
        self.loadLayout("resources\\send_text_ui.xml")
        self.setMinimumSize(600, 500)

        btn: xcgui.XButton = self.findObjectByName("btn_open")
        btn.regEvent(xcgui.XE_BNCLICK, self.on_btn_open_clicked)

        btn: xcgui.XButton = self.findObjectByName("btn_send")
        btn.regEvent(xcgui.XE_BNCLICK, self.on_btn_send_clicked)

        self.edit_conversation_id: xcgui.XEdit = self.findObjectByName("edit_conversation_id")
        self.edit_content: xcgui.XEdit = self.findObjectByName("edit_content")
        self.edit_log: xcgui.XEdit = self.findObjectByName("edit_log")
        self.edit_log.enableAutoWrap(True)

        self.wework_instance: ntwork.WeWork = None

    def on_btn_open_clicked(self, sender, _):
        self.wework_instance = ntwork.WeWork()
        self.wework_instance.open(smart=True)

        # 监听所有通知消息
        self.wework_instance.on(ntwork.MT_ALL, self.on_recv_message)

    def on_btn_send_clicked(self, sender, _):
        if not self.wework_instance or not self.wework_instance.login_status:
            svg = xcgui.XSvg.loadFile("resources\\warn.svg")
            svg.setSize(16, 16)
            self.notifyMsgWindowPopup(xcgui.position_flag_top, "警告", "请先打开并登录微信",
                                      xcgui.XImage.loadSvg(svg), xcgui.notifyMsg_skin_warning)
        else:
            self.wework_instance.send_text(self.edit_wxid.getText(), self.edit_content.getText())

    def on_recv_message(self, wework, message):
        text = self.edit_log.getText()
        text += "\n"
        text += str(message)
        self.edit_log.setText(text)
        self.redraw()


if __name__ == '__main__':
    app = XApp()
    window = ntworkWindow()
    window.showWindow()
    app.run()
    ntwork.exit_()
    app.exit()
```

帮助&支持
-------------------------
点击链接加入群聊[NtWork交流群](https://jq.qq.com/?_wv=1027&k=y8d0wpXJ)
