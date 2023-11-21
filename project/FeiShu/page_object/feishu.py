import allure, os


from libs.common.read_element import Element
import time
from ..test_case.conftest import *

object_name = os.path.basename(__file__).split('.')[0]
user = Element(pro_name, object_name)

class UserPage(Base):
    """用户类"""

    def __init__(self, driver, env_name='test'):
        super().__init__(driver)
        self.env_name = env_name

    def input_text(self, locator, txt, *choice):
        """输入文本"""
        ele = self.find_element(locator, *choice)
        ele.clear()
        ele.clear()
        ele.send_keys(txt)
        logging.info("输入文本：{}".format(txt))

    def more(self):
        '''点击更多'''
        self.is_click(user['点击更多'])

    def more_modules(self):
        '''选择模块'''
        self.is_click(user['选择模块'])
        self.switch_window(1)
        time.sleep(2)

    def contacts(self,name,txt):
        '''选择联系人，并发送消息'''
        '''选择联系人'''
        self.is_click(user['选择联系人'],name)
        '''输入文本'''
        self.input_text(user['输入文本'],txt)
        '''点击发送'''
        self.click_enter()

    def fs_assert_exact_att(self,text):
        ass=DomAssert(self.driver)
        ass.assert_exact_att(text)

    def fs_elements_assert(self,text,txt):
        ass=DomAssert(self.driver)
        user = Element(pro_name, object_name)
        ass.elements_assert(text,user['消息发送成功'],txt)



if __name__ == '__main__':
    pass
