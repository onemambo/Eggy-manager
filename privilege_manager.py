import ctypes
import sys
from PyQt6.QtWidgets import QMessageBox

class PrivilegeManager:
    @staticmethod
    def is_admin() -> bool:
        """检测当前进程是否拥有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    @staticmethod
    def request_admin_privilege():
        """请求管理员权限（重启程序并提权）"""
        try:
            # 以管理员身份重启当前程序
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1  # 1=SW_SHOWNORMAL
            )
            sys.exit(0)  # 退出当前非管理员进程
        except Exception as e:
            QMessageBox.critical(None, "权限错误", f"请求管理员权限失败：{str(e)}")

    @staticmethod
    def terminate_with_system_privilege(pid: int) -> bool:
        """
        以System权限终止进程（Windows下需系统服务支持，简化版暂提示需管理员）
        注：完整System权限需创建Windows服务，此处为预留接口
        """
        QMessageBox.warning(
            None, "权限说明", 
            f"无法以管理员权限终止PID:{pid}（可能是System进程）\n"
            "完整System权限需安装系统服务，当前版本暂不支持"
        )
        return False