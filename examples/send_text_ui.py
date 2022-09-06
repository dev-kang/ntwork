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
