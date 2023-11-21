import pytest, logging
from public.data.unified_login.unified import *
from public.base.assert_ui import *
from public.libs.unified_login.login import Login
from libs.common.read_config import *

pro_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logging.info(f'the proname is {pro_name}')

@pytest.fixture(scope='session',autouse=True)
def __init__(drivers, env_name):
    """初始化"""
    global pro_env
    pro_env = env_name
    logging.info("【{}】项目【{}】环境- UI自动化开始执行".format(pro_name, pro_env))
    ini = ReadConfig(pro_name, pro_env)
    logging.info("前置条件：开始登录飞书")
    user = Login(drivers)
    user.feishu_login(drivers, ini.url,  account[0]['usernum'], account[0]['passwd'])
    user = DomAssert(drivers)
    user.assert_exact_att(account[0]['username'])
    logging.info("前置条件：登录飞书成功")

