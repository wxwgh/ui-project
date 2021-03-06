# -- coding:utf-8 --
import eel
import os
import shutil
from loadserver import download
from loadserver import analyze
from loadserver import importandexport
from loadserver import userlicence

eel.init('web')

# 图层管理器 导入相关
# 导入数据
@eel.expose
def import_features(info):
    result = importandexport.import_features(info)
    return result
# 获取导入路径
@eel.expose
def get_import_path():
    file_path = importandexport.get_import_path()
    return file_path
#获取导入文件坐标系
@eel.expose
def get_import_coordinate(info):
    coord_name = importandexport.get_import_coordinate(info)
    return coord_name
# 获取导入数据json
@eel.expose
def get_import_features(info):
    result = importandexport.get_import_features(info)
    return result
#判断文件是否存在
@eel.expose
def get_file_exists(info):
    result = importandexport.get_file_exists(info)
    return result

# 图层管理器 导出相关
# 获取导出路径
@eel.expose
def get_export_path():
    file_path = importandexport.get_export_path()
    return file_path
#判断文件是否存在
@eel.expose
def is_samename(path):
    flag = os.path.exists(path)
    return flag
# 导出数据
@eel.expose
def export_features(info):
    result = importandexport.export_features(info)
    return result
# 判断是否是相同基准坐标系
@eel.expose
def is_same_geo(source,target):
    is_same = importandexport.is_same_geo(source,target)
    return is_same

# 坐标转换相关
# 获取导入tif路径
@eel.expose
def get_tif_path():
    file_path = analyze.get_tif_path()
    return file_path
# 投影转换
@eel.expose
def tif_coordinate_trans(info):
    analyze.tif_coordinate_trans(info)

# 用户许可相关
# 获取许可文件路径
@eel.expose
def get_licence_path():
    file_path = userlicence.get_licence_path()
    return file_path



# 导出shp矢量
@eel.expose
def export_shape(info):
    importandexport.export_shape(info)
#使用装饰器 类似flask里面对路由的定义
@eel.expose
def tile_load(info):
    download.down_load(info)
@eel.expose
def vector_load(info):
    download.down_load(info)
@eel.expose
def dem_load(info):
    download.down_load(info)
# 删除文件夹
@eel.expose
def delete_file(path):
    del_list = os.listdir(path)
    for f in del_list:
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    shutil.rmtree(path)
# 打开文件夹
@eel.expose
def open_file(path):
    os.startfile(path)
# 坐标转换
@eel.expose
def coordinate_transition(info):
    analyze.analyze(info)
# 生成许可
@eel.expose
def get_licence(info):
    userlicence.get_licence(info)
# 更新许可
@eel.expose
def update_licence(info):
    result = userlicence.update_licence(info)
    return result


eel.start('index.html',port=18099,size=(1920,1080),chromeFlags=['-kiosk'])