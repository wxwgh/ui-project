# -- coding:utf-8 --
import os
import eel
import json
import math
import sys
proj_str = os.path.dirname(sys.argv[0])+'/proj'
os.environ['PROJ_LIB'] = proj_str
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np

import csv
#线程池
from concurrent.futures import ThreadPoolExecutor

#创建线程池
thread_pool = ThreadPoolExecutor(10)
# 判断文件是否存在
def get_file_exists(path):
    result = os.path.isfile(path)
    return result
# 获取导入文件路径
def get_import_path():
    app = QApplication(sys.argv)
    # 桌面经典窗口类
    rans = QWidget()
    rans.setStyleSheet("background-color:black;")
    rans.setWindowOpacity(0.1)
    # 删除title栏
    rans.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
    # 获取桌面
    desktop = QApplication.desktop()
    # 设置宽高
    rans.setFixedSize(desktop.width(), desktop.height())
    rans.show()
    path = QFileDialog.getOpenFileName(rans, "请选择要导入的文件", "D:/", "Shape File (*.shp);;KML (*.kml);;CSV (*.csv)")
    file_path = path[0]
    return file_path
# 获取导入数据坐标系
def get_import_coordinate(info):
    file_path = info["file_path"]
    file_format = info["file_format"]
    coord_name=""
    if file_format == "shp":
        # 注册所有数据类型驱动
        ogr.RegisterAll()
        # 获取驱动
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # 0为以只读方式打开矢量文件 返回数据源
        data_source = driver.Open(file_path, 0)
        # 获取第一张图层
        layer = data_source.GetLayer(0)
        # 获取数据源坐标系
        source_coordinate = layer.GetSpatialRef()
        temp_coord_name = source_coordinate.GetName()
        coord_name = str(temp_coord_name)
    else:
        coord_name="WGS 84"
    print(coord_name)
    return coord_name

# 解决csv读取大小限制
maxInt = sys.maxsize
decrement = True
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
# 判断是否是相同基准坐标系
def is_same_geo(source,target):
    print(target)
    print(source)
    source_coordinate = osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(source))
    target_coordinate = osr.SpatialReference()
    target_coordinate.ImportFromEPSG(int(target))
    # 判断是否是相同的椭球基准面
    is_same = source_coordinate.IsSameGeogCS(target_coordinate)
    print(is_same)
    return is_same
# 获取坐标系转换对象
def get_coordinate_trans(source,target,x,y,seven):
    # 设置源数据坐标系
    source_coordinate = osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(source))
    # 设置目标坐标系
    target_coordinate = osr.SpatialReference()
    target_coordinate.ImportFromEPSG(int(target))
    result = ""
    # 判断是否是相同坐标系 即 不需要转换
    if source == target:
        result = [x,y]
    else:
        # 判断是否是相同的椭球基准面
        is_same = source_coordinate.IsSameGeogCS(target_coordinate)
        # 如果是则直接进行转换
        if is_same == 1:
            # 创建坐标转换对象
            transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
            temp_coord = transform.TransformPoint(y,x)
            result = [temp_coord[0],temp_coord[1]]
            print("相同基准")
        # 不同的椭球体基准面, 要设置七参数或者三参数
        else:
            # 判断源坐标系是否是投影坐标系 如果是需要先转成地理坐标系
            if source_coordinate.IsProjected():
                temp_coordinate = source_coordinate.CloneGeogCS()
                # 创建坐标转换对象
                transform = osr.CoordinateTransformation(source_coordinate, temp_coordinate)
                # 投影坐标转地理坐标系
                temp_coord = transform.TransformPoint(x,y)
                print(temp_coord)
                # 将地理坐标系 转为 空间直角坐标系
                source_zhijiao = geo_to_zhijiao(temp_coordinate,temp_coord[1],temp_coord[0],0)
                # 七参数运算,将源直角坐标系转为目标直角坐标系
                target_zhijiao = qicanshu(source_zhijiao,seven)
                # 判断目标坐标系是否是投影坐标系
                if target_coordinate.IsProjected():
                    # 获取同基准地理坐标系
                    target_temp_coordinate = source_coordinate.CloneGeogCS()
                    # 直角坐标系转地理坐标系
                    target_geo = zhijiao_to_geo(target_temp_coordinate,target_zhijiao)
                    # 地理坐标系转目标投影坐标系
                    # 创建坐标转换对象
                    temp_transform = osr.CoordinateTransformation(target_temp_coordinate, target_coordinate)
                    result = temp_transform.TransformPoint(target_geo[0], target_geo[1])
                else:
                    # 直角坐标系转地理坐标系
                    result = zhijiao_to_geo(target_coordinate, target_zhijiao)
            else:
                # 直接将地理坐标系转为空间直角坐标系
                source_zhijiao = geo_to_zhijiao(source_coordinate,x,y,0)
                # 七参数运算,将源直角坐标系转为目标直角坐标系
                target_zhijiao = qicanshu(source_zhijiao, seven)
                # 判断目标坐标系是否是投影坐标系
                if target_coordinate.IsProjected():
                    # 获取同基准地理坐标系
                    target_temp_coordinate = source_coordinate.CloneGeogCS()
                    # 直角坐标系转地理坐标系
                    target_geo = zhijiao_to_geo(target_temp_coordinate, target_zhijiao)
                    # 地理坐标系转目标投影坐标系
                    # 创建坐标转换对象
                    temp_transform = osr.CoordinateTransformation(target_temp_coordinate, target_coordinate)
                    result = temp_transform.TransformPoint(target_geo[0], target_geo[1])
                else:
                    # 直角坐标系转地理坐标系
                    result = zhijiao_to_geo(target_coordinate, target_zhijiao)
    return result
# 空间直角坐标系转地理坐标系
def zhijiao_to_geo(temp_coordinate,coord):
    # 获取长半轴
    a = temp_coordinate.GetSemiMajor()
    # 获取扁率倒数
    f = temp_coordinate.GetInvFlattening()
    X = coord[0]
    Y = coord[1]
    Z = coord[2]
    e2 = 2 * f - f * f
    L = math.degrees(math.atan(Y / X) + math.pi)
    B2 = math.atan(Z / math.sqrt(X * X + Y * Y))
    B1 = ""
    N = ""
    while True:
        N = a / math.sqrt(1 - f * (2 - f) * math.sin(B2) * math.sin(B2));
        B1 = math.atan((Z + N * f * (2 - f) * math.sin(B2)) / math.sqrt(X * X + Y * Y))
        if math.abs(B1 - B2) < 0.0000000001:
            break
    B2 = B1
    H = Z / math.sin(B2) - N * (1 - e2)
    B = math.toDegrees(B2)
    return [L,B,H]
# 地理坐标系转空间直角坐标系
def geo_to_zhijiao(temp_coordinate,x,y,z):
    # 获取长半轴
    a = temp_coordinate.GetSemiMajor()
    # 获取短半轴
    b = temp_coordinate.GetSemiMinor()
    # 获取偏心率
    ee = (a * a - b * b) / (a * a)
    L = math.radians(x)
    B = math.radians(y)
    H = z
    N = a / math.sqrt(1 - ee * math.sin(B) * math.sin(B))
    X = (N + H) * math.cos(B) * math.cos(L)
    Y = (N + H) * math.cos(B) * math.sin(L)
    Z = (N * (1 - ee) + H) * math.sin(B)
    return [X,Y,Z]
# 七参数运算
def qicanshu(coord,seven):
    # 平移x
    x = seven["x"]
    # 平移y
    y = seven["y"]
    # 平移z
    z = seven["z"]
    # 旋转α
    ox = seven["alpha"]
    # 旋转β
    oy = seven["beta"]
    # 旋转γ
    oz = seven["gamma"]
    # 比例因子k
    k = seven["k"]
    X = x + coord[0] * (1 + k) + oz * coord[1] - oy * coord[2];
    Y = y + coord[1] * (1 + k) - oz * coord[0] + ox * coord[2];
    Z = z + coord[2] * (1 + k) + oy * coord[0] - ox * coord[1];
    return [X,Y,Z]
# 获取导入数据json
def get_import_features(info):
    # 获取文件地址
    file_path = info["file_path"]
    # 获取文件格式
    file_format = info["import_format"]
    # 获取源数据坐标系
    coordinate = info["coordinate"]
    # 返回值
    result = {}
    result["data"] = []
    transform = ""
    result_coordinate = ""
    # 设置源数据坐标系
    source_coordinate = osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(coordinate))
    # 判断是否是投影坐标系 如果是则转为同基准经纬度坐标
    if source_coordinate.IsProjected():
        # 设置目标坐标系为 投影坐标系参考基准
        target_coordinate = source_coordinate.CloneGeogCS()
        # 创建坐标转换对象
        transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
        result_coordinate = target_coordinate.GetName()
    else:
        result_coordinate = source_coordinate.GetName()
    # 设置属性表字段支持中文
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 根据文件格式进行不同的操作
    if file_format == "csv":
        # 获取矢量类型
        feature_type = info["feature_type"]
        # 根据不同类型的进行解析
        if feature_type == "point":
            # 获取xy列号
            x = info["x"]
            y = info["y"]
            # 打开csv文件
            with open(file_path, 'r',encoding='UTF-8') as f:
                reader = list(csv.reader(f))
                field_keys = ""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row == 0:
                        # 获取字段列表
                        field_keys = reader[row]
                    else:
                        # 判断是否需要转换坐标
                        temp_coord = ""
                        if transform == "":
                            temp_coord = [float(reader[row][y]), float(reader[row][x])]
                        else:
                            coords = transform.TransformPoint(float(reader[row][x]), float(reader[row][y]))
                            temp_coord = [coords[0], coords[1]]
                        features_json["features"].append(temp_coord)
                        for i in range(len(reader[row])):
                            features_json["attributes"][field_keys[i]] = reader[row][i]
                        # 设置矢量对象实际类型
                        features_json["type"] = "POINT"
                        result["data"].append(features_json)
            f.close()
        elif feature_type == "line":
            # 获取空间对象列号
            geometry_col = info["geometry"]
            with open(file_path, 'r',encoding='UTF-8') as f:
                reader = list(csv.reader(f))
                field_keys = ""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row == 0:
                        field_keys = reader[row]
                    else:
                        temp_geometry = reader[row][geometry_col]
                        temp_index = temp_geometry.find("(")
                        temp_type = temp_geometry[0:temp_index].rstrip()
                        # 设置矢量对象实际类型
                        features_json["type"] = temp_type
                        if temp_type == "LINESTRING":
                            temp_str = temp_geometry[temp_index + 1:len(temp_geometry) - 1]
                            temp_list = temp_str.split(",")
                            for i in range(len(temp_list)):
                                str_coord = temp_list[i].lstrip().split(" ")
                                # 判断是否需要转换坐标
                                if transform == "":
                                    temp_coord = [float(str_coord[1]), float(str_coord[0])]
                                else:
                                    coords = transform.TransformPoint(float(str_coord[0]), float(str_coord[1]))
                                    temp_coord = [coords[0], coords[1]]
                                features_json["features"].append(temp_coord)
                            for i in range(len(reader[row])):
                                if i != geometry_col:
                                    features_json["attributes"][field_keys[i]] = reader[row][i]
                        elif temp_type == "MULTILINESTRING":
                            temp_str = json.loads(temp_geometry[temp_index:len(temp_geometry)].replace(" ", ",").replace(",,",",").replace("(","[").replace(")", "]"))
                            print(temp_str)
                            for i in range(len(temp_str)):
                                temp_m = []
                                temp_n = []
                                for m in range(len(temp_str[i])):
                                    if len(temp_n) < 2:
                                        temp_n.append(temp_str[i][m])
                                    else:
                                        # 判断是否需要转换坐标
                                        if transform == "":
                                            temp_coord = [float(temp_n[1]), float(temp_n[0])]
                                        else:
                                            coords = transform.TransformPoint(float(temp_n[0]), float(temp_n[1]))
                                            temp_coord = [coords[0], coords[1]]
                                        temp_m.append(temp_coord)
                                        temp_n = []
                                        temp_n.append(temp_str[i][m])
                                features_json["features"].append(temp_m)
                            for i in range(len(reader[row])):
                                if i != geometry_col:
                                    features_json["attributes"][field_keys[i]] = reader[row][i]
                        result["data"].append(features_json)
            f.close()
        elif feature_type == "region":
            geometry_col = info["geometry"]
            with open(file_path, 'r',encoding='UTF-8') as f:
                reader = list(csv.reader(f))
                field_keys = ""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row == 0:
                        field_keys = reader[row]
                    else:
                        temp_geometry = reader[row][geometry_col]
                        temp_index = temp_geometry.find("(")
                        temp_type = temp_geometry[0:temp_index].rstrip()
                        # 设置矢量对象实际类型
                        features_json["type"] = temp_type
                        if temp_type == "MULTIPOLYGON":
                            temp_str = json.loads(temp_geometry[temp_index:len(temp_geometry)].replace(" ", ",").replace(",,",",").replace("(","[").replace(")", "]"))
                            for i in range(len(temp_str)):
                                temp_i = []
                                for m in range(len(temp_str[i])):
                                    temp_m = []
                                    temp_n = []
                                    for n in range(len(temp_str[i][m])):
                                        if len(temp_n) < 2:
                                            temp_n.append(temp_str[i][m][n])
                                        else:
                                            # 判断是否需要转换坐标
                                            if transform == "":
                                                temp_coord = [float(temp_n[1]), float(temp_n[0])]
                                            else:
                                                coords = transform.TransformPoint(float(temp_n[0]), float(temp_n[1]))
                                                temp_coord = [coords[0], coords[1]]
                                            temp_m.append(temp_coord)
                                            temp_n = []
                                            temp_n.append(temp_str[i][m][n])
                                    temp_i.append(temp_m)
                                features_json["features"].append(temp_i)
                            for i in range(len(reader[row])):
                                if i != geometry_col:
                                    features_json["attributes"][field_keys[i]] = reader[row][i]
                        elif temp_type == "POLYGON":
                            temp_str = json.loads(temp_geometry[temp_index:len(temp_geometry)].replace(" ", ",").replace(",,",",").replace("(","[").replace(")", "]"))
                            for i in range(len(temp_str)):
                                temp_m = []
                                temp_n = []
                                for m in range(len(temp_str[i])):
                                    if len(temp_n) < 2:
                                        temp_n.append(temp_str[i][m])
                                    else:
                                        # 判断是否需要转换坐标
                                        if transform == "":
                                            temp_coord = [float(temp_n[1]), float(temp_n[0])]
                                        else:
                                            coords = transform.TransformPoint(float(temp_n[0]), float(temp_n[1]))
                                            temp_coord = [coords[0], coords[1]]
                                        temp_m.append(temp_coord)
                                        temp_n = []
                                        temp_n.append(temp_str[i][m])
                                features_json["features"].append(temp_m)
                            for i in range(len(reader[row])):
                                if i != geometry_col:
                                    features_json["attributes"][field_keys[i]] = reader[row][i]
                        result["data"].append(features_json)
            f.close()
        result["code"] = 200
        result["type"] = feature_type
        result["message"] = "数据获取成功"
        result["coordinate"] = result_coordinate
        return result
    else:
        # 注册所有数据类型驱动
        ogr.RegisterAll()
        driver = ""
        if file_format == "kml":
            # 获取驱动
            driver = ogr.GetDriverByName("KML")
        elif file_format == "shp":
            driver = ogr.GetDriverByName("ESRI Shapefile")
        # 0为以只读方式打开矢量文件 返回数据源
        data_source = driver.Open(file_path, 0)
        # 获取第一张图层
        layer = data_source.GetLayer(0)
        # 获取要素总数
        feature_count = layer.GetFeatureCount(1)
        for i in range(feature_count):
            features_json = {}
            features_json["features"] = []
            features_json["attributes"] = {}
            feature = layer.GetFeature(i)
            # 获取空间对象
            geometry = feature.GetGeometryRef()
            # 获取要素类型 POINT LINESTRING MULTILINESTRING POLYGON MULTIPOLYGON
            geometry_type = geometry.GetGeometryName()
            # 设置矢量对象实际类型
            features_json["type"] = geometry_type
            # 设置整体图层类型
            if geometry_type == "POINT" or geometry_type == "MULTIPOINT":
                result["type"] = "point"
            elif geometry_type == "LINESTRING" or geometry_type == "MULTILINESTRING":
                result["type"] = "line"
            elif geometry_type == "POLYGON" or geometry_type == "MULTIPOLYGON":
                result["type"] = "region"
            if geometry_type == "POINT":
                # 判断是否需要转换坐标
                if transform == "":
                    temp_coord = [geometry.GetY(0),geometry.GetX(0)]
                else:
                    coords = transform.TransformPoint(geometry.GetX(0),geometry.GetY(0))
                    temp_coord = [coords[0], coords[1]]
                features_json["features"].append(temp_coord)
            # 多点集合
            elif geometry_type == "MULTIPOINT":
                print("多点集合")
            # 简单线
            elif geometry_type == "LINESTRING":
                feature_points = geometry.GetPoints()
                temp_coord = []
                for x in range(len(feature_points)):
                    point = list(feature_points[x])
                    # 判断是否需要转换坐标
                    if transform == "":
                        temp_coord2 = [point[1], point[0]]
                    else:
                        coords = transform.TransformPoint(point[0], point[1])
                        temp_coord2 = [coords[0], coords[1]]
                    temp_coord.append(temp_coord2)
                features_json["features"].append(temp_coord)
            # 多线集合
            elif geometry_type == "MULTILINESTRING":
                temp_json = json.loads(geometry.ExportToJson())
                temp_coords = temp_json["coordinates"]
                for j in range(len(temp_coords)):
                    temp_coord = []
                    for s in range(len(temp_coords[j])):
                        # 判断是否需要转换坐标
                        if transform == "":
                            temp_coord2 = [temp_coords[j][s][1], temp_coords[j][s][0]]
                        else:
                            coords = transform.TransformPoint(temp_coords[j][s][0], temp_coords[j][s][1])
                            temp_coord2 = [coords[0], coords[1]]
                        temp_coord.append(temp_coord2)
                    features_json["features"].append(temp_coord)
            # 多个面集合
            elif geometry_type == "MULTIPOLYGON":
                temp_json = json.loads(geometry.ExportToJson())
                temp_coords = temp_json["coordinates"]
                for f in range(len(temp_coords)):
                    temp_parent = []
                    for m in range(len(temp_coords[f])):
                        temp_coord = []
                        for n in range(len(temp_coords[f][m])):
                            # 判断是否需要转换坐标
                            if transform == "":
                                temp_coord2 = [temp_coords[f][m][n][1], temp_coords[f][m][n][0]]
                            else:
                                coords = transform.TransformPoint(temp_coords[f][m][n][0], temp_coords[f][m][n][1])
                                temp_coord2 = [coords[0], coords[1]]
                            temp_coord.append(temp_coord2)
                        temp_parent.append(temp_coord)
                    features_json["features"].append(temp_parent)
            # 简单面
            elif geometry_type == "POLYGON":
                temp_json = json.loads(geometry.ExportToJson())
                temp_coords = temp_json["coordinates"]
                for f in range(len(temp_coords)):
                    temp_coord = []
                    for m in range(len(temp_coords[f])):
                        # 判断是否需要转换坐标
                        if transform == "":
                            temp_coord2 = [temp_coords[f][m][1], temp_coords[f][m][0]]
                        else:
                            coords = transform.TransformPoint(temp_coords[f][m][0], temp_coords[f][m][1])
                            temp_coord2 = [coords[0], coords[1]]
                        temp_coord.append(temp_coord2)
                    features_json["features"].append(temp_coord)
            # 获取字段列表
            feature_keys = feature.keys()
            for j in range(len(feature_keys)):
                # 获取字段类型
                field_info = feature.GetFieldDefnRef(j)
                field_type = field_info.GetTypeName()
                field = ""
                if field_type == "String":
                    field = feature.GetFieldAsString(feature_keys[j])
                elif field_type == "Integer":
                    field = feature.GetFieldAsInteger(feature_keys[j])
                elif field_type == "Double":
                    field = feature.GetFieldAsDouble(feature_keys[j])
                elif field_type == "DateTime":
                    field = feature.GetFieldAsDateTime(feature_keys[j])
                elif field_type == "Binary":
                    field = feature.GetFieldAsBinary(feature_keys[j])
                features_json["attributes"][feature_keys[j]] = field
            result["data"].append(features_json)
        result["code"] = 200
        result["message"] = "数据获取成功"
        result["coordinate"] = result_coordinate
        return result

# 获取导出路径
def get_export_path():
    app = QApplication(sys.argv)
    # 桌面经典窗口类
    rans = QWidget()
    rans.setStyleSheet("background-color:black;")
    rans.setWindowOpacity(0.1)
    # 删除title栏
    rans.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    # 获取桌面
    desktop = QApplication.desktop()
    # 设置宽高
    rans.setFixedSize(desktop.width(), desktop.height())
    rans.show()
    file_path = QFileDialog.getExistingDirectory(rans,"请选择保存路径","D:/")
    return file_path
# 获取列表维度
def get_list_dim(datas):
    if type(datas) is float:
        return False
    return 1+get_list_dim(datas[0])
# 导出数据
def export_features(info):
    # 进度条字典
    progress = {}
    progress["id"] = info["id"]
    progress["progress"] = 0
    progress["exportProgress"] = 0
    file_path = os.path.join(info["savePath"], info["taskName"])
    os.makedirs(file_path)
    source = info["source"]
    target = info["target"]
    features = info["features"]
    seven = info["seven"]
    atrributes = info["attributes"]
    # 设置windows环境下识别中文
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
    if info["saveType"] == "csv":
        # 表头列
        field_keys = []
        # 获取头部列表
        for key in atrributes[0]:
            if key != "parentId" and key != "index":
                field_keys.append(key)
        if info["type"] == "point" or info["type"] == "marker":
            field_keys.append("x")
            field_keys.append("y")
        else:
            field_keys.append("geometry")
        print("头部列表:" + str(field_keys))
        # 构建写入数据对象
        datas=[]
        for j in range(len(atrributes)):
            temp_data = []
            for key in atrributes[j]:
                if key != "parentId" and key != "index":
                    if atrributes[j][key] == []:
                        temp_data.append("")
                    else:
                        temp_data.append(atrributes[j][key])
            # 插入空间对象
            if info["type"] == "point" or info["type"] == "marker":
                # 坐标转换
                temp_feature = get_coordinate_trans(source, target, features[j][0][1], features[j][0][0],seven)
                temp_tup = (temp_feature[0], temp_feature[1])
                # 构建x,y
                x = str(temp_tup[0])
                y = str(temp_tup[1])
                temp_data.append(x)
                temp_data.append(y)
            elif info["type"] == "line":
                print("线类型")
                print(features[j])
                wkt = "LINESTRING("
                for s in range(len(features[j])):
                    temp_feature = get_coordinate_trans(source, target, features[j][s][1],features[j][s][0], seven)
                    temp_tup = (temp_feature[0], temp_feature[1])
                    if s == len(features[j]) - 1:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                    else:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                temp_data.append(wkt)
            elif info["type"] == "region":
                # 获取列表维度
                dim = get_list_dim(features[j])
                # 判断数组维数,4维则是多面类型
                if dim == 4:
                    print("多面类型")
                    wkt = "MULTIPOLYGON("
                    for s in range(len(features[j])):
                        # 通过数组长度判断是简单面还是洞岛面
                        if len(features[j][s]) >1:
                            for x in range(len(features[j][s])):
                                for k in range(len(features[j][s][x])):
                                    temp_feature = get_coordinate_trans(source, target, features[j][s][x][k][1],features[j][s][x][k][0], seven)
                                    temp_tup = (temp_feature[0], temp_feature[1])
                                    if k == 0:
                                        wkt += "(" + str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                                    elif x == len(features[j][s]) - 1:
                                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                                    else:
                                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                        else:
                            for k in range(len(features[j][s][0])):
                                temp_feature = get_coordinate_trans(source, target, features[j][s][0][k][1],features[j][s][0][k][0], seven)
                                temp_tup = (temp_feature[0], temp_feature[1])
                                if k == 0:
                                    wkt += "(" + str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                                elif k == len(features[j][s][0]) - 1:
                                    wkt += str(temp_tup[0])+ " " +str(temp_tup[1])+")"
                                else:
                                    wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                        if s == len(features[j])-1:
                            wkt += ")"
                        else:
                            wkt += ","
                    temp_data.append(wkt)
                elif dim == 3:
                    print("洞岛类型")
                    wkt = "POLYGON("
                    for s in range(len(features[j])):
                        for x in range(len(features[j][s])):
                            temp_feature = get_coordinate_trans(source, target, features[j][s][x][1],features[j][s][x][0], seven)
                            temp_tup = (temp_feature[0], temp_feature[1])
                            if x == 0:
                                wkt += "("+str(temp_tup[0])+" "+str(temp_tup[1])+","
                            elif x == len(features[j][s]) - 1:
                                wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                            else:
                                wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                        if s == len(features[j])-1:
                            wkt+=")"
                        else:
                            wkt+=","
                    temp_data.append(wkt)
                # 判断数组维数,2维则是简单面类型
                elif dim == 2:
                    print("简单面类型")
                    wkt = "POLYGON (("
                    for s in range(len(features[j])):
                        temp_feature = get_coordinate_trans(source, target, features[j][s][1],features[j][s][0], seven)
                        temp_tup = (temp_feature[0], temp_feature[1])
                        if s == len(features[j]) - 1:
                            wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + "))"
                        else:
                            wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                    temp_data.append(wkt)
            current = j + 1
            total = len(features)
            temp_progress = math.floor((current / total) * 100)
            progress["progress"] = temp_progress
            eel.updateTaskProgress(progress)
            datas.append(temp_data)
        # 写入csv
        with open(file_path+"/"+info["taskName"]+".csv", 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(field_keys)
            for i in range(len(datas)):
                writer.writerow(datas[i])
                current = i + 1
                total = len(datas)
                temp_progress = math.floor((current / total) * 100)
                progress["exportProgress"] = temp_progress
                eel.updateTaskProgress(progress)
        f.close()
    else:
        data_source = ""
        layer = ""
        if info["saveType"] == "shp":
            driver = ogr.GetDriverByName("ESRI Shapefile")
            data_source = driver.CreateDataSource(file_path + "/" +info["taskName"] + ".shp")
        elif info["saveType"] == "kml":
            driver = ogr.GetDriverByName("KML")
            data_source = driver.CreateDataSource(file_path + "/" +info["taskName"] + ".kml")
        # 设置坐标系
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(target))
        if info["type"] == "point" or info["type"] == "marker":
            layer = data_source.CreateLayer(info["taskName"], srs, ogr.wkbPoint)
        elif info["type"] == "line":
            layer = data_source.CreateLayer(info["taskName"], srs, ogr.wkbLineString)
        elif info["type"] == "region":
            layer = data_source.CreateLayer(info["taskName"], srs, ogr.wkbMultiPolygon)

        # 设置表头
        for key in atrributes[0]:
            if key != "parentId" and key != "index":
                field_name = ogr.FieldDefn(key, ogr.OFTString)
                field_name.SetWidth(30)
                layer.CreateField(field_name)

        for j in range(len(features)):
            # 插入空间对象
            if info["type"] == "point" or info["type"] == "marker":
                # 获取空间对象类
                feature=ogr.Feature(layer.GetLayerDefn())
                # 坐标转换
                temp_feature = get_coordinate_trans(source, target,features[j][0][1], features[j][0][0],seven)
                if info["saveType"] == "kml":
                    temp_tup = (temp_feature[1], temp_feature[0])
                elif info["saveType"] == "shp":
                    temp_tup = (temp_feature[0], temp_feature[1])
                wkt = "POINT(" + str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                point = ogr.CreateGeometryFromWkt(wkt)
                for key in atrributes[j]:
                    if key!="parentId" and key!="index":
                        if atrributes[j][key] == []:
                            feature.SetField(key,"")
                        else:
                            feature.SetField(key,str(atrributes[j][key]))
                feature.SetGeometry(point)
                layer.CreateFeature(feature)
                current = j + 1
                total = len(features)
                temp_progress = math.floor((current / total) * 100)
                progress["progress"] = temp_progress
                eel.updateTaskProgress(progress)

            elif info["type"] == "line":
                # 获取空间对象类
                feature=ogr.Feature(layer.GetLayerDefn())
                wkt = "LINESTRING("
                for s in range(len(features[j])):
                    temp_feature = get_coordinate_trans(source, target, features[j][s][1], features[j][s][0], seven)
                    if info["saveType"] == "kml":
                        temp_tup = (temp_feature[1], temp_feature[0])
                    elif info["saveType"] == "shp":
                        temp_tup = (temp_feature[0], temp_feature[1])
                    if s == len(features[j]) - 1:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                    else:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                line = ogr.CreateGeometryFromWkt(wkt)
                for key in atrributes[j]:
                    if key!="parentId" and key!="index":
                        if atrributes[j][key] == []:
                            feature.SetField(key,"")
                        else:
                            feature.SetField(key,str(atrributes[j][key]))
                feature.SetGeometry(line)
                layer.CreateFeature(feature)
                current = j + 1
                total = len(features)
                temp_progress = math.floor((current / total) * 100)
                progress["progress"] = temp_progress
                eel.updateTaskProgress(progress)
            elif info["type"] == "region":
                # 获取空间对象类
                feature=ogr.Feature(layer.GetLayerDefn())
                wkt = ""
                # 判断数组维数,4维则是多面类型
                if len(np.array(features[j]).shape) == 3:
                    print("多面类型")
                    wkt = "MULTIPOLYGON(("
                    for s in range(len(features[j][0])):
                        temp_feature = get_coordinate_trans(source, target, features[j][0][s][1], features[j][0][s][0], seven)
                        if info["saveType"] == "kml":
                            temp_tup = (temp_feature[1], temp_feature[0])
                        elif info["saveType"] == "shp":
                            temp_tup = (temp_feature[0], temp_feature[1])
                        if s == len(features[j]) - 1:
                            wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + "))"
                        else:
                            wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                # 判断数组维数,3维则是简单面类型
                elif len(np.array(features[j]).shape) == 2:
                    print("简单面类型")
                    first_point = ""
                    wkt = "POLYGON (("
                    for s in range(len(features[j])):
                        temp_feature = get_coordinate_trans(source, target, features[j][s][1], features[j][s][0], seven)
                        if info["saveType"] == "kml":
                            temp_tup = (temp_feature[1], temp_feature[0])
                            if len(features[j]) == 3:
                                if s ==0:
                                    first_point = (temp_feature[1], temp_feature[0])
                                if s == len(features[j]) - 1:
                                    wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) +","+ str(first_point[0]) + " " + str(first_point[1]) +"))"
                                else:
                                    wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                            else:
                                if s == len(features[j]) - 1:
                                    wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + "))"
                                else:
                                    wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                        elif info["saveType"] == "shp":
                            temp_tup = (temp_feature[0], temp_feature[1])
                            if s == len(features[j]) - 1:
                                wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + "))"
                            else:
                                wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                region = ogr.CreateGeometryFromWkt(wkt)
                for key in atrributes[j]:
                    if key!="parentId" and key!="index":
                        if atrributes[j][key] == []:
                            feature.SetField(key,"")
                        else:
                            feature.SetField(key,str(atrributes[j][key]))
                feature.SetGeometry(region)
                layer.CreateFeature(feature)
                current = j + 1
                total = len(features)
                temp_progress = math.floor((current / total) * 100)
                progress["progress"] = temp_progress
                eel.updateTaskProgress(progress)

        progress["exportProgress"] = 100
        eel.updateTaskProgress(progress)
        # 关闭资源
        feature = None
        data_source = None
    result={}
    result["code"]=200
    result["message"]="数据导出成功"
    return result

def import_scope(info):
    # 获取文件地址
    file_path=info["file_path"]
    # 获取文件格式
    file_format=info["import_format"]
    # 获取源数据坐标系
    coordinate=info["coordinate"]
    # 返回值
    result={}
    transform=""
    result_coordinate=""
    # 设置源数据坐标系
    source_coordinate=osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(coordinate))
    # 判断是否是投影坐标系 如果是则转为同基准经纬度坐标
    if source_coordinate.IsProjected():
        # 设置目标坐标系为 投影坐标系参考基准
        target_coordinate=source_coordinate.CloneGeogCS()
        # 创建坐标转换对象
        transform=osr.CoordinateTransformation(source_coordinate,target_coordinate)
        result_coordinate=target_coordinate.GetName()
    else:
        result_coordinate=source_coordinate.GetName()
    # 设置属性表字段支持中文
    gdal.SetConfigOption("SHAPE_ENCODING","")
    geo_json={
        "type":"FeatureCollection",
        "features":[]
    }
    if file_format=="csv":
        geometry_col=info["geometry"]
        with open(file_path,'r',encoding='UTF-8') as f:
            reader=list(csv.reader(f))
            field_keys=""
            for row in range(len(reader)):
                features={
                    "type":"Feature",
                    "properties":{},
                    "geometry":{
                        "type":"",
                        "coordinates":[]
                    }
                }
                if row==0:
                    field_keys=reader[row]
                else:
                    temp_geometry=reader[row][geometry_col]
                    temp_index=temp_geometry.find("(")
                    temp_type=temp_geometry[0:temp_index].rstrip()
                    if temp_type=="MULTIPOLYGON":
                        features["geometry"]["type"]="MultiPolygon"
                        temp_str=json.loads(
                            temp_geometry[temp_index:len(temp_geometry)].replace(" ",",").replace(",,",",").replace(
                                "(","[").replace(")","]"))
                        for i in range(len(temp_str)):
                            for m in range(len(temp_str[i])):
                                temp_m=[]
                                temp_n=[]
                                for n in range(len(temp_str[i][m])):
                                    if len(temp_n)<2:
                                        temp_n.append(temp_str[i][m][n])
                                    else:
                                        # 判断是否需要转换坐标
                                        if transform=="":
                                            temp_coord=[float(temp_n[0]),float(temp_n[1])]
                                        else:
                                            coords=transform.TransformPoint(float(temp_n[0]),float(temp_n[1]))
                                            temp_coord=[coords[1],coords[0]]
                                        temp_m.append(temp_coord)
                                        temp_n=[]
                                        temp_n.append(temp_str[i][m][n])
                            features["geometry"]["coordinates"].append([temp_m])
                    elif temp_type=="POLYGON":
                        features["geometry"]["type"]="Polygon"
                        temp_str=json.loads(
                            temp_geometry[temp_index:len(temp_geometry)].replace(" ",",").replace(",,",",").replace(
                                "(","[").replace(")","]"))
                        for i in range(len(temp_str)):
                            temp_m=[]
                            temp_n=[]
                            for m in range(len(temp_str[i])):
                                if len(temp_n)<2:
                                    temp_n.append(temp_str[i][m])
                                else:
                                    # 判断是否需要转换坐标
                                    if transform=="":
                                        temp_coord=[float(temp_n[0]),float(temp_n[1])]
                                    else:
                                        coords=transform.TransformPoint(float(temp_n[0]),float(temp_n[1]))
                                        temp_coord=[coords[1],coords[0]]
                                    temp_m.append(temp_coord)
                                    temp_n=[]
                                    temp_n.append(temp_str[i][m])
                        features["geometry"]["coordinates"].append(temp_m)
                    geo_json["features"].append(features)
        f.close()
        result["code"]=200
        result["data"]=geo_json
        result["message"]="数据获取成功"
        result["coordinate"]=result_coordinate
        return result
    else:
        # 注册所有数据类型驱动
        ogr.RegisterAll()
        driver=""
        if file_format=="kml":
            # 获取驱动
            driver=ogr.GetDriverByName("KML")
        elif file_format=="shp":
            driver=ogr.GetDriverByName("ESRI Shapefile")
        # 0为以只读方式打开矢量文件 返回数据源
        data_source=driver.Open(file_path,0)
        # 获取第一张图层
        layer=data_source.GetLayer(0)
        # 获取要素总数
        feature_count=layer.GetFeatureCount(1)
        for i in range(feature_count):
            feature=layer.GetFeature(i)
            # 获取空间对象
            geometry=feature.GetGeometryRef()
            # 获取要素类型 POINT LINESTRING MULTILINESTRING POLYGON MULTIPOLYGON
            geometry_type=geometry.GetGeometryName()
            features={
                "type":"Feature",
                "properties":{
                    "id":"导入范围面"
                },
                "geometry":{
                    "type":"",
                    "coordinates":[]
                }
            }
            # 多个面集合
            if geometry_type=="MULTIPOLYGON":
                features["geometry"]["type"]="MultiPolygon"
                temp_json=json.loads(geometry.ExportToJson())
                temp_coords=temp_json["coordinates"]
                for f in range(len(temp_coords)):
                    temp_coord=[]
                    for m in range(len(temp_coords[f])):
                        for n in range(len(temp_coords[f][m])):
                            # 判断是否需要转换坐标
                            if transform=="":
                                temp_coord2=[temp_coords[f][m][n][0],temp_coords[f][m][n][1]]
                            else:
                                coords=transform.TransformPoint(temp_coords[f][m][n][0],temp_coords[f][m][n][1])
                                temp_coord2=[coords[1],coords[0]]
                            temp_coord.append(temp_coord2)
                    features["geometry"]["coordinates"].append([temp_coord])
            # 简单面
            elif geometry_type=="POLYGON":
                features["geometry"]["type"]="Polygon"
                temp_json=json.loads(geometry.ExportToJson())
                temp_coords=temp_json["coordinates"]
                temp_coord=[]
                for f in range(len(temp_coords)):
                    for m in range(len(temp_coords[f])):
                        # 判断是否需要转换坐标
                        if transform=="":
                            temp_coord2=[temp_coords[f][m][0],temp_coords[f][m][1]]
                        else:
                            coords=transform.TransformPoint(temp_coords[f][m][0],temp_coords[f][m][1])
                            temp_coord2=[coords[1],coords[0]]
                        temp_coord.append(temp_coord2)
                features["geometry"]["coordinates"].append(temp_coord)
            geo_json["features"].append(features)
        result["data"] = geo_json
        result["code"]=200
        result["message"]="数据获取成功"
        result["coordinate"]=result_coordinate
        return result