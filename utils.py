from PyQt6.QtWidgets import QApplication

def set_modern_theme():
    """设置全局现代化QSS样式（圆角、阴影、配色）"""
    app = QApplication.instance()
    if not app:
        return
    
    modern_qss = """
        /* 全局窗口样式 */
        QMainWindow {
            background-color: #f5f7fa;
            color: #2d3748;
        }

        /* 左侧导航树 */
        QTreeWidget {
            background-color: #ffffff;
            border: none;
            border-right: 1px solid #e2e8f0;
            font-size: 14px;
        }
        QTreeWidget::item {
            height: 30px;
            padding-left: 10px;
        }
        QTreeWidget::item:selected {
            background-color: #e6f7ff;
            color: #1890ff;
            border-radius: 8px;
        }

        /* 搜索框 */
        QLineEdit {
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 8px 16px;
            font-size: 14px;
            margin: 10px 20px;
            background-color: #ffffff;
        }
        QLineEdit:focus {
            border-color: #1890ff;
            outline: none;
        }

        /* 滚动区域 */
        QScrollArea {
            border: none;
            background-color: transparent;
        }

        /* 按钮通用样式 */
        QPushButton {
            border: none;
            border-radius: 10px;
            padding: 6px 16px;
            font-size: 13px;
            cursor: pointer;
        }
        QPushButton:hover {
            opacity: 0.9;
        }
        QPushButton#TerminateBtn {
            background-color: #ff4d4f;
            color: white;
        }
        QPushButton#TerminateBtn:hover {
            background-color: #f5222d;
        }

        /* 下拉框（优先级选择） */
        QComboBox {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 13px;
            background-color: #ffffff;
        }
        QComboBox:focus {
            border-color: #1890ff;
            outline: none;
        }
    """
    app.setStyleSheet(modern_qss)