# -- coding:utf-8 --
import overpass
import math
import requests
import shutil
import os
from contextlib import closing
import iobjectspy
import json
import time

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
test()