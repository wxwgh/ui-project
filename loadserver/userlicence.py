# -- coding:utf-8 --
import iobjectspy
import os
import eel

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
    file.write(info["time"])
    file.close()
# 更新许可
def update_licence(info):
    file_path = info["url"]
    # 打开文件
    file = open(file_path, mode="r", encoding="utf-8")
    content = file.readline()
    return content