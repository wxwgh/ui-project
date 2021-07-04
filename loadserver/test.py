# -- coding:utf-8 --
import overpass
import math
import requests
import shutil
import os
from contextlib import closing
import iobjectspy
import socket
import uuid
import base64
import ast
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import sys
import csv
import json
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from loadserver.mainform import MainForm
import decimal
from openpyxl import load_workbook
import pymysql
# iobjectspy.set_iobjects_java_path('E:\SuperMapDemo\yaogan\javaforobject\Bin')
def test():
    import_path = "D:/SuperMap DownLoad/临时/QueryResult.shp"
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    result = iobjectspy.conversion.import_shape(import_path, temp_udb)
    temp_dataset = ""
    prj_unit = ""
    coordinate = ""
    target_pro = ""
    root_pro = ""
    if coordinate == "GCS_BEIJING_1954":
        target_pro = "米"
    else:
        target_pro = "度"
    if result is not None:
        temp_dataset = temp_udb.get_dataset(result[0])
        prj_unit=temp_dataset.prj_coordsys.coord_unit
    if prj_unit == iobjectspy.enums.Unit.METER:
        root_pro="米"
    elif prj_unit == iobjectspy.enums.Unit.DEGREE:
        root_pro="度"
    # 创建datasetvector
    temp_vector = temp_udb.write_recordset(temp_dataset)
    if root_pro == "度" and target_pro == "米":
        temp_result = iobjectspy.data.CoordSysTranslator.forward(temp_vector, iobjectspy.data.PrjCoordSys(
            prj_type="GCS_WGS_1984"), iobjectspy.data.CoordSysTransParameter(),
                                                                 coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,
                                                                 out_data=temp_udb)
    elif root_pro == "米" and target_pro == "度":
        temp_result = iobjectspy.data.CoordSysTranslator.inverse(temp_vector, iobjectspy.data.PrjCoordSys(
            prj_type="GCS_WGS_1984"), iobjectspy.data.CoordSysTransParameter(),
                                                                 coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,
                                                                 out_data=temp_udb)
    else:
        temp_result = iobjectspy.data.CoordSysTranslator.convert(temp_vector, iobjectspy.data.PrjCoordSys(
            prj_type="GCS_WGS_1984"), iobjectspy.data.CoordSysTransParameter(),
                                                                 coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,
                                                                 out_data=temp_udb)
def export_shape():
    export_path="D:/SuperMap DownLoad/临时/test.shp"
    attribute={}
    attribute["id"]=100
    attribute["UserID"]=100
    type = "Point"
    if type == "Point":
        type ="1"
    geometry_json = '{"Point":[113.58727668000006, 22.16493972869857],"id":1}'
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 创建数据集类
    temp_vector = temp_udb.create_vector_dataset("ni","POINT",False)
    # 创建字段
    # 字段信息类
    temp_list=[]
    temp_info1 = iobjectspy.data.FieldInfo("name","TEXT",max_length=None, default_value=None, caption=None,is_required=False, is_zero_length_allowed=True)
    temp_info2 = iobjectspy.data.FieldInfo("type","TEXT",max_length=None, default_value=None, caption=None,is_required=False, is_zero_length_allowed=True)
    temp_list.append(temp_info1)
    temp_list.append(temp_info2)
    temp_vector.create_fields(temp_list)
    temp_dict={}
    temp_dict["name"]="你好"
    temp_dict["type"]="点"
    # 创建geometry
    temp_geometry = iobjectspy.data.Geometry.from_json(geometry_json)
    temp_feature = iobjectspy.data.Feature(temp_geometry,temp_dict,"100",temp_list)
    # 在数据集类中追加数据
    temp_vector.append(temp_feature)
    # 创建字段
    print(temp_vector)
    iobjectspy.conversion.export_to_shape(temp_vector, export_path)

def progress(step_event):
    print(step_event)
def test_osm():
    # 导出监听函数
    def export_progress(step_event):
        print(step_event)
    # 导入监听函数
    def load_progress(step_event):
        print(step_event)
    data_url = "../osm/osm.udbx"
    # 数据集名称
    dataset_names = "naturals"
    # 连接信息
    connectInfo = iobjectspy.data.DatasourceConnectionInfo(data_url)
    # 叠加面
    sss = [[[107.161097,21.125498],[107.161097,24.20689],[115.468099,24.20689],[115.468099,21.125498],[107.161097,21.125498]]]
    # dataset_overlay = iobjectspy.data.Geometry.from_json('{"Region":[[[116.197625,39.3088],[116.197625,39.926588],[117.175565,39.926588],[ 117.175565,39.3088],[116.197625,39.3088]]],"id":1}')
    dataset_overlay = iobjectspy.data.Geometry.from_json('{"Region":[[[107.161097,21.125498],[107.161097,24.20689],[115.468099,24.20689],[115.468099,21.125498],[107.161097,21.125498]]],"id":1}')
    # 打开数据源
    data_source = iobjectspy.data.Datasource.open(connectInfo)
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 获取数据集
    print(dataset_names)
    dataset = data_source.get_dataset(dataset_names)
    # 导出路径
    file_path = "D:/SuperMap DownLoad/测试osm/"+dataset_names+".shp"
    try:
        result_vector = iobjectspy.analyst.overlay(dataset, [dataset_overlay], iobjectspy.enums.OverlayMode.CLIP,out_data =temp_udb,out_dataset_name =dataset_names)
    except:
        print("该范围下无数据")
    else:
        iobjectspy.conversion.export_to_shape(result_vector, file_path)
def test_mac():
    ip = socket.gethostbyname(socket.gethostname())
    name = socket.getfqdn(socket.gethostname())
    node = uuid.getnode()
    macHex = uuid.UUID(int=node).hex[-12:]
    mac = []
    str_mac=""
    for i in range(len(macHex))[::2]:
        mac.append(macHex[i:i + 2])
    str_mac = '-'.join(mac).upper()
    print('IP:', ip)
    print('name',name)
    print(str_mac)
def test_file():
    file_path = "D:/SuperMap DownLoad/许可文件时间/测试物理地址2/测试物理地址2.sm1x"
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
    file.close()
    node = uuid.getnode()
    macHex = uuid.UUID(int=node).hex[-12:]
    mac = []
    str_mac = ""
    for i in range(len(macHex))[::2]:
        mac.append(macHex[i:i + 2])
    str_mac = '-'.join(mac).upper()
    if str_mac == url:
        print("相等")
    print(time)
    print(url)
    print(str_mac)
def test_import_features():
    path = r"D:/SuperMap DownLoad/临时/QueryResult_region_bz.csv"
    import_type = "csv"
    feature_type = "region"
    x = 2
    y = 3
    driver_name=""
    if import_type == "kml":
        driver_name = "KML"
    elif import_type == "shp":
        driver_name = "ESRI Shapefile"
    if import_type == "csv":
        # 创建结果字典
        result = {}
        result["data"] = []
        result["is_load"] = False
        if feature_type == "point":
            # 获取数据源坐标系
            source_coordinate = osr.SpatialReference()
            source_coordinate.ImportFromEPSG(4610)
            # 设置目标坐标系为WGS84
            target_coordinate = osr.SpatialReference()
            target_coordinate.ImportFromEPSG(4326)
            # 创建坐标转换对象
            transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
            with open(path,'r') as f:
                reader = list(csv.reader(f))
                field_keys=""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row ==0:
                        field_keys = reader[row]
                    else:
                        coords = transform.TransformPoint(float(reader[row][x]),float(reader[row][y]))
                        temp_coord = [coords[0], coords[1]]
                        features_json["features"].append(temp_coord)
                        for i in range(len(reader[row])):
                            features_json["attributes"][field_keys[i]] = reader[row][i]
                        result["data"].append(features_json)
            f.close()
            print(result)
        elif feature_type == "line":
            # 获取数据源坐标系
            source_coordinate = osr.SpatialReference()
            source_coordinate.ImportFromEPSG(4610)
            print(source_coordinate.GetName())
            # 设置目标坐标系为WGS84
            target_coordinate = osr.SpatialReference()
            target_coordinate.ImportFromEPSG(4326)
            print(target_coordinate.GetName())
            # 创建坐标转换对象
            transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
            geometry_col = 4
            with open(path,'r') as f:
                reader = list(csv.reader(f))
                field_keys=""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row ==0:
                        field_keys = reader[row]
                        print(field_keys)
                    else:
                        temp_geometry = reader[row][geometry_col]
                        temp_index = temp_geometry.find("(")
                        temp_type = temp_geometry[0:temp_index].rstrip()
                        temp_str = temp_geometry[temp_index+1:len(temp_geometry)-1]
                        temp_list = temp_str.split(",")
                        for i in range(len(temp_list)):
                            str_coord = temp_list[i].lstrip().split(" ")
                            coords = transform.TransformPoint(float(str_coord[1]),float(str_coord[0]))
                            temp_coord = [coords[0], coords[1]]
                            features_json["features"].append(temp_coord)
                        for i in range(len(reader[row])):
                            if i != geometry_col:
                                features_json["attributes"][field_keys[i]] = reader[row][i]
                        result["data"].append(features_json)
            f.close()
            print(result)
        elif feature_type == "region":
            # 获取数据源坐标系
            source_coordinate = osr.SpatialReference()
            source_coordinate.ImportFromEPSG(4490)
            # 设置目标坐标系为WGS84
            target_coordinate = osr.SpatialReference()
            target_coordinate.ImportFromEPSG(4326)
            # 创建坐标转换对象
            transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
            geometry_col = 2
            with open(path,'r') as f:
                reader = list(csv.reader(f))
                field_keys=""
                for row in range(len(reader)):
                    features_json = {}
                    features_json["features"] = []
                    features_json["attributes"] = {}
                    if row ==0:
                        field_keys = reader[row]
                    else:
                        temp_geometry = reader[row][geometry_col]
                        temp_index = temp_geometry.find("(")
                        temp_type = temp_geometry[0:temp_index].rstrip()
                        if temp_type == "MULTIPOLYGON":
                            temp_str = json.loads(temp_geometry[temp_index:len(temp_geometry)].replace(" ",",").replace(",,",",").replace("(","[").replace(")","]"))
                            temp_parent=[]
                            for i in range(len(temp_str)):
                                temp_i=[]
                                for m in range(len(temp_str[i])):
                                    temp_m = []
                                    temp_n = []
                                    for n in range(len(temp_str[i][m])):
                                        if len(temp_n) < 2:
                                            temp_n.append(temp_str[i][m][n])
                                        else:
                                            coords = transform.TransformPoint(float(temp_n[1]),float(temp_n[0]))
                                            temp_coord = [coords[0], coords[1]]
                                            temp_m.append(temp_coord)
                                            temp_n = []
                                            temp_n.append(temp_str[i][m][n])
                                    temp_i.append(temp_m)
                                features_json["features"].append(temp_i)
                            for i in range(len(reader[row])):
                                if i != geometry_col:
                                    features_json["attributes"][field_keys[i]] = reader[row][i]
                            result["data"].append(features_json)
                        elif temp_type == "POLYGON":
                            temp_str = json.loads(temp_geometry[temp_index:len(temp_geometry)].replace(" ", ",").replace(",,",",").replace("(","[").replace(")", "]"))
                            for i in range(len(temp_str)):
                                temp_m = []
                                temp_n = []
                                for m in range(len(temp_str[i])):
                                    if len(temp_n) < 2:
                                        temp_n.append(temp_str[i][m])
                                    else:
                                        coords = transform.TransformPoint(float(temp_n[1]), float(temp_n[0]))
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
            result["message"] = "数据获取成功"
            print(result)
                            # 写入csv
                            # header = field_keys
                            # data = [
                            #     ['山东省', 0, temp_type+" "+json.dumps(temp_parent)],
                            # ]
                            # save_path=r"D:/SuperMap DownLoad/临时/QueryResult_region_bz_my.csv"
                            # with open(save_path, 'w', encoding='utf-8-sig', newline='') as f:
                            #     writer = csv.writer(f)
                            #     writer.writerow(header)
                            #     writer.writerows(data)
    else:
        # 注册所有数据类型驱动
        ogr.RegisterAll()
        # 获取驱动
        driver = ogr.GetDriverByName(driver_name)
        # 支持中文路径
        # gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
        # 支持属性表字段为中文
        # gdal.SetConfigOption("SHAPE_ENCODING", "")

        # 0为以只读方式打开矢量文件 返回数据源
        data_source = driver.Open(path,0)
        # 获取图层总数量
        # layer_count = data_source.GetLayerCount()
        #获取第一张图层
        layer = data_source.GetLayer(0)
        # 获取数据源坐标系
        source_coordinate = osr.SpatialReference()
        source_coordinate.SetGeocCS("Xian 1980")
        # 设置目标坐标系为WGS84
        target_coordinate = osr.SpatialReference()
        target_coordinate.SetGeocCS("WGS 84")
        # 创建坐标转换对象
        transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
        # 创建结果字典
        result={}
        result["data"]=[]
        result["is_load"]=False
        #获取要素总数
        feature_count = layer.GetFeatureCount(1)
        for i in range(feature_count):
            features_json = {}
            features_json["features"] = []
            features_json["attributes"] = {}
            feature = layer.GetFeature(i)
            # 获取空间对象
            geometry = feature.GetGeometryRef()
            # 获取要素类型 POINT LINESTRING MULTIPOLYGON
            geometry_type = geometry.GetGeometryName()
            features_json["type"] = geometry_type
            if geometry_type == "POINT":
                coords = transform.TransformPoint(geometry.GetX(0),geometry.GetY(0))
                temp_coord = [coords[0],coords[1]]
                features_json["features"].append(temp_coord)
            elif geometry_type == "LINESTRING":
                feature_points = geometry.GetPoints()
                temp_coord=[]
                for x in range(len(feature_points)):
                    point = list(feature_points[x])
                    # 坐标转换
                    coords = transform.TransformPoint(point[0], point[1])
                    temp_coord.append([coords[0], coords[1]])
                features_json["features"].append(temp_coord)
            # 多个面集合
            elif geometry_type == "MULTIPOLYGON":
                temp_json = json.loads(geometry.ExportToJson())
                temp_coords = temp_json["coordinates"]
                for f in range(len(temp_coords)):
                    temp_parent=[]
                    for m in range(len(temp_coords[f])):
                        temp_coord=[]
                        for n in range(len(temp_coords[f][m])):
                            # 坐标转换
                            coords = transform.TransformPoint(temp_coords[f][m][n][0], temp_coords[f][m][n][1])
                            temp_coord.append([coords[0], coords[1]])
                        temp_parent.append(temp_coord)
                    features_json["features"].append(temp_parent)

            # 简单面
            elif geometry_type == "POLYGON":
                temp_json = json.loads(geometry.ExportToJson())
                temp_coords = temp_json["coordinates"]
                for f in range(len(temp_coords)):
                    temp_coord = []
                    for m in range(len(temp_coords[f])):
                        # 坐标转换
                        coords = transform.TransformPoint(temp_coords[f][m][0], temp_coords[f][m][1])
                        temp_coord.append([coords[0], coords[1]])
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
            result["is_load"]=True
        print(result)
        # keys = feature.keys()
        # print(keys)
        # print(type(keys))
        # field = feature.GetFieldAsInteger("userid")
        # print(field)
        # print(type(field))
maxInt = sys.maxsize
decrement = True
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
def test_import_path():
    app = QApplication(sys.argv)
    # 桌面经典窗口类
    rans = QWidget()
    rans.setStyleSheet("background-color:black;")
    rans.setWindowOpacity(0.5)
    # 删除title栏
    rans.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
    # 获取桌面
    desktop = QApplication.desktop()
    # 设置宽高
    rans.setFixedSize(desktop.width(), desktop.height())
    rans.show()
    path = QFileDialog.getOpenFileName(rans, "请选择要添加的文件", "D:/SuperMap DownLoad/临时", "Shape File (*.shp);;KML (*.kml);;CSV (*.csv)")
    file_path = path[0]
    result = {}
    if file_path == "":
        result["file_path"] = file_path
        result["coordinate"] = ""
    else:
        temp_str = file_path.split(".")[1]
        if temp_str == "shp":
            # 获取坐标系
            coordinate = get_shp_coordinate(file_path)
            result["file_path"] = file_path
            result["coordinate"] = coordinate
        else:
            result["file_path"] = file_path
            result["coordinate"]="WGS 84"
    print(result)
    # app.exec_()
def get_shp_coordinate(path):
    # 注册所有数据类型驱动
    ogr.RegisterAll()
    # 获取驱动
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # 0为以只读方式打开矢量文件 返回数据源
    data_source = driver.Open(path, 0)
    # 获取第一张图层
    layer = data_source.GetLayer(0)
    # 获取数据源坐标系
    source_coordinate = layer.GetSpatialRef()
    return source_coordinate.GetName()

# BP能源导入
def test_import_excel():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【0】BP能源属性数据_任亚文/能源属性数据/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        # if file_names[x] == "可再生-风能（装机容量）.xlsx":
            file_path = dir_path+file_names[x]
            file = load_workbook(file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            temp_year=[]
            temp_unit = ""
            temp_type = ""
            for row in range(1,rows+1):
                temp_value = {}
                temp_value["year"] = []
                temp_value["values"] = []
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row == 1 and col == 1:
                        temp_unit = value
                        temp_type = file_names[x].split(".")[0]
                    elif row == 1 and col != 1:
                        if value != "" and value != None:
                            temp_year.append(value)
                    elif row !=1 and col == 1:
                        if value != "" and value != None:
                            temp_value["country_en"] = value
                    elif row !=1 and col != 1:
                        if value == "n/a":
                            temp_value["values"].append(0)
                            temp_value["year"].append(temp_year[col - 2])
                        elif value !="" and value!=None:
                            temp_value["values"].append(value)
                            temp_value["year"].append(temp_year[col - 2])
                if len(temp_value["values"]) != 0 and "country_en" in temp_value.keys():
                    temp_value["unit"] = temp_unit
                    temp_value["type"] = temp_type
                    temp_values.append(temp_value)
            for i in range(len(temp_values)):
                for j in range(len(temp_values[i]["year"])):
                    sql_str = "insert into bpnengyuan (country_en,type,year,unit,value) values \
                                     ('%s','%s','%s','%s','%s')" % \
                              (temp_values[i]["country_en"],temp_values[i]["type"],temp_values[i]["year"][j],\
                               temp_values[i]["unit"],temp_values[i]["values"][j])
                    cursor.execute(sql_str)
                    conn.commit()
    conn.close()
# 能源贸易
def test_import_excel2():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【1】能源贸易_何则/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") !=-1:
            print(file_names[x])
            file_path = dir_path+file_names[x]
            file = load_workbook(file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and col == 1:
                        if value == None or value == "":
                            temp_value["exporter_iso3"] = ""
                        else:
                            temp_value["exporter_iso3"] = value
                    elif row != 1 and col == 2:
                        if value == None or value == "":
                            temp_value["exporter"] = ""
                        else:
                            temp_value["exporter"] = value
                    elif row !=1 and col == 3:
                        if value == None or value == "":
                            temp_value["importer_iso3"] = ""
                        else:
                            temp_value["importer_iso3"] = value
                    elif row !=1 and col == 4:
                        if value == None or value == "":
                            temp_value["importer"] = ""
                        else:
                            temp_value["importer"] = value

                    elif row !=1 and col == 5:
                        if value == None or value == "":
                            temp_value["type"] = ""
                        else:
                            temp_value["type"] = value
                    elif row !=1 and col == 6:
                        if value == None or value == "":
                            temp_value["code"] = 0
                        else:
                            temp_value["code"] = value
                    elif row !=1 and col == 7:
                        if value == None or value == "":
                            temp_value["year"] = ""
                        else:
                            temp_value["year"] = value
                    elif row !=1 and col == 8:
                        if value == "" or value == None:
                            temp_value["value"] = 0
                        else:
                            temp_value["value"] = value
                    elif row !=1 and col == 9:
                        if value == "" or value == None:
                            temp_value["weight"] = 0
                        else:
                            temp_value["weight"] = value
                if "exporter_iso3" in temp_value.keys():
                    temp_value["value_unit"] = "1000USD"
                    temp_value["weight_unit"] = "1000kg"
                    temp_values.append(temp_value)
            for i in range(len(temp_values)):
                sql_str = "insert into nengyuanmaoyi (exporter_iso3,exporter,importer_iso3,importer,type,code,year,value,value_unit,weight,weight_unit) values \
                                 ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                          (temp_values[i]["exporter_iso3"],temp_values[i]["exporter"],temp_values[i]["importer_iso3"],\
                           temp_values[i]["importer"],temp_values[i]["type"],temp_values[i]["code"],temp_values[i]["year"],\
                           temp_values[i]["value"],temp_values[i]["value_unit"],temp_values[i]["weight"],temp_values[i]["weight_unit"])
                cursor.execute(sql_str)
                conn.commit()
    conn.close()
# 新能源贸易导入
def test_import_excel3():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【2】新能源贸易_夏四友/15种新能源关键稀缺材料/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        # 拼接地址
        temp_path = dir_path+file_names[x]
        # 判断是否是目录
        if os.path.isdir(temp_path):
            temp_file_names = os.listdir(temp_path)
            for s in range(len(temp_file_names)):
                temp_file_path = temp_path+"/"+temp_file_names[s]
                file = load_workbook(temp_file_path)
                table = file.get_sheet_by_name(file.sheetnames[0])
                # 行数
                rows = table.max_row
                # 列数
                cols = table.max_column
                temp_values=[]
                for row in range(1,rows+1):
                    temp_value = {}
                    for col in range(1, cols + 1):
                        value = table.cell(row=row, column=col).value
                        if row != 1 and col == 1:
                            if value == None or value == "":
                                temp_value["exporter_iso3"] = ""
                            else:
                                temp_value["exporter_iso3"] = value
                        elif row != 1 and col == 2:
                            if value == None or value == "":
                                temp_value["exporter"] = ""
                            elif value.find("Ivoire")!=-1:
                                temp_value["exporter"] = value.replace("'"," ")
                            else:
                                temp_value["exporter"] = value
                        elif row !=1 and col == 3:
                            if value == None or value == "":
                                temp_value["importer_iso3"] = ""
                            else:
                                temp_value["importer_iso3"] = value
                        elif row !=1 and col == 4:
                            if value == None or value == "":
                                temp_value["importer"] = ""
                            elif value.find("Ivoire")!=-1:
                                temp_value["importer"] = value.replace("'"," ")
                            else:
                                temp_value["importer"] = value

                        elif row !=1 and col == 5:
                            if value == None or value == "":
                                temp_value["type"] = ""
                            else:
                                temp_value["type"] = value
                        elif row !=1 and col == 6:
                            if value == None or value == "":
                                temp_value["code"] = 0
                            else:
                                temp_value["code"] = value
                        elif row !=1 and col == 7:
                            if value == None or value == "":
                                temp_value["year"] = ""
                            else:
                                temp_value["year"] = value
                        elif row !=1 and col == 8:
                            if value == "" or value == None:
                                temp_value["value"] = 0
                            else:
                                temp_value["value"] = value
                        elif row !=1 and col == 9:
                            if value == "" or value == None:
                                temp_value["weight"] = 0
                            else:
                                temp_value["weight"] = value
                    if "exporter" in temp_value.keys() and "importer" in temp_value.keys():
                        if temp_value["exporter"] != "" and temp_value["importer"] != "":
                            temp_value["value_unit"] = "1000USD"
                            temp_value["weight_unit"] = "1000kg"
                            temp_values.append(temp_value)
                for i in range(len(temp_values)):
                    sql_str = "insert into xinnengyuanmaoyi (exporter_iso3,exporter,importer_iso3,importer,type,code,year,value,value_unit,weight,weight_unit) values \
                                     ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                              (temp_values[i]["exporter_iso3"],temp_values[i]["exporter"],temp_values[i]["importer_iso3"],\
                               temp_values[i]["importer"],temp_values[i]["type"],temp_values[i]["code"],temp_values[i]["year"],\
                               temp_values[i]["value"],temp_values[i]["value_unit"],temp_values[i]["weight"],temp_values[i]["weight_unit"])
                    cursor.execute(sql_str)
                    conn.commit()
                print(temp_file_path+"插入成功")
    conn.close()
# 隐含能源贸易导入 目前只有煤炭
def test_import_excel4():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【5】隐含能源贸易_周彦楠/【1】隐含能源OD数据/【1】coal/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        temp_file_path = dir_path+file_names[x]
        file = load_workbook(temp_file_path)
        table = file.get_sheet_by_name(file.sheetnames[1])
        # 行数
        rows = table.max_row
        # 列数
        cols = table.max_column
        temp_values=[]
        for row in range(1,rows+1):
            temp_value = {}
            for col in range(1, cols + 1):
                value = table.cell(row=row, column=col).value
                if row != 1 and col == 1:
                    if value == None or value == "":
                        temp_value["exporter"] = ""
                    elif value.find("Ivoire") != -1:
                        temp_value["exporter"] = value.replace("'", " ")
                    else:
                        temp_value["exporter"] = value
                elif row != 1 and col == 2:
                    if value == None or value == "":
                        temp_value["importer"] = ""
                    elif value.find("Ivoire")!=-1:
                        temp_value["importer"] = value.replace("'"," ")
                    else:
                        temp_value["importer"] = value
                elif row !=1 and col == 3:
                    if value == None or value == "":
                        temp_value["weight"] = 0
                    else:
                        temp_value["weight"] = value
            if "exporter" in temp_value.keys() and "importer" in temp_value.keys():
                if temp_value["exporter"] != "" and temp_value["importer"] != "":
                    temp_value["weight_unit"] = "mtoe"
                    temp_value["type"] = "coal"
                    temp_value["year"] = file_names[x].split("_")[0]
                    temp_values.append(temp_value)
        print(temp_values)
        for i in range(len(temp_values)):
            sql_str = "insert into yinhannengyuanmaoyi (exporter,importer,type,year,weight,weight_unit) values \
                             ('%s','%s','%s','%s','%s','%s')" % \
                      (temp_values[i]["exporter"],temp_values[i]["importer"],temp_values[i]["type"],temp_values[i]["year"],\
                       temp_values[i]["weight"],temp_values[i]["weight_unit"])
            cursor.execute(sql_str)
            conn.commit()
        print(temp_file_path+"插入成功")
    conn.close()
# 隐含能源贸易分布 目前仅有煤炭
def test_import_excel5():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【5】隐含能源贸易_周彦楠/【2】隐含能源分布数据/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        temp_file_path = dir_path+file_names[x]
        file = load_workbook(temp_file_path)
        table = file.get_sheet_by_name(file.sheetnames[0])
        # 行数
        rows = table.max_row
        # 列数
        cols = table.max_column
        temp_values=[]
        for row in range(1,rows+1):
            temp_value = {}
            for col in range(1, cols + 1):
                value = table.cell(row=row, column=col).value
                if row != 1 and col == 1:
                    if value == None or value == "":
                        temp_value["country"] = ""
                    elif value.find("Ivoire") != -1:
                        temp_value["country"] = value.replace("'", " ")
                    else:
                        temp_value["country"] = value
                if row != 1 and col == 2:
                    if value == None or value == "":
                        temp_value["export_weight"] = 0
                    else:
                        temp_value["export_weight"] = value
                elif row != 1 and col == 3:
                    if value == None or value == "":
                        temp_value["import_weight"] = 0
                    else:
                        temp_value["import_weight"] = value
                elif row !=1 and col == 4:
                    if value == None or value == "":
                        temp_value["net_export_weight"] = 0
                    else:
                        temp_value["net_export_weight"] = value
            if "country" in temp_value.keys():
                if temp_value["country"] != "":
                    temp_value["weight_unit"] = "mtoe"
                    temp_value["type"] = "coal"
                    temp_value["year"] = file_names[x].split(".")[0].split("出口")[1]
                    temp_values.append(temp_value)
        for i in range(len(temp_values)):
            sql_str = "insert into yinhannengyuanmaoyifenbu (country,export_weight,import_weight,net_export_weight,weight_unit,type,year) values \
                             ('%s','%s','%s','%s','%s','%s','%s')" % \
                      (temp_values[i]["country"],temp_values[i]["export_weight"],temp_values[i]["import_weight"],temp_values[i]["net_export_weight"],\
                       temp_values[i]["weight_unit"],temp_values[i]["type"],temp_values[i]["year"])
            cursor.execute(sql_str)
            conn.commit()
        print(temp_file_path+"插入成功")
        # 批量插入
        # sql_str = "insert into yinhannengyuanmaoyifenbu (country,export_weight,import_weight,net_export_weight,weight_unit,type,year) values \
        #                  (%s,%s,%s,%s,%s,%s,%s)"
        # res = cursor.executemany(sql_str,temp_values)
        # print(res)
        # conn.commit()
        # print(temp_file_path+"插入成功")
    conn.close()
#专利转移数据导入
def test_import_excel6():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【6】能源技术_钱肖颖/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and row !=2 and col == 1:
                        temp_value["year"] = str(value)
                    elif row != 1 and row !=2 and col == 2:
                        temp_value["title_en"] = str(value)
                    elif row != 1 and row !=2 and col == 3:
                        temp_value["abstract_en"] = str(value)
                    elif row != 1 and row !=2 and col == 4:
                        temp_value["pub_year"] = str(value)
                    elif row != 1 and row !=2 and col == 5:
                        temp_value["title_ch"] = str(value)
                    elif row != 1 and row !=2 and col == 6:
                        temp_value["abstract_ch"] = str(value)
                    elif row != 1 and row !=2 and col == 7:
                        temp_value["main_ipc"] = str(value)
                    elif row != 1 and row !=2 and col == 8:
                        temp_value["ipc"] = str(value)
                    elif row != 1 and row !=2 and col == 9:
                        if value == None or value == "":
                            temp_value["exporter"] = ""
                        else:
                            temp_value["exporter"] = str(value)
                    elif row != 1 and row !=2 and col == 10:
                        if value == None or value == "":
                            temp_value["importer"] = ""
                        else:
                            temp_value["importer"] = str(value)
                if "year" in temp_value.keys():
                    temp_values.append(temp_value)
            for i in range(len(temp_values)):
                sql_str = "insert into zhuanlizhuanyi (year,title_en,abstract_en,pub_year,title_ch,abstract_ch,main_ipc,ipc,exporter,importer) values \
                                 ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                          (temp_values[i]["year"], temp_values[i]["title_en"], temp_values[i]["abstract_en"],\
                           temp_values[i]["pub_year"], temp_values[i]["title_ch"],\
                           temp_values[i]["abstract_ch"], temp_values[i]["main_ipc"], temp_values[i]["ipc"],\
                           temp_values[i]["exporter"],temp_values[i]["importer"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
#能源治理组织导入
def test_import_excel7():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【7】能源组织_任亚文/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            # 组织列表
            temp_organizations=[]
            for row in range(1,rows+1):
                temp_value = {}
                temp_value["is_joins"]=[]
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row == 1 and col > 2:
                        if value !="" and value !=None:
                            temp_organizations.append(str(value))
                    elif row != 1 and col == 1:
                        temp_value["country_ch"] = str(value)
                    elif row != 1 and col == 2:
                        temp_value["country_en"] = str(value)
                    elif row != 1 and col > 2:
                        if value != "" and value != None and str(value).find("=SUM")==-1:
                            temp_value["is_joins"].append(str(value))
                if len(temp_value["is_joins"]) !=0:
                    temp_value["organizations"] = temp_organizations
                    temp_values.append(temp_value)
            for i in range(len(temp_values)):
                for j in range(len(temp_values[i]["organizations"])):
                    sql_str = "insert into nengyuanzhilizuzhi (country_ch,country_en,organization,is_join) values \
                                     ('%s','%s','%s','%s')" % \
                              (temp_values[i]["country_ch"], temp_values[i]["country_en"], temp_values[i]["organizations"][j],\
                               temp_values[i]["is_joins"][j])
                    cursor.execute(sql_str)
                    conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()

#能源企业导入 目前只有中国
def test_import_excel8():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【11】中国能源企业的点位数据_钱肖颖/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and row !=2 and col == 1:
                        temp_value["company"] = str(value)
                    elif row != 1 and row !=2 and col == 2:
                        temp_value["registration"] = str(value)
                    elif row != 1 and row !=2 and col == 3:
                        temp_value["capital"] = str(value)
                    elif row != 1 and row !=2 and col == 4:
                        if value == None:
                            temp_value["Incorporation_year"] = ""
                        else:
                            temp_value["Incorporation_year"] = str(value)
                    elif row != 1 and row !=2 and col == 5:
                        if value == None:
                            temp_value["approval_year"] = ""
                        else:
                            temp_value["approval_year"] = str(value)
                    elif row != 1 and row !=2 and col == 6:
                        temp_value["province"] = str(value)
                    elif row != 1 and row !=2 and col == 7:
                        temp_value["city"] = str(value)
                    elif row != 1 and row !=2 and col == 8:
                        temp_value["county"] = str(value)
                    elif row != 1 and row !=2 and col == 9:
                        temp_value["type"] = str(value)
                    elif row != 1 and row !=2 and col == 10:
                        temp_value["sector"] = str(value)
                    elif row != 1 and row !=2 and col == 11:
                        temp_value["address"] = str(value)
                    elif row != 1 and row !=2 and col == 12:
                        temp_value["business_scope"] = str(value)
                    elif row != 1 and row !=2 and col == 13:
                        temp_value["lon"] = str(value)
                    elif row != 1 and row !=2 and col == 14:
                        temp_value["lat"] = str(value)
                if "company" in temp_value.keys():
                    temp_values.append(temp_value)
            print(temp_values)
            for i in range(len(temp_values)):
                sql_str = "insert into nengyuanqiye (company,registration,capital,Incorporation_year,approval_year,province,city,county,\
                            type,sector,address,business_scope,lon,lat) values \
                                 ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                          (temp_values[i]["company"], temp_values[i]["registration"], temp_values[i]["capital"],\
                           temp_values[i]["Incorporation_year"], temp_values[i]["approval_year"],\
                           temp_values[i]["province"], temp_values[i]["city"], temp_values[i]["county"],\
                           temp_values[i]["type"],temp_values[i]["sector"],temp_values[i]["address"],temp_values[i]["business_scope"],\
                           temp_values[i]["lon"],temp_values[i]["lat"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
#全球电力装机容量 导入
def test_import_excel9():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【10】全球能源基础设施数据_何则&周彦楠/【2】全球电力装机容量/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and col == 1:
                        temp_value["year"] = str(value)
                    elif row != 1 and col == 2:
                        temp_value["weight"] = str(value)
                    elif row != 1 and col == 3:
                        temp_value["country"] = str(value)
                    elif row != 1 and col == 4:
                        temp_value["country_iso3"] = str(value)
                    elif row != 1 and col == 5:
                        temp_value["weight_unit"] = str(value)
                if "year" in temp_value.keys():
                    temp_values.append(temp_value)
            print(temp_values)
            for i in range(len(temp_values)):
                sql_str = "insert into dianlizhuangjirongliang (year,weight,country,country_iso3,weight_unit) values \
                                 ('%s','%s','%s','%s','%s')" % \
                          (temp_values[i]["year"], temp_values[i]["weight"], temp_values[i]["country"],\
                           temp_values[i]["country_iso3"], temp_values[i]["weight_unit"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
# 导入船舶轨迹数据
def test_import_excel10():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【8】AIS的传播轨迹数据_彭澎/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and row != 2 and col == 1:
                        temp_value["mmsi"] = str(value)
                    elif row != 1 and row != 2 and col == 2:
                        temp_value["lon"] = str(value)
                    elif row != 1 and row != 2 and col == 3:
                        temp_value["lat"] = str(value)
                    elif row != 1 and row != 2 and col == 4:
                        temp_value["time"] = str(value)
                if "mmsi" in temp_value.keys():
                    temp_values.append(temp_value)
            print(temp_values)
            for i in range(len(temp_values)):
                sql_str = "insert into chuanboguiji (mmsi,lon,lat,time) values \
                                 ('%s','%s','%s','%s')" % \
                          (temp_values[i]["mmsi"], temp_values[i]["lon"], temp_values[i]["lat"],\
                           temp_values[i]["time"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
# 导入油气并购数据
def test_import_excel11():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【4】能源投资并购_郭越/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[2])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if row != 1 and col == 1:
                        temp_value["time"] = str(value)
                    elif row != 1 and col == 2:
                        temp_value["acquiror_country"] = str(value)
                    elif row != 1 and col == 3:
                        temp_value["target_country"] = str(value)
                    elif row != 1 and col == 4:
                        temp_value["value"] = str(value)
                if "acquiror_country" in temp_value.keys() and temp_value["acquiror_country"] != None:
                    temp_value["value_unit"] = "EUR"
                    temp_values.append(temp_value)
            print(temp_values)
            for i in range(len(temp_values)):
                sql_str = "insert into youqibinggou (time,acquiror_country,target_country,value,value_unit) values \
                                 ('%s','%s','%s','%s','%s')" % \
                          (temp_values[i]["time"], temp_values[i]["acquiror_country"], temp_values[i]["target_country"],\
                           temp_values[i]["value"],temp_values[i]["value_unit"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
# 导入全球发电厂数据
def test_import_excel12():
    conn = pymysql.connect(
        host="192.168.84.130",
        port=3306,
        user="root",
        password="0",
        database="dilisuo",
        charset="utf8"
    )
    # 获取操作游标
    cursor = conn.cursor()
    dir_path = "D:/SuperMapDemo/地理所/【中科院】第二次数据对接20210430/【10】全球能源基础设施数据_何则&周彦楠/【1】全球发电厂数据/"
    # 获取所有文件名
    file_names = os.listdir(dir_path)
    for x in range(len(file_names)):
        if file_names[x].find("xlsx") != -1 and file_names[x].find("~$") == -1:
            temp_file_path = dir_path+file_names[x]
            file = load_workbook(temp_file_path)
            table = file.get_sheet_by_name(file.sheetnames[0])
            # 行数
            rows = table.max_row
            # 列数
            cols = table.max_column
            temp_values=[]
            for row in range(1,rows+1):
                temp_value = {}
                for col in range(1, cols + 1):
                    value = table.cell(row=row, column=col).value
                    if value == None:
                        value = ""
                    if row != 1 and row !=2 and col == 1:
                        temp_value["country_iso3"] = str(value)
                    elif row != 1 and row !=2 and col == 2:
                        temp_value["country"] = str(value)
                    elif row != 1 and row !=2 and col == 3:
                        temp_value["power_station_name"] = str(value)
                    elif row != 1 and row !=2 and col == 4:
                        temp_value["power_station_code"] = str(value)
                    elif row != 1 and row !=2 and col == 5:
                        temp_value["power_station_capacity"] = str(value)
                    elif row != 1 and row !=2 and col == 6:
                        temp_value["lat"] = str(value)
                    elif row != 1 and row !=2 and col == 7:
                        temp_value["lon"] = str(value)
                    elif row != 1 and row !=2 and col == 8:
                        temp_value["primary_fuel"] = str(value)
                    elif row != 1 and row !=2 and col == 9:
                        temp_value["other_fuel1"] = str(value)
                    elif row != 1 and row !=2 and col == 10:
                        temp_value["other_fuel2"] = str(value)
                    elif row != 1 and row !=2 and col == 11:
                        temp_value["other_fuel3"] = str(value)
                    elif row != 1 and row !=2 and col == 12:
                        temp_value["commissioning_year"] = str(value)
                    elif row != 1 and row !=2 and col == 13:
                        temp_value["owner"] = str(value)
                    elif row != 1 and row !=2 and col == 14:
                        temp_value["source"] = str(value)
                    elif row != 1 and row !=2 and col == 15:
                        temp_value["url"] = str(value)
                    elif row != 1 and row !=2 and col == 16:
                        temp_value["geolocation_source"] = str(value)
                    elif row != 1 and row !=2 and col == 17:
                        temp_value["wepp_id"] = str(value)
                    elif row != 1 and row !=2 and col == 18:
                        temp_value["year_of_capacity_data"] = str(value)
                    elif row != 1 and row !=2 and col == 19:
                        temp_value["generation_gwh_2013"] = str(value)
                    elif row != 1 and row !=2 and col == 20:
                        temp_value["generation_gwh_2014"] = str(value)
                    elif row != 1 and row !=2 and col == 21:
                        temp_value["generation_gwh_2015"] = str(value)
                    elif row != 1 and row !=2 and col == 22:
                        temp_value["generation_gwh_2016"] = str(value)
                    elif row != 1 and row !=2 and col == 23:
                        temp_value["generation_gwh_2017"] = str(value)
                    elif row != 1 and row !=2 and col == 24:
                        temp_value["estimated_generation_gwh"] = str(value)
                if "estimated_generation_gwh" in temp_value.keys():
                    temp_value["power_station_capacity_unit"] = "mw"
                    temp_values.append(temp_value)
            print(temp_values)
            for i in range(len(temp_values)):
                sql_str = "insert into fadianchang (country_iso3,country,power_station_name,power_station_code,\
                power_station_capacity,lat,lon,primary_fuel,other_fuel1,other_fuel2,other_fuel3,commissioning_year,\
                source,owner,url,geolocation_source,wepp_id,year_of_capacity_data,generation_gwh_2013,generation_gwh_2014,\
                generation_gwh_2015,generation_gwh_2016,generation_gwh_2017,estimated_generation_gwh,power_station_capacity_unit) values \
                ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                (temp_values[i]["country_iso3"], temp_values[i]["country"], temp_values[i]["power_station_name"],\
                temp_values[i]["power_station_code"],temp_values[i]["power_station_capacity"],temp_values[i]["lat"],\
                 temp_values[i]["lon"],temp_values[i]["primary_fuel"],temp_values[i]["other_fuel1"],temp_values[i]["other_fuel2"],\
                 temp_values[i]["other_fuel3"],temp_values[i]["commissioning_year"],temp_values[i]["source"],temp_values[i]["owner"],\
                 temp_values[i]["url"],temp_values[i]["geolocation_source"],temp_values[i]["wepp_id"],temp_values[i]["year_of_capacity_data"],\
                 temp_values[i]["generation_gwh_2013"],temp_values[i]["generation_gwh_2014"],temp_values[i]["generation_gwh_2015"],\
                 temp_values[i]["generation_gwh_2016"],temp_values[i]["generation_gwh_2017"],temp_values[i]["estimated_generation_gwh"],\
                 temp_values[i]["power_station_capacity_unit"])
                cursor.execute(sql_str)
                conn.commit()
            print(temp_file_path + "插入成功")
    conn.close()
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
    path = QFileDialog.getExistingDirectory(rans,"请选择保存路径","D:/")
    print(path)
def get_coordinate_trans(source,target):
    # 设置源数据坐标系
    source_coordinate = osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(source))
    # 设置目标坐标系为WGS84
    target_coordinate = osr.SpatialReference()
    target_coordinate.ImportFromEPSG(int(target))
    # 创建坐标转换对象
    transform = osr.CoordinateTransformation(source_coordinate, target_coordinate)
    return transform
def text_export():
    info = {'id': 'b84a4c46e6515a37ef8cdb8733838252', 'downType': '导出矢量', 'taskName': '444', 'savePath': 'D:/SuperMap DownLoad/临时', 'saveType': 'shp', 'type': 'point', 'coordinate': '4326', 'time': '2021/6/17 11:38:44', 'features': [[[39.232253141714914, 87.81173553467306]], [[36.87962060502676, 89.21821200009381]]], 'attributes': [{'name': '点图层', 'parentId': 'f5c033a0ae2629d6e918004520c43438', 'mydescribe': '用户自定义矢量标绘', 'index': 0}, {'name': '点图层', 'parentId': '625b487db14bfeeead3d3df705819e7b', 'mydescribe': '用户自定义矢量标绘', 'index': 1}]}
    file_path = os.path.join(info["savePath"],info["taskName"])
    coordinate = info["coordinate"]
    features = info["features"]
    atrributes = info["attributes"]
    transform = get_coordinate_trans("4326",coordinate)
    # 设置windows环境下识别中文
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
    if info["saveType"] == "csv":
        print()
    else:
        data_source = ""
        layer = ""
        if info["saveType"] == "shp":
            driver = ogr.GetDriverByName("ESRI Shapefile")
            data_source = driver.CreateDataSource(file_path + ".shp")
        elif info["saveType"] == "kml":
            driver = ogr.GetDriverByName("KML")
            data_source = driver.CreateDataSource(file_path + ".kml")
        # 设置坐标系
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(coordinate))
        if info["type"] == "point":
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
        # 获取空间对象类
        feature = ogr.Feature(layer.GetLayerDefn())
        # 设置要素属性字段
        for i in range(len(atrributes)):
            for key in atrributes[i]:
                if key != "parentId" and key != "index":
                    feature.SetField(key, str(atrributes[i][key]))

        for j in range(len(features)):
            # 插入空间对象
            if info["type"] == "point":
                # 坐标转换
                temp_feature = transform.TransformPoint(features[j][0][0], features[j][0][1])
                temp_tup = (temp_feature[0], temp_feature[1])
                wkt = "POINT(" + str(temp_tup[0]) +" "+ str(temp_tup[1]) + ")"
                point = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(point)
                layer.CreateFeature(feature)
            elif info["type"] == "line":
                wkt = "LINESTRING("
                for s in range(len(features[j])):
                    temp_feature = transform.TransformPoint(features[j][s][0], features[j][s][1])
                    temp_tup = (temp_feature[0], temp_feature[1])
                    if s == len(features[j])-1:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ")"
                    else:
                        wkt += str(temp_tup[0]) + " " + str(temp_tup[1]) + ","
                print(wkt)
                line = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(line)
                layer.CreateFeature(feature)
            elif info["type"] == "region":
                print(info)
                return False
                wkt = ""
                # 判断数组维数,4维则是多面类型
                if features[j].ndim == 4:
                    wkt = "MULTIPOLYGON(("
                # 判断数组维数,3维则是简单面类型
                elif features[j].ndim == 3:
                    wkt = "POLYGON("
                region = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(region)
                layer.CreateFeature(feature)
        # 关闭资源
        feature = None
        data_source = None
def get_list_dim(datas,index):
    try:
        if len(datas) !=0:
            index+=1
            print(index)
            get_list_dim(datas[0],index)
        else:
            print("结束")
    except TypeError:
        print("已到达末端")
    return index