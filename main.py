import eel
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from loadserver import download
from loadserver import analyze
from loadserver import importandexport
from loadserver import userlicence


eel.init('web')
# 获取shp中矢量数据
@eel.expose
def get_features(info):
    datas = importandexport.get_features(info)
    return datas
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
#判断目录是否存在
@eel.expose
def is_samename(path):
    flag = os.path.exists(path)
    return flag
#获取存储路径
@eel.expose
def get_save_path():
    root= tk.Tk()
    root.withdraw()
    # 将窗口显示在所有其他窗口之上
    root.attributes("-topmost", True)
    # 获取文件夹路径
    Folderpath = filedialog.askdirectory()
    root.destroy()
    return Folderpath
#获取栅格文件路径
@eel.expose
def get_grid_path():
    root= tk.Tk()
    root.withdraw()
    # 获取文件夹路径
    file_path = filedialog.askopenfilename(filetypes=[('grid','*.tif;*.img')])
    return file_path
# 获取许可文件路径
@eel.expose
def get_licence_path():
    root= tk.Tk()
    root.withdraw()
    # 获取文件夹路径
    file_path = filedialog.askopenfilename(filetypes=[('licence','*.sm1x')])
    return file_path
# 获取shp格式文件路径
@eel.expose
def get_shape_path():
    root= tk.Tk()
    root.withdraw()
    # 将窗口显示在所有其他窗口之上
    root.attributes("-topmost", True)
    # 获取文件夹路径
    file_path = filedialog.askopenfilename(filetypes=[('shp', '*.shp')])
    root.destroy()
    return file_path
# 提取等值
@eel.expose
def get_contour_line(info):
    analyze.get_contour_line(info)
# 提取等面
@eel.expose
def get_contour_polygon(info):
    analyze.get_contour_polygon(info)
# 坡度分析
@eel.expose
def get_slope(info):
    analyze.get_slope(info)
# 坡向分析
@eel.expose
def get_aspect(info):
    analyze.get_aspect(info)
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
    content = userlicence.update_licence(info)
    return content


eel.start('index.html',port=18099,size=(1920,1080),chromeFlags=['-kiosk'])