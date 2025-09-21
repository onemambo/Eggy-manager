import psutil
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from privilege_manager import PrivilegeManager

class PriorityAdjuster:
    PRIORITY_MAP = {
        psutil.IDLE_PRIORITY_CLASS: "低",
        psutil.BELOW_NORMAL_PRIORITY_CLASS: "低于标准",
        psutil.NORMAL_PRIORITY_CLASS: "标准",
        psutil.ABOVE_NORMAL_PRIORITY_CLASS: "高于标准",
        psutil.HIGH_PRIORITY_CLASS: "高",
        psutil.REALTIME_PRIORITY_CLASS: "实时"
    }
    PRIORITY_LABELS = list(PRIORITY_MAP.values())
    LABEL_TO_PRIORITY = {v: k for k, v in PRIORITY_MAP.items()}

    @staticmethod
    def set_priority(pid: int, priority_label: str) -> bool:
        try:
            priority = PriorityAdjuster.LABEL_TO_PRIORITY[priority_label]
            process = psutil.Process(pid)
            process.nice(priority)
            return True
        except Exception:
            return False

class ProcessManager(QObject):
    process_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.refresh_processes)
        self.timer.start()

    def refresh_processes(self):
        processes = []
        try:
            for proc in psutil.processes():
                try:
                    processes.append({
                        "name": proc.name(),
                        "pid": proc.pid,
                        "status": str(proc.status()),
                        "priority": "标准"
                    })
                except:
                    processes.append({
                        "name": "未知进程",
                        "pid": proc.pid,
                        "status": "无权限",
                        "priority": "未知"
                    })
            processes.sort(key=lambda x: x["pid"])
        except Exception as e:
            print(f"刷新进程错误: {str(e)}")
        self.process_updated.emit(processes)

    @staticmethod
    def terminate_process(pid: int) -> bool:
        try:
            if not PrivilegeManager.is_admin():
                PrivilegeManager.request_admin_privilege()
                return False
            process = psutil.Process(pid)
            process.terminate()
            return True
        except Exception:
            return False
