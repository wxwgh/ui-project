#!/usr/bin/env python3
###############################################################################
# Purpose:  从百度API网站 http://lbsyun.baidu.com/index.php?title=webapi抓取数据
# Author:   venen,chenxw
# Input:   抓取'公司名称','地址','电话','纬度','经度'相关数据
# Output:  满足条件的数据保存Excel
# Excute： python3 getBaiduXingzhengquhuaApi.py 钢铁厂 北京
#          支持对全国，分省，分地市的检索，修改by chenxw
#          表示抓取北京地区的钢铁厂所有'公司名称','地址','电话','纬度','经度'相关数据，数据保存在当前目录xingzhengquhua.xls文件中
###############################################################################
import requests
import json
import math
import sys
import os
import time
import platform

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
}
# 生成exel的表头
excel_col = ['名称', '地址', '电话', '纬度', '经度']
# 结果数组
all_result = []
# 查询区域名称
query_region = ""
# 查询关键词
query_word = "村"
# 生成的excel文件路径
excel_path = ""


# 测试用例说明
# 煤炭厂 四川  第一页是poi_type,第二页是city_type
# 化工厂 四川  第一页是city_type
# 煤炭厂 成都  第一页是poi_type
# 煤炭厂 嘉峪关市 第一页是city_type，第二页是poi_type---最终查询结果为空
# 煤炭厂 全国
# 代理
proxies={"http":None,"https":None}
# 触发调用百度接口，获取结果对象
def toogle_query_baidu_poi(query_word, region_name, page_num):
    url = 'http://api.map.baidu.com/place/v2/search?query=%s&region=%s&output=json&ak=3El1hQec2kMxiHpFbACZ1p6PpFg6lR4A&page_size=20&page_num=%s&coord_type=wgs84ll' % (
        query_word, region_name, page_num)
    res = requests.get(url, headers=headers,proxies=proxies)
    res.encoding = 'utf-8-sig'
    data = json.loads(res.text)
    return data


# 触发调用百度接口，获取结果类型
def get_query_baidu_data_type(query_word, region_name, page_num):
    url = 'http://api.map.baidu.com/place/v2/search?query=%s&city_limit=true&tag=村庄&region=%s&output=json&ak=3El1hQec2kMxiHpFbACZ1p6PpFg6lR4A&page_size=20&page_num=%s' % (
        query_word, region_name, page_num)
    res = requests.get(url, headers=headers,proxies=proxies)
    res.encoding = 'utf-8-sig'
    data = json.loads(res.text)
    return data['result_type']


# 得到city_type下面的name,有可能是省，也可能是地市
def get_result_name_list_of_city_type(query_word, region_name, page_num):
    result_name_list = []
    url = 'http://api.map.baidu.com/place/v2/search?&scope=2&extensions_adcode=true&query=%s&region=%s&output=json&ak=3El1hQec2kMxiHpFbACZ1p6PpFg6lR4A&page_size=20&page_num=%s' % (
        query_word, region_name, page_num)
    res = requests.get(url, headers=headers,proxies=proxies)
    res.encoding = 'utf-8-sig'
    data = json.loads(res.text)
    print(data)
    for t in range(0, len(data['results'])):
        result_region_name = data['results'][t].get('name')
        result_name_list.append(result_region_name)
    return result_name_list


# 获取百度查询需要的地市名称，根据百度接口返回结果调整
# 不支持任意值的区域名称
def get_area_region_of_baidu_need(region_name):
    need_region_list = []
    if region_name == "全国":
        need_region_list = get_all_city_of_country()
    else:
        if get_query_baidu_data_type(query_word, region_name, 0) == "poi_type":
            # 针对只有一页的poi_type
            if get_query_baidu_data_type(query_word, region_name, 1) is None:
                need_region_list.append(region_name)
            else:
                # 针对两页多的poi_type
                if get_query_baidu_data_type(query_word, region_name, 1) == "poi_type":
                    need_region_list.append(region_name)
                # 第一页是poi_type,第二页是city_type, 如区域为四川，关键词是煤炭厂
                elif get_query_baidu_data_type(query_word, region_name, 1) == "city_type":
                    result_name_list = get_result_name_list_of_city_type(query_word, region_name, 1)
                    for result_name in result_name_list:
                        need_region_list.append(result_name)
        elif get_query_baidu_data_type(query_word, region_name, 0) == "city_type":
            # 煤炭厂 嘉峪关市
            if get_query_baidu_data_type(query_word, region_name, 1) == "poi_type":
                pass
            else:
                result_name_list2 = get_result_name_list_of_city_type(query_word, region_name, 1)
                for result_name2 in result_name_list2:
                    need_region_list.append(result_name2)
    return need_region_list


# 从百度地图官网上下载的百度地图city_code文件中获取全国的城市列表
# 后期百度地图的city_code更新后，同步更新这个txt文件接口
# 下载地址：http://lbsyun.baidu.com/index.php?title=open/%E5%BC%80%E5%8F%91%E8%B5%84%E6%BA%90
def get_all_city_of_country():
    city_list = []
    if (platform.system() == 'Windows'):
        baidu_city_code_file_path = "D:\qcn_python\qcn\百度数据抓取\BaiduMap_cityCode.txt"
    else:
        baidu_city_code_file_path = "/app/qcn/python/BaiduMap_cityCode.txt"
    with open(baidu_city_code_file_path, 'r', encoding='UTF-8') as file:
        city_code_file = file.read()
        current_row = 0
        line_list = city_code_file.split("\n")
        for line in line_list:
            current_row += 1
            if current_row == 1:
                continue
            else:
                city_list.append(line.split(",")[1])
    return city_list


# 调用百度地图接口获取结果数据
def get_poi_data_from_baidu(query_word, region_name):
    data = toogle_query_baidu_poi(query_word, region_name, 0)
    # 即使是正常地市名，也会查询出city_code，如煤炭厂，嘉峪关市，第一页是city_code,第二页是poi_type，但没有数值
    # 上述情况有可能是嘉峪关市没有煤炭厂的原因
    if data['result_type'] == "poi_type":
        total = data['total']
        pageSize = math.ceil(total / 20)
        if (pageSize):
            for i in range(0, pageSize):
                print("采集第{}/{}页数据".format(str(i + 1), str(pageSize)))
                data = toogle_query_baidu_poi(query_word, region_name, i)
                for t in range(0, len(data['results'])):
                    obj = {}
                    obj['name'] = data['results'][t].get('name')
                    address = data['results'][t].get('province') + ',' + data['results'][t].get('city') + ',' + \
                              data['results'][t].get('area') + ',' + data['results'][t].get('address')
                    obj['address'] = address
                    obj['tel'] = data['results'][t].get('telephone')
                    obj['lng'] = data['results'][t].get('location').get('lng')
                    obj['lat'] = data['results'][t].get('location').get('lat')
                    all_result.append(obj)
    print(all_result)
    print(len(all_result))



# 得到文件路径的斜杆写法
def get_dash_in_system():
    if (platform.system() == 'Windows'):
        return "\\"
    else:
        return "/"


# 获取日志文件路径
def get_log_file_path():
    (file_pre_path, temp_filename) = os.path.split(excel_path)
    (shot_name, file_ext) = os.path.splitext(temp_filename)
    log_file_path = file_pre_path + get_dash_in_system() + shot_name + ".log"
    return log_file_path


# 生成日志文件
def make_log_file(log_info):
    log_file_path = get_log_file_path()
    if os.path.isfile(log_file_path):
        os.remove(log_file_path)
    if not os.path.isfile(log_file_path):
        fd = open(log_file_path, mode="w", encoding="utf-8")
        fd.write(log_info)
        fd.close()


# 删除日志文件
def del_log_file():
    log_file_path = get_log_file_path()
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

def test():
    need_region_list = get_result_name_list_of_city_type("村庄", "菏泽市",0)
    print(need_region_list)
    # get_poi_data_from_baidu("村","沙土镇")
    # toogle_query_baidu_poi("村","山东",1)
test()
# get_query_baidu_data_type("村","山东",1)
# get_poi_data_from_baidu("村庄","曹县")
