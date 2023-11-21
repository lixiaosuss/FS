import pytest, logging
from public.base.assert_ui import *
from project.FeiShu.page_object.feishu import *
import time




@allure.feature("接口数据核对")  # 迭代名称
class TestCheckInterface:
    @allure.story("飞书发送消息成功")  # 用户故事名称
    @allure.title("进入消息页面，发送消息")  # 用例名称
    @allure.description("发送消息的字数不少于10个字符，且发送成功")  # 用例描述
    @allure.severity("normal")  # 用例等级
    @pytest.mark.smoke  # 用例标记
    def test_001_001(self,drivers):
        times = time.strftime('%Y-%m-%d%H:%M:%S')
        text = '飞书发送福利给大家了{}'.format(times)
        user=UserPage(drivers)
        user.more()
        user.more_modules()
        user.contacts('飞书新用户体验群',text)
        user.fs_assert_exact_att(text)
        user.fs_elements_assert(text,text)






