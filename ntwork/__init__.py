from .conf import VERSION
from .core.wework import WeWork
from .wc import wcprobe
from .const.notify_type import *
from .exception import *
from . import conf

__version__ = VERSION


def set_wework_exe_path(wework_exe_path=None, wework_version=None):
    """
    自定义企业微信路径
    """
    conf.DEFAULT_WEWORK_EXE_PATH = wework_exe_path
    conf.DEFAULT_WEWORK_VERSION = wework_version


def get_install_wework_version() -> str:
    """
    获取安装的企业微信的版本号
    """
    return wcprobe.get_install_wework_version()


def exit_():
    """
    退出
    """
    wcprobe.exit()
