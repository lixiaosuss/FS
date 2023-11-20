import os
from selenium.webdriver.common.by import By

# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#本地下载路径
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'libs', 'download')

#图片下载路径

IMAGE_PATH = os.path.join(BASE_DIR, 'libs', 'image')

#当前项目目录
PEROJECT_PATH  = os.path.join(BASE_DIR, 'project')

#日志目录
LOG_PATH = os.path.join(BASE_DIR, 'log')


