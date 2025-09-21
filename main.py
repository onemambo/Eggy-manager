import sys
from PyQt6.QtWidgets import QApplication
from main_window import EGGYMainWindow
from utils import set_modern_theme

if __name__ == "__main__":
    # 初始化Qt应用
    app = QApplication(sys.argv)
    
    # 设置现代化主题（圆角、阴影、配色）
    set_modern_theme()
    
    # 启动主窗口
    window = EGGYMainWindow()
    window.show()
    
    # 程序循环
    sys.exit(app.exec())