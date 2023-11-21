from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
import sys
import allure
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from public.base.basics import Base

"""     值校验的各种方法     """




class DomAssert(object):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)



    @allure.step("存在某文字断言")
    def assert_att(self, word):
        """页面是否存在某文字"""
        try:
            Base(self.driver).base_get_img('result')
            att = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"{}")]'.format(word)))).text
            assert word in att, logging.warning("断言失败：页面不存在该标识 | 当前页面关键字: {}".format(att.replace("\n", "|")))
            logging.info("断言成功：页面存在该标识 | 当前页面关键字: {}".format(att.replace("\n", "|")))
        except Exception as e:
            logging.error(e)
            raise

    def assert_exact_att(self, word):
        """精确匹配：页面是否存在某文字"""
        try:
            Base(self.driver).base_get_img('result')
            att = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[normalize-space(text())='{}']".format(word)))).text
            assert word in att, logging.warning("断言失败：页面不存在该标识{} | 关键字:{}".format(att, word))
            logging.info("断言成功：页面存在该标识{} | 关键字:{}".format(att, word))
        except Exception as e:
            logging.error(e)
            raise




    def elements_assert(self,ExpectedResults,element,choice=None,get_attribute='innerText'):
        '''
        locator：元素
        test:断言预期结果在实际结果中
        '''
        ActualResults =  Base(self.driver).find_elemens_ipm_yaml_get_attribute(element,choice,get_attribute)
        try:
            assert  ExpectedResults in ActualResults
            logging.info((f'断言成功，元素：{ActualResults}存在结果为：{ExpectedResults}'))

        except Exception as e:
            logging.info(e)
            raise
