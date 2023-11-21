import base64
import datetime
import time
import openpyxl
import xlrd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from libs.config.conf import LOCATE_MODE, DOWNLOAD_PATH, IMAGE_PATH, BASE_DIR
from libs.common.time_ui import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import logging
import allure
import datetime
import ddddocr
import random
import cv2 as cv
from selenium.webdriver.chrome.options import Options


import warnings
from PIL import Image

"""git
selenium基类
本文件存放了selenium基类的封装方法
"""


class Base(object):
    """selenium基类"""

    def __init__(self, driver):
        # self.driver = webdriver.Chrome()
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(LOCATE_MODE[name], value)


    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            logging.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    def mouse_move(self, slide, tracks):
        '''鼠标滑动'''

        # 鼠标点击滑块并按照不放
        ActionChains(self.driver).click_and_hold(slide).perform()
        # 按照轨迹进行滑动，
        for track in tracks:
            ActionChains(self.driver).move_by_offset(track, 0).perform()
        time.sleep(0.2)
        ActionChains(self.driver).release().perform()
        time.sleep(2)
        return




    def is_click(self, locator, *args, **kwargs):
        """点击元素"""
        if args and args is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            for i in range(len(args)):
                Npath[1] = Npath[1].replace('variable', str(args[i]), 1)
            sleep(2)
            self.find_element(Npath).click()
            logging.info("选择点击：{}".format(Npath))

        elif kwargs and kwargs is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            Npath[1] = Npath[1].replace('variable', str(kwargs['choice']))
            logging.info(Npath)
            sleep(2)
            self.find_element(Npath).click()
            logging.info("选择点击：{}".format(Npath))

        else:
            self.find_element(locator).click()
            logging.info("点击元素：{}".format(locator))
            sleep(0.5)

    def find_element(self, locator, *args, **kwargs):
        """寻找单个元素"""
        if args and args is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            for i in range(len(args)):
                Npath[1] = Npath[1].replace('variable', str(args[i]), 1)
            logging.info("查找元素：{}".format(Npath))
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_element_located(args)), Npath)

        elif kwargs and kwargs is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            Npath[1] = Npath[1].replace('variable', str(kwargs['choice']))
            logging.info("查找元素：{}".format(Npath))
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_element_located(args)), Npath)
        else:
            logging.info("查找元素：{}".format(locator))
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_element_located(args)), locator)



    def input_text(self, locator, txt, choice=None):
        """输入文本"""
        if choice is None:
            sleep(0.5)
            ele = self.find_element(locator)
            ele.clear()
            ele.clear()
            ele.send_keys(txt)
            logging.info("输入文本：{}".format(txt))
        else:
            """输入(输入前先清空)"""
            sleep(0.5)
            ele = self.find_element(locator, choice)
            ele.clear()
            ele.clear()
            ele.send_keys(txt)
            logging.info("输入文本：{}".format(txt))


    def base_get_img(self, name='err'):
        """截图方法"""
        imgname = IMAGE_PATH + '\\' + "{}.png".format(name)
        # 保存截图 error日志
        # logging.error("正在截图...")
        self.driver.get_screenshot_as_file(imgname)
        # 写入报告
        self.__base_write_img(imgname)
    def __base_write_img(self, imgname):
        """读图片"""
        # logging.error("日志正在附加截图...")
        with open(imgname, 'rb') as f:
            # 附加报告
            allure.attach(f.read(), "断言截图:", allure.attachment_type.PNG)
        # logging.error("日志附加截图成功")

    def frame_back(self):
        """返回frame"""
        self.driver.switch_to.parent_frame()  # 返回上一层

    def element_text(self, locator, *args, **kwargs):
        """获取元素的文本"""
        if args and args is not None:
            ele = self.find_element(locator, *args)
            _text = ele.text.replace("\n", "|")
            logging.info("获取文本：{}".format(_text))
            return _text
        elif kwargs and kwargs is not None:
            ele = self.find_element(locator, *kwargs)
            _text = ele.text.replace("\n", "|")
            logging.info("获取文本：{}".format(_text))
            return _text
        else:
            _text = self.find_element(locator).text.replace("\n", "|")
            logging.info("获取文本：{}".format(_text))
            return _text



    def switch_window(self, n):
        """切换窗口"""
        self.driver.switch_to.window(self.driver.window_handles[n])
        logging.info("开始切换新打开的窗口")

    def close_switch(self, n):
        """关闭窗口"""
        self.driver.switch_to.window(self.driver.window_handles[n])  # 切换到新页签
        self.driver.close()  # 关闭新页签
        self.driver.switch_to.window(self.driver.window_handles[0])  # 然后切换回原始页签
        logging.info("关闭新打开的窗口")

    def find_elements(self, locator, *args, **kwargs):
        """寻找多个相同的元素"""
        if args and args is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            for i in range(len(args)):
                Npath[1] = Npath[1].replace('variable', str(args[i]), 1)
            logging.info("查找元素：{}".format(Npath))
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), Npath)
        elif kwargs and kwargs is not None:
            Npath = []
            Npath.append(locator[0])
            Npath.append(locator[1])
            Npath[1] = Npath[1].replace('variable', str(kwargs['choice']))
            logging.info("查找元素：{}".format(Npath))
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), Npath)
        else:
            return Base.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), locator)

    def elements_inner_text(self, locator, *args):
        """获取元素的文本"""
        text_list = []
        eles = self.find_elements(locator, *args)
        for i in eles:
            _text = i.get_attribute('innerText').replace("\n", "|")
            text_list.append(_text)
        logging.info("获取文本：{}".format(text_list))
        return text_list

    def find_elemens_ipm_yaml_get_attribute(self, element, choice=None, get_attribute="innerText"):
        ele = self.find_elements(element, choice=choice)
        elelist = []
        for i in ele:
            res = i.get_attribute(get_attribute)
            elelist.append(res)
        return elelist

    def click_enter(self):
        '''回车'''
        # 创建Action对象
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()




if __name__ == "__main__":
    pass