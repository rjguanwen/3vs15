# -*- coding:utf-8 -*-

"""
功能：棋子
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'

from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter, QPixmap, QWindow, QImage, QBrush
from PyQt5.QtWidgets import QFrame, QLabel

import constants
import styles


class Card(QLabel):
    """棋子基类"""

    def __init__(self):
        super().__init__()

    def removeCardSelf(self):
        """
        移除棋子
        :return:
        """
        # 移除卡牌
        self.parent().layout().removeWidget(self)
        # 安全删除控件
        self.deleteLater()

    def getFaction(self):
        """
        获取卡牌所属阵营
        :return:
        """
        return self.faction

    def enterEvent(self, *args, **kwargs):
        """
        鼠标悬停效果
        :param args:
        :param kwargs:
        :return:
        """
        # 鼠标样式
        self.is_cursor_on = True

    def leaveEvent(self, *args, **kwargs):
        self.is_cursor_on = False

    clicked = pyqtSignal(str, int, int)

    def mousePressEvent(self, *args, **kwargs):
        """
        定义鼠标点击事件
        :param args:
        :param kwargs:
        :return:
        """
        self.clicked.emit(self.name, self.row, self.col)


class EraCard(Card):
    """棋子：八路"""

    def __init__(self, name, row, col):
        """
        八路棋子初始化
        :param name: 名称
        :param row: 行号
        :param col: 列号
        """
        super().__init__()
        self.name = name
        self.row = row
        self.col = col
        self.init_ui()
        # 棋子阵营
        self.faction = constants.PLAYER_ERA

    def init_ui(self):
        # 设置样式
        self.setStyleSheet(styles.card_style)
        # 设置背景图片，并以圆形显示
        imgpath = "images/era_2.png"
        imgdata = open(imgpath, 'rb').read()
        pixmap = mask_image(imgdata)
        self.setPixmap(pixmap)


class FoeCard(Card):
    """棋子：敌人"""

    def __init__(self, name, row, col):
        """
        敌人棋子初始化
        :param name: 名称
        :param row: 行号
        :param col: 列号
        """
        super().__init__()
        self.name = name
        self.row = row
        self.col = col
        self.init_ui()
        # 棋子阵营
        self.faction = constants.PLAYER_FOE

    def init_ui(self):
        # 设置样式
        self.setStyleSheet(styles.card_style)
        # 设置背景图片，并以圆形显示
        imgpath = "images/foe_1.jpg"
        imgdata = open(imgpath, 'rb').read()
        pixmap = mask_image(imgdata, imgtype='jpg')
        self.setPixmap(pixmap)


def mask_image(imgdata, imgtype='png', out_R=constants.BOX_WIDTH-2):
    """
    通过遮罩将图像转化为指定大小圆形图片
    :param imgdata:
    :param imgtype:
    :param size:
    :param out_width:
    :param out_height:
    :return:
    """
    # Load image
    image = QImage.fromData(imgdata, imgtype)

    # convert image to 32-bit ARGB (adds an alpha
    # channel ie transparency factor):
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) // 2,
        (image.height() - imgsize) // 2,
        imgsize,
        imgsize,
    )

    image = image.copy(rect)

    # Create the output image with the same dimensions
    # and an alpha channel and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle
    # with the original image onto the output image:
    brush = QBrush(image)

    # Paint the output image
    painter = QPainter(out_img)
    painter.setBrush(brush)

    # Don't draw an outline
    painter.setPen(Qt.NoPen)

    # drawing circle
    painter.drawEllipse(0, 0, imgsize, imgsize)

    # closing painter event
    painter.end()

    # Convert the image to a pixmap and rescale it.
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    # size *= pr
    pm = pm.scaled(out_R, out_R, Qt.KeepAspectRatio,
                   Qt.SmoothTransformation)

    # return back the pixmap data
    return pm