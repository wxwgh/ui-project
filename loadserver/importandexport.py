# -- coding:utf-8 --
import iobjectspy
import os
import eel
import json
import math
import py4j.java_collections

# 进度条字典
progressDict = {}
def get_features(info):
    # 创建内存数据源s
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 导入文件路径
    import_path = info["url"]
    result = iobjectspy.conversion.import_shape(import_path, temp_udb)
    temp_dataset = ""
    if result is not None:
        temp_dataset = temp_udb.get_dataset(result[0])
    # 创建datasetvector
    temp_vector = temp_udb.write_recordset(temp_dataset)
    # 投影转换
    temp_result = iobjectspy.data.CoordSysTranslator.convert(temp_vector, iobjectspy.data.PrjCoordSys(
        prj_type="GCS_WGS_1984"), iobjectspy.data.CoordSysTransParameter(),
                                                             coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,
                                                             out_data=temp_udb)

    # 获取空间数据
    temp_features = temp_result.get_features()
    # 需传递的数据
    datas={}
    datas["features"]=[]
    for i in range(len(temp_features)):
        temp_feature={}
        temp_feature["attribute"]={}
        # 获取属性x
        temp_field = temp_features[i].get_values(True, True)
        # 获取空间对象
        temp_geometry = temp_features[i].geometry
        #空间数据类型
        temp_type = temp_geometry.type
        if temp_type == 1:
            datas["type"] ="Point"
        elif temp_type ==3:
            datas["type"] = "Line"
        elif temp_type ==5:
            datas["type"] = "Region"
        # 空间对象转json
        temp_json = temp_geometry.to_json()
        print(temp_json)
        temp_feature["geojson"]=temp_json
        # dictkeys转list
        temp_keys = list(temp_field.keys())
        for j in range(len(temp_keys)):
            temp_feature["attribute"][temp_keys[j]] = temp_field[temp_keys[j]]
        datas["features"].append(temp_feature)
    return datas
def export_shape(info):
    # 进度条字典
    progressDict["id"] = info["id"]
    progressDict["type"] = "export"
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0
    # 存储路径
    save_path = os.path.join(info["savePath"], info["taskName"])
    # 创建目录
    os.makedirs(save_path)
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 导出文件路径
    file_name = info["taskName"] + "." + info["saveType"]
    file_path = os.path.join(save_path, file_name)
    # 获取数据集类型
    dataset_type=""
    if info["type"] == "Point":
        dataset_type="POINT"
    elif info["type"] == "marker":
        dataset_type = "POINT"
    elif info["type"] == "Line":
        dataset_type="LINE"
    elif info["type"] == "Region":
        dataset_type="REGION"
    # 创建数据集类
    temp_vector = temp_udb.create_vector_dataset("exportVector", dataset_type, False)
    # 获取字段及值信息
    temp_attribute = info["geometrys"][0]["attribute"]
    temp_keys = list(temp_attribute.keys())
    # 创建字段
    # 字段信息类
    temp_list = []
    for j in range(len(temp_keys)):
        temp_info = iobjectspy.data.FieldInfo(temp_keys[j], "TEXT", max_length=None, default_value=None,caption=None,is_required=False,is_zero_length_allowed=True)
        temp_list.append(temp_info)
    temp_vector.create_fields(temp_list)

    addIndex=0
    temp_geometrys = info["geometrys"]
    for i in range(len(temp_geometrys)):
        geometry_json = temp_geometrys[i]["geojson"]
        geometry_attribute = temp_geometrys[i]["attribute"]
        # 创建geometry
        temp_geometry = iobjectspy.data.Geometry.from_json(geometry_json)
        temp_feature = iobjectspy.data.Feature(temp_geometry, geometry_attribute, temp_attribute["id"], temp_list)
        # 在数据集类中追加数据
        temp_vector.append(temp_feature)
        addIndex += 1
        temp_progress = math.floor((addIndex / len(temp_geometrys)) * 100)
        progressDict["progress"] = temp_progress
        eel.updateTaskProgress(progressDict)
    # 投影转换
    temp_result = iobjectspy.data.CoordSysTranslator.convert(temp_vector, iobjectspy.data.PrjCoordSys(
        prj_type=info["coordinate"]), iobjectspy.data.CoordSysTransParameter(),
                                                             coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,
                                                             out_data=temp_udb)
    # 根据格式参数选择导出方式x
    if info["saveType"] == "shp":
        iobjectspy.conversion.export_to_shape(temp_result, file_path, progress=export_progress)
    elif info["saveType"] == "json":
        iobjectspy.conversion.export_to_geojson(temp_result, file_path, progress=export_progress)

def export_progress(step_event):
    if step_event.percent <= 100:
        progressDict["exportProgress"] = step_event.percent
        eel.updateTaskProgress(progressDict)