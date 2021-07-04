# -- coding:utf-8 --
import os
import socket
import uuid
import base64
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

# 获取许可地址
def get_licence_path():
    app=QApplication(sys.argv)
    # 桌面经典窗口类
    rans=QWidget()
    rans.setStyleSheet("background-color:black;")
    rans.setWindowOpacity(0.1)
    # 删除title栏
    rans.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
    # 获取桌面
    desktop=QApplication.desktop()
    # 设置宽高
    rans.setFixedSize(desktop.width(),desktop.height())
    rans.show()
    path=QFileDialog.getOpenFileName(rans,"请选择要导入的文件","D:/","LICENCE (*.sm1x)")
    file_path=path[0]
    return file_path
# 生成许可
def get_licence(info):
    # 存储路径
    save_path = os.path.join(info["save_path"], info["task_name"])
    # 创建目录
    os.makedirs(save_path)
    # 导出文件路径
    temp_str = info["task_name"] + ".sm1x"
    file_path = os.path.join(save_path,temp_str)
    # 创建并打开文件
    file = open(file_path, mode="w", encoding="utf-8")
    file.write(info["time"]+"\n")
    file.write(info["url"])
    file.close()
# 更新许可
def update_licence(info):
    file_path = info["url"]
    # 打开文件
    file = open(file_path, mode="r", encoding="utf-8")
    content = file.readlines()
    time = ""
    url = ""
    for i in range(len(content)):
        if i == 0:
            time = base64.b64decode(content[i].strip()).decode()
        else:
            url = base64.b64decode(content[i].strip()).decode()
    print(url)
    file.close()
    node = uuid.getnode()
    macHex = uuid.UUID(int=node).hex[-12:]
    mac = []
    str_mac = ""
    for i in range(len(macHex))[::2]:
        mac.append(macHex[i:i + 2])
    str_mac = '-'.join(mac).upper()
    print(str_mac)
    result={}
    if url == str_mac:
        result["url_correct"] = True
        result["time"] = time
    else:
        result["url_correct"] = False
        result["time"] = time
    return result