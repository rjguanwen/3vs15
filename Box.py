# -*- coding:utf-8 -*-

"""
功能：棋盘落子
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

import constants
import styles


class Box(QFrame):
    """棋盘落子位"""

    def __init__(self, name, row, col):
        super().__init__()
        self.name = name
        self.row = row
        self.col = col
        self.init_ui()

    def init_ui(self):
        # 设置大小
        self.setFixedSize(constants.BOX_WIDTH, constants.BOX_WIDTH)
        # 设置样式
        self.setStyleSheet(styles.box_style)
        # 设置布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    # 定义信号
    clicked = pyqtSignal(str, int, int)

    def mousePressEvent(self, event):
        """自定义鼠标点击事件"""
        self.clicked.emit(self.name, self.row, self.col)

    def isEmpty(self):
        """判断本Box是否为空"""
        if self.get_card() is None:
            return True
        else:
            return False

    def get_card(self):
        """
        获取本落子位上的棋子，如果没有则返回 None
        :return:
        """
        child = self.findChild(QLabel)
        return child
