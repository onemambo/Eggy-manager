
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QTreeWidget, QTreeWidgetItem, QScrollArea, QLineEdit, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from process_core import ProcessManager, PriorityAdjuster
from ui_components import ProcessCard

class EGGYMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EGGY管理器")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)

        self.process_manager = ProcessManager()
        self.process_manager.process_updated.connect(self.update_process_cards)

        self.init_layout()

    def init_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)

        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderLabels(["进程分类"])
        self.nav_tree.setColumnWidth(0, 220)
        QTreeWidgetItem(self.nav_tree, ["所有进程"])
        main_layout.addWidget(self.nav_tree)

        right_layout = QVBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索进程...")
        right_layout.addWidget(self.search_box)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20,20,20,20)
        self.scroll_area.setWidget(self.scroll_content)
        right_layout.addWidget(self.scroll_area)

        main_layout.addLayout(right_layout, stretch=1)

    def update_process_cards(self, processes: list):
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()
            if item.layout():
                item.layout().deleteLater()

        if not processes:
            label = QLabel("请以管理员身份启动！")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size:16px; color:red;")
            self.scroll_layout.addWidget(label)
            return

        row = QHBoxLayout()
        for idx, proc in enumerate(processes):
            card = ProcessCard(proc, self)
            row.addWidget(card)
            if (idx+1)%2 == 0:
                self.scroll_layout.addLayout(row)
                row = QHBoxLayout()
        if row.count()>0:
            self.scroll_layout.addLayout(row)

    def on_terminate_click(self, pid: int):
        if ProcessManager.terminate_process(pid):
            QMessageBox.information(self, "成功", f"PID:{pid} 已终止")
        else:
            QMessageBox.warning(self, "失败", "无权限或进程不存在")

    def on_priority_change(self, pid: int, priority_idx: int):
        label = PriorityAdjuster.PRIORITY_LABELS[priority_idx]
        if PriorityAdjuster.set_priority(pid, label):
            QMessageBox.information(self, "成功", f"优先级已改：{label}")
        else:
            QMessageBox.warning(self, "失败", "调整失败")
