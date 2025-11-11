# -*- coding: utf-8 -*-
# @Time: 2025/10/16 11:52
# @Author: lxc
# @File: setting.py
# @Software: PyCharm
import toml


def get_config():
    """
    获取配置文件。
    Get the configuration file.
    """
    with open("config/config.toml", "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


CONFIG = get_config()


def reload_config():
    """
    重新加载配置文件。
    Reload the configuration file.
    """
    global CONFIG
    CONFIG = get_config()


def get_config_value(section: str, key: str = None):
    """
    获取配置文件指定key的值。
    Get the value of the specified key in the configuration file.
    """
    if key:
        return CONFIG[section][key]
    return CONFIG[section]


if __name__ == '__main__':
    print(get_config_value("feishu_api"))
