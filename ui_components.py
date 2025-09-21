from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt
from process_core import PriorityAdjuster

class ProcessCard(QWidget):
    """进程卡片组件（圆角、阴影、包含进程信息与操作按钮）"""
    def __init__(self, process_info: dict, parent=None):
        super().__init__(parent)
        self.process_info = process_info  # 进程信息：name、pid、status、priority
        self.init_ui()

    def init_ui(self):
        # 卡片基础样式（圆角、阴影）
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                margin: 0 20px 20px 0;
            }
        """)
        self.setFixedSize(280, 220)  # 固定卡片尺寸（美观统一）

        # 卡片内部布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # 1. 进程名称（加粗）
        self.name_label = QLabel(self.process_info["name"])
        self.name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #2d3748;")
        layout.addWidget(self.name_label)

        # 2. PID
        self.pid_label = QLabel(f"PID: {self.process_info['pid']}")
        self.pid_label.setStyleSheet("font-size: 13px; color: #718096;")
        layout.addWidget(self.pid_label)

        # 3. 进程状态
        self.status_label = QLabel(f"状态: {self.process_info['status']}")
        self.status_label.setStyleSheet("font-size: 13px; color: #718096;")
        layout.addWidget(self.status_label)

        # 4. 优先级调整下拉框
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(PriorityAdjuster.PRIORITY_LABELS)
        # 匹配当前进程优先级并设置默认值
        current_priority = self.process_info["priority"]
        if current_priority in PriorityAdjuster.PRIORITY_MAP:
            idx = PriorityAdjuster.PRIORITY_LABELS.index(
                PriorityAdjuster.PRIORITY_MAP[current_priority]
            )
            self.priority_combo.setCurrentIndex(idx)
        layout.addWidget(self.priority_combo)

        # 5. 终止进程按钮
        self.terminate_btn = QPushButton("终止进程")
        self.terminate_btn.setObjectName("TerminateBtn")  # 关联QSS样式
        layout.addWidget(self.terminate_btn)

        # 绑定按钮点击事件（由主窗口实现具体逻辑）
        self.terminate_btn.clicked.connect(
            lambda: self.parent().on_terminate_click(self.process_info["pid"])
        )
        # 绑定优先级变更事件
        self.priority_combo.currentIndexChanged.connect(
            lambda idx: self.parent().on_priority_change(
                self.process_info["pid"], idx
            )
        )