#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import ast
import os
import configparser
from libs.config.conf import PEROJECT_PATH

class ReadConfig:
    """配置文件"""
    def __init__(self, name, env, ini_name=None, values=None):
        INI_PATH = os.path.join(PEROJECT_PATH, name, 'env', env, 'config.ini')
        if not os.path.exists(INI_PATH):
            raise FileNotFoundError("配置文件%s不存在！" % INI_PATH)
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(INI_PATH, encoding='utf-8')
        self.ini_name = ini_name
        self.values = values


    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    @property
    def url(self):
        return self._get('HOST', 'url')

    @property
    def db(self):
        return self._get('SQL','db')

if __name__ == '__main__':
    a = ReadConfig('POP','test','db_name').get('SQL','db')
    a = ast.literal_eval(a)
    print(a['db_name'])
