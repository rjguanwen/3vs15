# -*- coding:utf-8 -*-

"""
功能：
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'


# 版本号
VERSION = 'V0.0.1'

# 是否显示日志窗口
IS_LOGWIN_SHOW = False
# 整个棋盘的宽度
MAIN_WIN_WIDTH = 1150
# 日志窗口与消息窗口的宽度
STATUS_WIN_WIDTH = 200
MESSAGE_WIN_WIDTH = 200

# 卡牌位大小
BOX_WIDTH = 100

# 回合持续时间（秒）
ROUND_TIME = 100
#
# # 攻击动画定义
# FIGHTING_ANIMATION_DEFAULT = {
#     "image_path": "./images/gif/explosion_4.gif",
#     "width": 300,
#     "height": 300,
#     "speed": 100,
#     "duration": 1650
# }
#
# FIGHTING_ANIMATION_2 = {
#     "image_path": "./images/gif/boom.gif",
#     "width": 300,
#     "height": 300,
#     "speed": 100,
#     "duration": 2000
# }

# 玩家：三个八路玩家与十五个敌人玩家
PLAYER_ERA = 0
PLAYER_FOE = 1

# 游戏允许的最大回合数
MAX_ROUND_ALLOWED = 100

# ---- 游戏状态的各种key值 ----
# 当前执行动作的玩家
GS_CURRENT_USER = 'ct_user_glb'
# 当前正在执行的动作类型
GS_CURRENT_ACTION_TYPE = 'ct_action_type_glb'
# 当前回合数
GS_CURRENT_ROUND_NUM = 'cr_round_num_glb'

# 当前被选中的的box及card
GS_CURRENT_BOX_CHECKED = 'ct_box_checked_glb'
GS_CURRENT_CARD_CHECKED = 'ct_card_checked_glb'
# 当前选中的 card，可行牌的 box 列表
GS_PUT_AVAILABEL_BOXS = 'ct_availabel_move_boxs'
# 当前选中的 card，可以攻击的敌方 car 列表及其所在 box 列表
GS_ATTACKED_AVAILABEL_CARDS = 'ct_availabel_attacked_cards'
GS_ATTACKED_AVAILABEL_CARDS_BOXS = 'ct_availabel_attacked_cards_boxs'
# 该key值，存储所有战斗区的 box
ALL_BOXS_KEY = 'll_all_boxs_glb'
# 该key值，存储所有尚存活的敌人棋子
LEFT_FOE_KEY = 'll_left_foe_glb'
#
# # 该key值,存储鼠标样式
# CURSOR_ATTACK_JIAN_KEY = 'll_cursor_attack_jian'
# # 该key值，存储双方玩家的英雄面板
# NORTH_HERO_AVATAR = 'll_north_hero_avatar'
# SOUTH_HERO_AVATAR = 'll_south_hero_avatar'
