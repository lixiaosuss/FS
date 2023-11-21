import logging
import os
import sys

import yaml
import re
from libs.common.time_ui import timestamp
from libs.config.conf import PEROJECT_PATH, LOCATE_MODE



def get_FolderName(filepath):
    pro_list = []
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s' % (allDir))
        pro_list.append(child)
    return pro_list


def inspect_element():
    """审查所有的元素是否正确"""
    print("【开始】请稍候，元素定位库文件自检程序开始！")
    start_time = timestamp()
    pro_list = get_FolderName(PEROJECT_PATH)

    error_list = []
    for pro in pro_list:
        ELEMENT_PATH = os.path.join(PEROJECT_PATH, pro, 'page_element')
        for i in os.listdir(ELEMENT_PATH):
            _path = os.path.join(ELEMENT_PATH, i)
            if os.path.isfile(_path):
                with open(_path, encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    try:
                        if data is None:
                            error_list.append('【项目】%s【模块】%s中元素格式不符！' % (pro, i))

                        if isinstance(data, dict) is False:
                            error_list.append(
                                '【项目】%s【模块】%s请检查元素名和表达式固定格式【元素定位名: 定位方式==定位路径】！' % (
                                pro, i))

                        for k, v in data.items():

                            if v is None:
                                error_list.append(
                                    '【项目】%s【模块】%s【元素】%s【定位表达式】%s定位方式和值未填写！' % (pro, i, k, v))

                            if '==' not in str(v):
                                error_list.append(
                                    '【项目】%s【模块】%s【元素】%s【定位表达式】%s标签和路径需用==间隔！' % (pro, i, k, v))

                            pattern, value = v.split('==')

                            if pattern not in LOCATE_MODE:
                                error_list.append('【项目】%s【模块】%s【元素】%s【定位表达式】%s类型系统暂不支持' % (pro, i, k, v))

                            if pattern in ('id', 'name', 'css', 'class', 'text', 'partial-link', 'tag'):
                                continue

                            if pattern == 'xpath':

                                if '“' in value or '‘' in value:
                                    error_list.append(
                                        '【项目】%s【模块】%s【元素】%s【定位表达式】%s注意不要用中文符号的引号！' % (
                                        pro, i, k, v))

                                if '/' not in value:
                                    error_list.append(
                                        '【项目】%s【模块】%s【元素】%s【定位表达式】%s该类型不为路径！' % (pro, i, k, v))



                            # if pattern == 'css':
                            #     if '/' not in value:
                            #         print('【提示】【%s】项目【%s】模块【%s】元素css类型与值不配' % (pro, i, k))
                            #         error_list += 1

                            # if pattern == 'id':
                            #     if '/' not in value:
                            #         print('【提示】【%s】项目【%s】模块【%s】元素css类型与值不配' % (pro, i, k))
                            #         error_list += 1
                    except:
                        continue

    end_time = timestamp()
    print("【结束】恭喜您，元素库文件自检程序完成！用时%.3f秒！" % (end_time - start_time))
    if len(error_list) != 0:
        raise AttributeError('\n%s\n【提示】请尽快检查并修改自己的用例，如有异议，请尽快联系我们，谢谢！' % error_list)

def inspect_description():
    """审查所有的描述是否正确"""
    print("【开始】请稍候，描述文件自检程序开始！")
    start_time = timestamp()
    pro_list = get_FolderName(PEROJECT_PATH)

    error_list = []
    for pro in pro_list:
        # 获取项目下所有用例目录
        dirlist = []
        DIR_PATH = os.path.join(PEROJECT_PATH, pro, 'test_case')
        for i in os.listdir(DIR_PATH):
            _path = os.path.join(DIR_PATH, i)
            if 'conftest.py' not in _path and '__pycache__' not in _path and 'failures' not in _path and 'allure-results' not in _path:
                dirlist.append(_path)
        for dir in dirlist:
            for filename in os.listdir(dir):
                if 'failures' not in filename and 'allure-results' not in filename:
                    file_path = os.path.join(dir, filename)
                    # fixtlist = []

                if os.path.isfile(file_path):
                    with open(file_path, encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        readIn = [i.rstrip() for i in lines]

                        # 判断是否是空文件
                        count = 0
                        for j in readIn:
                            if "class" in j:
                                count = count + 1
                        if count == 0:
                            error_list.append('项目【%s】的文件【%s】为空文件，无class代码！' % (pro, filename))
                            # break
                            continue

                        fixtlist = []
                        for i in range(len(readIn)):
                            # 判断class类是否有feature
                            if 'class Test' in readIn[i]:
                                if '@allure.feature' not in readIn[i-1]:
                                    error_list.append('项目【%s】的文件【%s】中class【%s】无feature，不符合规则,请修改！' % (pro, filename, readIn[i]))
                                    break
                                    # continue
                            # 获取feature的列表
                            if '@allure.feature' in readIn[i] and readIn[i].startswith("#") is False:
                                repFeature = re.findall('(?<=@allure.feature\().*?(?=\))', readIn[i])
                                fixtlist.append(repFeature[0])

                        if len(fixtlist) > 1:
                            # 判断feature名称是否一致
                            lll = set(fixtlist)
                            try:
                                assert len(lll) == 1
                            except Exception as e:
                                error_list.append('项目【%s】的文件【%s】中feature的描述不一致，不符合规则,请修改！' % (pro, filename))


                        # 验证story
                        resp = [i for i in readIn if "class Test" in i]
                        # 获取每个class的下标列表
                        nnn = []
                        for inde, value in enumerate(readIn):
                            for i in range(len(resp)):
                                if value == resp[i]:
                                    nnn.append(inde)

                        # 每个“feature”之间的数据生成新的列表
                        lll = []
                        for i in range(len(nnn)):
                            if i < len(nnn) - 1:
                                ll = readIn[nnn[i]:nnn[i + 1]]
                            else:
                                ll = readIn[nnn[i]:]
                            lll.append(ll)

                        for news in lll:
                            res1 = [li for li in news if '@allure.story' in li and li.strip().startswith("#") is False]

                            storytlist = []
                            if len(res1) > 1:
                                for linee in res1:
                                    repFeature = re.findall('(?<=@allure.story\().*?(?=\))', linee)
                                    storytlist.append(repFeature[0])
                                llll = set(storytlist)
                                try:
                                    assert len(llll) == 1
                                except Exception as e:
                                        error_list.append('项目【%s】的文件【%s】中feature【%s】的story描述不一致，不符合规则,请修改！' % (
                                        pro, filename, news[0]))

    end_time = timestamp()
    print("【结束】恭喜您，test_case文件自检程序完成！用时%.3f秒！" % (end_time - start_time))
    if len(error_list) != 0:
        raise AttributeError('\n%s\n【提示】请尽快检查并修改自己的用例，如有异议，请尽快联系我们，谢谢！' % error_list)



if __name__ == '__main__':
    # print(get_FolderName(PEROJECT_PATH))
    # inspect_element()
    #inspect_description('DCR_GLOBAL')
    inspect_description()
