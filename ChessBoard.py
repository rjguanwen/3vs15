# -*- coding:utf-8 -*-
""" 主应用程序 """
import logging
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QGridLayout, QApplication, QTextBrowser, QLabel

import constants
import globalVar as GV
import styles
from Box import Box
from Cards import EraCard, FoeCard
from StatusPanel import StatusPanel
from logShow import LogSignal, QtHandler


class ChessBoard(QMainWindow):
    """ 棋盘类 """
    
    def __init__(self):
        super().__init__()

        # 初始化全局变量
        GV._init()
        # 所有落子位
        GV.set_value(constants.ALL_BOXS_KEY, {})
        # 尚存活的敌人棋子
        GV.set_value(constants.LEFT_FOE_KEY, {})
        # 当前选中牌所对应的可行牌的 box 列表，每次选中卡牌是计算更新
        GV.set_value(constants.GS_PUT_AVAILABEL_BOXS, [])
        # 当前选中卡牌所对应的可攻击的敌方卡牌，每次选中战斗区卡牌时计算更新
        GV.set_value(constants.GS_ATTACKED_AVAILABEL_CARDS, [])
        GV.set_value(constants.GS_ATTACKED_AVAILABEL_CARDS_BOXS, [])

        self.setWindowTitle("三个八路十五个敌人")
        self.logger = init_log()
        self.init_ui()

    def init_ui(self):
        """初始化棋盘ui"""
        self.setWindowTitle("三个八路十五个敌人")
        central_widget = QWidget()
        central_widget.setFixedWidth(constants.MAIN_WIN_WIDTH)
        self.setCentralWidget(central_widget)
        # 横向布局
        main_layout = QHBoxLayout(central_widget)

        # 系统消息显示窗口
        self.message_win = QTextBrowser(self)
        self.message_win.setReadOnly(True)
        self.message_win.setFixedWidth(constants.MESSAGE_WIN_WIDTH)
        self.message_win.setStyleSheet(styles.message_win_style)
        self.message_win.setText("<H3>系统消息</H3>")
        # # 定义状态窗口并加入布局
        self.status_win = StatusPanel()
        self.status_win.setFixedWidth(constants.STATUS_WIN_WIDTH)
        main_layout.addWidget(self.status_win)

        # 创建 5*5 的网格布局
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignCenter)
        grid_layout.setContentsMargins(10,10,10,10)
        grid_layout.setSpacing(50)
        for row in range(5):
            for col in range(5):
                # 生成落子位
                box_name = ChessBoard.gen_box_name(row+1, col+1)
                box = Box(box_name, row+1, col+1)
                # 放到网格
                grid_layout.addWidget(box, row, col)
                # 将落子位存入全局变量，方便后续画网格线以及判断可行棋位置使用
                GV.get_value(constants.ALL_BOXS_KEY).update({box_name: box})
                # 所有落子位绑定点击事件
                box.clicked.connect(self.box_clicked)
        main_layout.addLayout(grid_layout)
        # 将系统消息窗口加入主窗口布局
        main_layout.addWidget(self.message_win)

        # self.logger.debug(GV.get_value(constants.ALL_BOXS_KEY))

    def paintEvent(self, a0, QPaintEvent=None):
        """
        覆写paintEvent方法，为棋盘画框线
        :param a0:
        :param QPaintEvent:
        :return:
        """
        # self.logger.info("ChessBoard -- PaintEvent - start...")
        painter = QPainter(self)
        # 设置颜色
        color = QColor(styles.line_color)
        painter.setPen(color)
        # 落子位的半径
        box_r = constants.BOX_WIDTH//2
        # 获取周边落子位的坐标，用于画框线
        box_11 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(1, 1))
        x11, y11 = box_11.x() + box_r, box_11.y() + box_r
        box_12 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(1, 2))
        x12, y12 = box_12.x() + box_r, box_12.y() + box_r
        box_13 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(1, 3))
        x13, y13 = box_13.x() + box_r, box_13.y() + box_r
        box_14 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(1, 4))
        x14, y14 = box_14.x() + box_r, box_14.y() + box_r
        box_15 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(1, 5))
        x15, y15 = box_15.x() + box_r, box_15.y() + box_r

        box_21 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(2, 1))
        x21, y21 = box_21.x() + box_r, box_21.y() + box_r
        box_31 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(3, 1))
        x31, y31 = box_31.x() + box_r, box_31.y() + box_r
        box_41 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(4, 1))
        x41, y41 = box_41.x() + box_r, box_41.y() + box_r
        box_51 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 1))
        x51, y51 = box_51.x() + box_r, box_51.y() + box_r

        box_52 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 2))
        x52, y52 = box_52.x() + box_r, box_52.y() + box_r
        box_53 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 3))
        x53, y53 = box_53.x() + box_r, box_53.y() + box_r
        box_54 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 4))
        x54, y54 = box_54.x() + box_r, box_54.y() + box_r
        box_55 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 5))
        x55, y55 = box_55.x() + box_r, box_55.y() + box_r

        box_25 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(2, 5))
        x25, y25 = box_25.x() + box_r, box_25.y() + box_r
        box_35 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(3, 5))
        x35, y35 = box_35.x() + box_r, box_35.y() + box_r
        box_45 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(4, 5))
        x45, y45 = box_45.x() + box_r, box_45.y() + box_r
        # 画网格线
        painter.drawLine(x11, y11, x15, y15)
        painter.drawLine(x21, y21, x25, y25)
        painter.drawLine(x31, y31, x35, y35)
        painter.drawLine(x41, y41, x45, y45)
        painter.drawLine(x51, y51, x55, y55)
        painter.drawLine(x11, y11, x51, y51)
        painter.drawLine(x12, y12, x52, y52)
        painter.drawLine(x13, y13, x53, y53)
        painter.drawLine(x14, y14, x54, y54)
        painter.drawLine(x15, y15, x55, y55)

        # self.logger.info("ChessBoard -- PaintEvent - end!!!")

    @staticmethod
    def gen_box_name(row, col):
        """
        根据Box的行列，为Box生成一个名字
        :param row: 行号
        :param col: 列号
        :return: 名称，格式为“box:X-Y”
        """
        return f"box:{row}-{col}"

    def show_message(self, message_text, font_color="black"):
        """
        在右侧消息栏，显示系统消息
        :param message_text:
        :return:
        """
        message_text_show = f"<p style='color: {font_color};'>{message_text}</p>"
        self.message_win.append(message_text_show)
        cursor = self.message_win.textCursor()
        cursor.movePosition(cursor.End)
        self.message_win.setTextCursor(cursor)

    def game_init(self):
        """
        游戏初始化
        1、生成双方棋子
        2、全屏显示游戏开始提示
        3、设置游戏初始变量：当前玩家、当前回合数
        :return:
        """
        self.logger.info("ChessBoard -- game_init - start...")

        # 生成八路与敌人的棋子，摆放到棋盘的相应位置，并为其绑定点击动作
        self.put_era_init()
        self.put_foe_init()
        # 全屏显示游戏开始信息
        self.show_game_start_info()
        # 八路首先行动，将当前玩家设置为八路
        GV.set_value(constants.GS_CURRENT_USER, constants.PLAYER_ERA)
        # 设置回合数为第一回合
        GV.set_value(constants.GS_CURRENT_ROUND_NUM, 1)


        self.logger.info("ChessBoard -- game_init - end!!!")

    def put_era_init(self):
        """
        在指定的落子位摆放八路棋子，用于游戏初始化
        :return:
        """
        # 生成三个八路的棋子并放置到棋盘
        self.era_l = EraCard("era_l", row=5, col=1)
        self.era_m = EraCard("era_m", row=5, col=3)
        self.era_r = EraCard("era_r", row=5, col=5)
        # 存入全局变量，方便后续使用
        GV.set_value("era_l", self.era_l)
        GV.set_value("era_m", self.era_m)
        GV.set_value("era_r", self.era_r)
        # 获取八路棋子的落子位
        box_51 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 1))
        box_53 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 3))
        box_55 = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(5, 5))
        # 摆放八路棋子
        box_51.layout().addWidget(self.era_l)
        box_53.layout().addWidget(self.era_m)
        box_55.layout().addWidget(self.era_r)
        # 绑定点击事件
        self.era_l.clicked.connect(self.era_clicked)
        self.era_m.clicked.connect(self.era_clicked)
        self.era_r.clicked.connect(self.era_clicked)

    def put_foe_init(self):
        """
        在指定的落子位摆放敌人棋子，用于游戏初始化
        :return:
        """
        foe_seq = 0
        for r in range(3):
            for c in range(5):
                # 生成一个新敌人
                foe_seq += 1
                foe_name = f"foe:{foe_seq}"
                tmp_foe = FoeCard(foe_name, r+1, c+1)
                # 将新生成的敌人存入全局变量
                GV.get_value(constants.LEFT_FOE_KEY).update({foe_name: tmp_foe})
                # 将新生成的敌人放入棋盘
                tmp_box = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(r+1, c+1))
                tmp_box.layout().addWidget(tmp_foe)
                # 绑定点击事件
                tmp_foe.clicked.connect(self.foe_clicked)

    def era_clicked(self, name, current_row, current_col):
        """
        点击八路牌的动作：
        在本游戏中八路只有两个动作，向周边四个点位运动一步，跨一个空位吃掉敌人。八路棋子被点击时，依据该规则计算其可行棋位置。
        :param name: 卡牌名称
        :param current_row: 所在行号
        :param current_col: 所在列号
        :return:
        """
        self.logger.info("ChessBoard -- era_clicked - start...")
        if GV.get_value(constants.GS_CURRENT_USER) == constants.PLAYER_ERA:
            # 清理可能存在的选中状态
            self.clear_box_checked_status()
            self.clear_put_available_box_status()
            self.clear_attack_available_card_box_status()

            # 用全局变量记录当前选中棋子，并设置其选中状态
            current_card = GV.get_value(name)
            # self.logger.debug(f"====>clicked card :{current_card.name} ==>{current_card.row},{current_card.col}")
            GV.set_value(constants.GS_CURRENT_CARD_CHECKED, current_card)
            current_box = current_card.parent()
            # self.logger.debug(f"====>clicked box :{current_box.row},{current_box.col}")
            self.add_box_checked_status(current_box)

            # 按上下左右四个方向检索可用落子位，检测的规则为：
            # 1、紧挨着八路的上下左右四个点位，如果是空位，则八路可以移动到该点位
            # 2、如果八路上下左右四个方向上，隔着一个空位的位置上有敌人棋子，则八路可以直接吃掉该棋子并将自身落在该点位
            # 3、八路不可以吃掉紧邻着的敌方棋子
            # 4、八路不可以跨越棋子行棋，不论是己方棋子还是敌方棋子

            # 下面，首先检测上方的两个落子位是否可用，如可用则加入可用列表，方便后续处理
            self.logger.debug(f"当前点击的card==>row:{current_row},col:{current_col}")
            up_box = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(current_row-1, current_col))
            self.logger.debug(up_box)
            if up_box is not None:
                self.logger.debug(up_box.isEmpty())
                self.logger.debug(up_box.get_card())
                if up_box.isEmpty():
                    # 如果上方落子位存在，且为空，则将该落子位加入可用列表
                    self.add_pub_available_box_status(up_box)
                    # 继续判断上方的上方点位情况
                    up_up_box = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(current_row-2, current_col))
                    if up_up_box is not None:
                        if up_up_box.isEmpty() is False:
                            # 获取该点位上的棋子
                            card = up_up_box.get_card()
                            if card.getFaction() == constants.PLAYER_FOE:
                                # 如果上方的上方点位上有敌方棋子，则将其加入可用列表
                                self.add_attack_available_card_box_status(card, up_up_box)
            # 检测左侧点位
            left_box = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(current_row, current_col-1))
            if left_box is not None:
                if left_box.isEmpty():
                    # 如果左侧落子位存在，且为空，则将该落子位加入可用列表
                    self.add_pub_available_box_status(left_box)
                    # 继续判断左侧的左侧点位情况
                    left_left_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                        ChessBoard.gen_box_name(current_row, current_col-2))
                    if left_left_box is not None:
                        if left_left_box.isEmpty() is False:
                            # 获取该点位上的棋子
                            card = left_left_box.get_card()
                            if card.getFaction() == constants.PLAYER_FOE:
                                # 如果上方的上方点位上有敌方棋子，则将其加入可用列表
                                self.add_attack_available_card_box_status(card, left_left_box)
            # 检测下方点位
            down_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                ChessBoard.gen_box_name(current_row+1, current_col))
            if down_box is not None:
                if down_box.isEmpty():
                    # 如果上方落子位存在，且为空，则将该落子位加入可用列表
                    self.add_pub_available_box_status(down_box)
                    # 继续判断上方的上方点位情况
                    down_down_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                        ChessBoard.gen_box_name(current_row+2, current_col))
                    if down_down_box is not None:
                        if down_down_box.isEmpty() is False:
                            # 获取该点位上的棋子
                            card = down_down_box.get_card()
                            if card.getFaction() == constants.PLAYER_FOE:
                                # 如果上方的上方点位上有敌方棋子，则将其加入可用列表
                                self.add_attack_available_card_box_status(card, down_down_box)
            # 检测右侧点位
            right_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                ChessBoard.gen_box_name(current_row, current_col+1))
            if right_box is not None:
                if right_box.isEmpty():
                    # 如果左侧落子位存在，且为空，则将该落子位加入可用列表
                    self.add_pub_available_box_status(right_box)
                    # 继续判断左侧的左侧点位情况
                    right_right_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                        ChessBoard.gen_box_name(current_row, current_col+2))
                    if right_right_box is not None:
                        if right_right_box.isEmpty() is False:
                            # 获取该点位上的棋子
                            card = right_right_box.get_card()
                            if card.getFaction() == constants.PLAYER_FOE:
                                # 如果上方的上方点位上有敌方棋子，则将其加入可用列表
                                self.add_attack_available_card_box_status(card, right_right_box)
        else:
            # 敌人行棋时，点击八路棋子无需响应
            pass

        self.logger.info("ChessBoard -- era_clicked - end!!!")

    def foe_clicked(self, name, current_row, current_col):
        """
        点击敌人牌的动作
        :param name: 卡牌名称
        :param current_row: 所在行号
        :param current_col: 所在列号
        :return:
        """
        self.logger.info("ChessBoard -- foe_clicked - start")
        if GV.get_value(constants.GS_CURRENT_USER) == constants.PLAYER_FOE:
            # 清理可能存在的选中状态
            self.clear_box_checked_status()
            self.clear_put_available_box_status()
            self.clear_attack_available_card_box_status()
            # 找到当前选中棋子，并用全局变量记录，然后设置其选中状态
            current_card = GV.get_value(constants.LEFT_FOE_KEY).get(name)
            GV.set_value(constants.GS_CURRENT_CARD_CHECKED, current_card)
            current_box = current_card.parent()
            self.add_box_checked_status(current_box)

            # 如果当前行棋方为敌人，则敌人棋子被点击时，计算其可落子位置
            # 可用落子位计算规则位，当前棋子上下左右四个方向相邻的空落子位即为可落子位
            # 检测上方点位
            up_box = GV.get_value(constants.ALL_BOXS_KEY).get(ChessBoard.gen_box_name(current_row-1, current_col))
            if up_box is not None:
                if up_box.isEmpty():
                    self.add_pub_available_box_status(up_box)
            # 检测左侧点位
            lef_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                ChessBoard.gen_box_name(current_row, current_col - 1))
            if lef_box is not None:
                if lef_box.isEmpty():
                    self.add_pub_available_box_status(lef_box)
            # 检测下方点位
            down_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                ChessBoard.gen_box_name(current_row+1, current_col))
            if down_box is not None:
                if down_box.isEmpty():
                    self.add_pub_available_box_status(down_box)
            # 检测右侧点位
            right_box = GV.get_value(constants.ALL_BOXS_KEY).get(
                ChessBoard.gen_box_name(current_row, current_col+1))
            if right_box is not None:
                if right_box.isEmpty():
                    self.add_pub_available_box_status(right_box)
        else:
            # 如果当前行棋方为八路，则看当前棋子是否可被攻击
            # 如可被攻击则被敌人吃掉，否则没有动作
            # 找到被点击棋子
            current_card = GV.get_value(constants.LEFT_FOE_KEY).get(name)
            if current_card in GV.get_value(constants.GS_ATTACKED_AVAILABEL_CARDS):
                # 如果当前棋子可被攻击，则移除该棋子，并将八路棋子移动当前点位
                # 1. 移除棋子
                current_card.parent().layout().removeWidget(current_card)
                # 2. 安全删除控件
                current_card.deleteLater()
                # 3. 将攻击卡牌移动到当前点位
                self.move_card_to_new_box(GV.get_value(constants.GS_CURRENT_CARD_CHECKED), current_card.parent())
                # 交换行棋方
                self.change_player()
            pass
        self.logger.info("ChessBoard -- foe_clicked - end")

    def box_clicked(self, name, current_row, current_col):
        """
        点击落子位的动作，判断落子位是否为当前选中棋子的可行棋位，是则行棋，否则无动作
        :param name:
        :param current_row:
        :param current_col:
        :return:
        """
        to_box = GV.get_value(constants.ALL_BOXS_KEY).get(name)
        if to_box in GV.get_value(constants.GS_PUT_AVAILABEL_BOXS):
            # 如果当前位可落子位，则将棋子移动到当前位置
            c_card = GV.get_value(constants.GS_CURRENT_CARD_CHECKED)
            from_box = GV.get_value(constants.ALL_BOXS_KEY).get(self.gen_box_name(c_card.row, c_card.col))
            # 移动棋子
            self.move_card_to_new_box(c_card, to_box)
            # 行棋后交换行棋方
            self.change_player()
        else:
            self.logger.debug(f"{name},无操作")
            pass

    def move_card_to_new_box(self, card, to_box):
        """
        将棋子由一个落子位移动到另一个落子位
        :param card:
        :param from_box:
        :param to_box:
        :return:
        """
        to_box.layout().addWidget(card)
        card.row = to_box.row
        card.col = to_box.col
        self.clear_attack_available_card_box_status()
        self.clear_put_available_box_status()
        self.clear_box_checked_status()

    def add_box_checked_status(self, box):
        """
        为选中的点位增加选中状态
        :return:
        """
        # 设置全局状态参数并设置当前点位样式
        GV.set_value(constants.GS_CURRENT_BOX_CHECKED, box)
        box.setStyleSheet(styles.box_era_checked_style)

    def clear_box_checked_status(self):
        """
        清除落子位的选中状态
        :return:
        """
        box = GV.get_value(constants.GS_CURRENT_BOX_CHECKED)
        if box is not None:
            box.setStyleSheet(styles.box_style)
            GV.clear_key(constants.GS_CURRENT_BOX_CHECKED)
            GV.clear_key(constants.GS_CURRENT_CARD_CHECKED)

    def add_pub_available_box_status(self, box):
        """为可用落子位增加状态"""
        self.logger.info("ChessBoard -- add_pub_available_box_status - start...")
        GV.get_value(constants.GS_PUT_AVAILABEL_BOXS).append(box)
        box.setCursor(Qt.PointingHandCursor)
        box.setStyleSheet(styles.box_put_available_style)
        self.logger.info("ChessBoard -- add_pub_available_box_status - end!!!")

    def clear_put_available_box_status(self):
        """清除可用落子位状态"""
        for box in GV.get_value(constants.GS_PUT_AVAILABEL_BOXS):
            box.setCursor(Qt.ArrowCursor)
            box.setStyleSheet(styles.box_style)
        GV.set_value(constants.GS_PUT_AVAILABEL_BOXS, [])

    def add_attack_available_card_box_status(self, card, box):
        """增加敌方棋子可被攻击状态"""
        GV.get_value(constants.GS_ATTACKED_AVAILABEL_CARDS).append(card)
        GV.get_value(constants.GS_ATTACKED_AVAILABEL_CARDS_BOXS).append(box)
        box.setCursor(Qt.PointingHandCursor)
        box.setStyleSheet(styles.box_attack_available_box_style)

    def clear_attack_available_card_box_status(self):
        """清除敌方棋子可被攻击状态"""
        for box in GV.get_value(constants.GS_ATTACKED_AVAILABEL_CARDS_BOXS):
            box.setCursor(Qt.ArrowCursor)
            box.setStyleSheet(styles.box_style)
        GV.set_value(constants.GS_ATTACKED_AVAILABEL_CARDS, [])
        GV.set_value(constants.GS_ATTACKED_AVAILABEL_CARDS_BOXS, [])

    def change_player(self):
        """交换当前玩家"""
        if GV.get_value(constants.GS_CURRENT_USER) == constants.PLAYER_ERA:
            GV.set_value(constants.GS_CURRENT_USER, constants.PLAYER_FOE)
            self.show_message("请敌人方行棋！", "blue")
        else:
            GV.set_value(constants.GS_CURRENT_USER, constants.PLAYER_ERA)
            self.show_message("请八路方行棋！", "red")


    def show_game_start_info(self):
        """
        显示游戏开始信息，并提示由八路先行棋
        :return:
        """
        sysinfo_label = QLabel(self)
        sysinfo_label.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        sysinfo_label.setStyleSheet(styles.sysinfo_label_style)
        sysinfo_label.setText("游戏开始，八路先行棋！")
        sysinfo_label.setAlignment(Qt.AlignCenter)
        main_widget_rect = self.geometry()
        sysinfo_label.setGeometry(0, 0, constants.MAIN_WIN_WIDTH, main_widget_rect.height())
        sysinfo_label.show()
        # 1秒后自动关闭
        QTimer().singleShot(1500, sysinfo_label.close)
        self.show_message("八路先行棋！", "red")

    def is_game_over(self):
        # TODO: 判断游戏是否已结束，并发出相关信号
        pass


def init_log():
    """
    初始化日志系统
    :param update_log:
    :return:
    """
    log_signal = LogSignal()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，将日志写入文件
    file_handler = logging.FileHandler('application.log', encoding="utf-8")  # 文件处理器
    file_handler.setLevel(logging.INFO)  # 设置文件日志的级别
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # 创建自定义处理器，就日志输出到 Qt 页面显示
    qt_handler = QtHandler(log_signal)  # 使用自定义的日志处理器
    qt_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(qt_handler)

    stream_handler = logging.StreamHandler()  # 输出到控制台
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s "))
    logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessBoard()
    window.game_init()
    window.show()
    sys.exit(app.exec_())
