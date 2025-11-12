# -*- coding:utf-8 -*-

"""
功能：游戏状态显示框
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout

import constants
import styles


class StatusPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        self.setFixedWidth(constants.STATUS_WIN_WIDTH)
        self.setStyleSheet(styles.status_panel_style)

        self.foe_panel = QWidget(self)
        main_layout.addWidget(self.foe_panel)

        # 加入分割线
        sp_line = QFrame()
        sp_line.setFrameShape(QFrame.HLine)
        sp_line.setFrameShadow(QFrame.Sunken)
        sp_line.setStyleSheet(styles.separator_line_style)
        main_layout.addWidget(sp_line)

        self.era_panel = QWidget(self)
        main_layout.addWidget(self.era_panel)




