
from public.base.basics import Base, sleep
from libs.common.read_public_element import Element

login = Element('login')




class LoginPage(Base):
    def fs_click_close(self):
        """进入飞书首页_关闭弹窗"""
        sleep(1)
        self.is_click(login['进入飞书首页_关闭弹窗'])

    def fs_click_HomeLogin(self):
        """进入飞书首页_点击登录"""
        sleep(1)
        self.is_click(login['进入飞书首页_点击登录'])

    def fs_click_account(self,):
        """输入账号"""
        sleep(2)
        self.is_click(login['选择账号登录'])

    def fs_input_account(self, content):
        """输入账号"""
        self.input_text(login['输入账号'], txt=content)

    def fs_input_agreement(self):
        """勾选协议，点击下一步"""
        self.is_click(login['勾选协议'])
        self.is_click(login['点击下一步'])


    def fs_input_passwd(self, content):
        """输入密码"""
        self.input_text(login['输入密码'], txt=content)

    def fs_click_login(self):
        """点击登录"""
        self.is_click(login['点击登录'])
        sleep(2)

if __name__ == '__main__':
    pass
