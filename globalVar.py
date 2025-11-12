# -*- coding:utf-8 -*-

"""
功能：全局变量管理，保存全局变量及游戏状态
"""

__author__ = 'zhengbin <rjguanwen001@163.com>'


def _init():
    global _global_dict
    _global_dict = {}

# 设置全局变量
def set_value(name, value):
    _global_dict[name] = value

# 获取全局变量
def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue

# 清除键值
def clear_key(name):
    _global_dict.pop(name)


def keys_list():
    return _global_dict.keys()
