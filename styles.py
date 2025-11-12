# -*- coding:utf-8 -*-

"""
功能：定义各种样式
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'

# 落子位样式
box_style = '''QWidget{
                border:1px solid #3ccdad;
                background:#d8f9f2;
                border-radius:50px;
            }'''
# 落子位样式
card_style = '''QLabel{
                border:0px;
                border-radius:48px;
            }'''
# 八路所在单元格被选中的样式
box_era_checked_style = '''QWidget{
                border:4px solid red;
                border-radius:50px;
            }'''
# 敌人所在单元格被选中的样式
box_foe_checked_style = '''QWidget{
                border:4px solid green;
                border-radius:50px;
            }'''

# 可用落子位样式
box_put_available_style = '''QWidget{
                border:2px solid orange;
                background:#d8f9f2;
                border-radius:50px;
            }'''

# 可被攻击的敌人棋子所在box的样式
box_attack_available_box_style = '''QWidget{
                border:4px solid orange;
                border-radius:50px;
            }'''

# 棋盘线条颜色
line_color = "#0063b1"

# 系统消息框样式
message_win_style = """QTextBrowser {
                background-color: #f5f5f5;
                border: 1px solid #3498db;
                border-radius: 8px; 
                padding: 10px; 
                font-family: 'Arial';
                font-size: 15px;
                color: #333333;
            }"""
# 状态框样式
status_panel_style = """QWidget {
                border: 1px solid #2b2d30;
                padding: 10px; 
            }"""
# 分割线样式
separator_line_style = '''QWidget{border:3px solid #780000;}'''

# 系统级信息显示样式
sysinfo_label_style = '''QLabel{
                            background-color: rgba(255, 255, 255, 120);
                            font-family:"华文行楷";
                            color:#ff5500;
                            font-weight:200;
                            font-size:50px;
                            border:0px;
                        }'''