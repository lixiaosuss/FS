import sys, pytest, os, time
import logging, allure
from py._xmlgen import html
from selenium import webdriver
from time import sleep
from libs.common.inspect_ymal import inspect_element, inspect_description
from libs.config.conf import DOWNLOAD_PATH, LOG_PATH
from selenium.webdriver.remote.file_detector import LocalFileDetector

driver = None

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default='test', help='环境操作')

    # -->默认请用DEV环境做代码调试<--
    parser.addoption("--remoteurl", action="store", default='http://10.250.101.58:4444', help='远程DEV环境（linux服务器）')
    # parser.addoption("--remoteurl", action="store", default='http://10.250.101.49:4444', help='远程DEV环境（windows服务器）')

    # parser.addoption("--remoteurl", action="store", default='http://10.250.113.16:4444', help='远程UAT环境（linux服务器）')
    # parser.addoption("--remoteurl", action="store", default='http://10.250.113.15:4444', help='远程UAT环境（windows服务器）')


@pytest.fixture(scope="session", autouse=True)
def env_name(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session", autouse=True)
def remote_url(request):
    return request.config.getoption("--remoteurl")

@pytest.fixture(scope='session', autouse=True)
def drivers(request, remote_url, remote_ui=False):
    global driver
    if driver is None:
        if 'linux' in sys.platform:
            option = webdriver.ChromeOptions()
            option.file_detector = LocalFileDetector()
            # option.add_argument('--headless')  # 浏览器不提供可视化页面（无头模式）. linux下如果系统不支持可视化不加这条会启动失败
            # option.add_argument('--window -size=1280x1024')  # 设置浏览器分辨率（窗口大小）
            # option.add_argument('--start -maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
            # option.add_argument('--disable -infobars')  # 禁用浏览器正在被自动化程序控制的提示
            # option.add_argument('--incognito')  # 隐身模式（无痕模式）
            # option.add_argument('--hide -scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # option.add_argument('--disable -javascript')  # 禁用javascript
            # option.add_argument('--blink -settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # option.add_argument('disable -gpu')  # 禁用GPU加速
            # option.add_argument('proxy-server={}'.format(self.proxy_server))  # 配置代理
            # option.add_argument('no-default-browser-check') # 不做浏览器默认检查
            # option.add_argument("–disable-popup-blocking")  # 允许弹窗
            # option.add_argument("–disable-extensions")  # 禁用扩展
            # option.add_argument("–ignore-certificate-errors")  # 忽略不信任证书
            # option.add_argument("–no-first-run")  # 初始化时为空白页面
            # option.add_argument('–disable -notifications')  # 禁用通知警告
            # option.add_argument('–enable -automation')  # 通知(通知用户其浏览器正由自动化测试控制)
            # option.add_argument('–disable -xss -auditor')  # 禁止xss防护
            # option.add_argument('–disable -web -security')  # 关闭安全策略
            # option.add_argument('–allow -running -insecure  content')  # 允许运行不安全的内容
            # option.add_argument('–disable - webgl')  # 禁用webgl
            # option.add_argument('–homedir = {}')  # 指定主目录存放位置
            # option.add_argument('disable -cache')  # 禁用缓存
            # option.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
            # option.add_argument('–disable-software-rasterizer')
            # option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 调用原来的浏览器，不用再次登录即可重启

            prefs = {"": ""}
            prefs["intl.accept_languages"] = 'zh-CN,zh'
            prefs["credentials_enable_service"] = False
            prefs["profile.password_manager_enabled"] = False
            prefs["download.prompt_for_download"] = False
            option.add_experimental_option("prefs", prefs)  # 屏蔽'保存密码'提示框

            option.add_argument('–lang=zh-CN')  # 设置语言
            option.add_argument('--no-sandbox')  # 以最高权限运行
            option.add_argument('--start-maximized')  # 最大化运行（全屏窗口）设置元素定位比较准确
            option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            # option.set_capability("browserVersion", "104.0")
            option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            driver = webdriver.Remote(remote_url, options=option)
            inspect_element() # page_element YMAL文件自检
            inspect_description() # test_case目录下子文件夹自检
        else:
            if remote_ui:
                '''win系统下VNC界面模式'''
                option = webdriver.ChromeOptions()
                prefs = {"": ""}
                prefs["intl.accept_languages"] = 'zh-CN,zh'
                prefs["credentials_enable_service"] = False
                prefs["profile.password_manager_enabled"] = False
                option.add_experimental_option("prefs", prefs)  # 屏蔽'保存密码'提示框

                option.add_argument('–lang=zh-CN')  # 设置语言
                option.add_argument('--no-sandbox')  # 以最高权限运行
                option.add_argument('--start-maximized')  # 最大化运行（全屏窗口）设置元素定位比较准确
                option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug

                option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
                driver = webdriver.Remote(remote_url, options=option)
                inspect_element() # page_element YMAL文件自检
                inspect_description()  # test_case目录下子文件夹自检
            else:
                option = webdriver.ChromeOptions()
                prefs = {"": ""}
                # prefs["credentials_enable_service"] = False
                # prefs["profile.password_manager_enabled"] = False
                # prefs["download.prompt_for_download"] = False  # 关闭下载自动打开选项
                # prefs["download.default_directory"] = DOWNLOAD_PATH
                # option.add_experimental_option("prefs", prefs)  # 屏蔽'保存密码'提示框
                # 防止打印一些无用的日志
                option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
                driver = webdriver.Chrome(options=option)
                driver.maximize_window()
                # inspect_element() # page_element YMAL文件自检
                #inspect_description()  # test_case目录下子文件夹自检
    def fn():
        sleep(5)
        driver.quit()

    # 终结函数
    request.addfinalizer(fn)
    return driver


# logname = time.strftime('%Y_%m_%d_%H')
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',
#                     datefmt='[%Y-%m-%d %H:%M:%S]',
#                     filename='{}/{}.log'.format(LOG_PATH, logname),
#                     encoding='utf-8',
#                     filemode='a')


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中,基于pytest-html
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def _capture_screenshot():
    '''
    截图保存为base64
    :return:
    '''
    return driver.get_screenshot_as_base64()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
获取⽤例执⾏结果的钩⼦函数
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode)as f:
            if "tmpir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
                f.write(report.nodeid + extra + "\n")
            with allure.step('添加失败截图'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

