import os
from selenium.webdriver.common.by import By

# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 本地下载路径
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'libs', 'download')

# 图片下载路径
IMAGE_PATH = os.path.join(BASE_DIR, 'libs', 'image')

# 当前项目目录
PEROJECT_PATH = os.path.join(BASE_DIR, 'project')

# 日志目录
LOG_PATH = os.path.join(BASE_DIR, 'log')



# excel目录
TESTCASE_PATH = os.path.join(PEROJECT_PATH, 'POP', 'excel_drive', 'TestCase.xlsx')

# 公共路径
PUBLIC_PATH = os.path.join(BASE_DIR, 'public')

# 公共页面元素目录
PUBLIC_ELEMENT_PATH = os.path.join(PUBLIC_PATH, 'libs', 'unified_login', 'page_element')

# 公共数据源
PUBLIC_DATA_PATH = os.path.join(PUBLIC_PATH, 'data', 'datasource')


# 元素定位的类型
LOCATE_MODE = {
    'id': By.ID,
    'name': By.NAME,
    'css': By.CSS_SELECTOR,
    'class': By.CLASS_NAME,
    'text': By.LINK_TEXT,
    'partial-link': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'xpath': By.XPATH,
}

if __name__ == '__main__':
    pass