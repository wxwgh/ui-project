# -- coding:utf-8 --
import iobjectspy
import os
import eel
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

# 进度条字典
progressDict = {}
#创建线程池
thread_pool = ThreadPoolExecutor(10)

#tif栅格数据投影转换相关
# 获取导入tif文件路径
def get_tif_path():
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
    path=QFileDialog.getOpenFileName(rans,"请选择要导入的文件","D:/","TIF (*.tif)")
    file_path=path[0]
    return file_path
def tif_coordinate_trans(info):
    # 进度条字典
    progress={}
    progress["id"]=info["id"]
    progress["progress"]=0
    progress["exportProgress"]=0
    import_file_path = info["import_file_path"]
    file_path=os.path.join(info["savePath"],info["taskName"])
    os.makedirs(file_path)
    source=info["source"]
    target=info["target"]
    # 首先，读取输入数据，然后获得输入数据的投影，放射变换参数，以及图像宽高等信息
    import_dataset=gdal.Open(import_file_path)
    progress["progress"]=100
    eel.updateTaskProgress(progress)
    # 设置源数据坐标系
    source_coordinate=osr.SpatialReference()
    source_coordinate.ImportFromEPSG(int(source))
    # 获取仿射变换6参数
    srs_trans=import_dataset.GetGeoTransform()
    # 获取图像宽
    x_size=import_dataset.RasterXSize
    # 获取图像高
    y_size=import_dataset.RasterYSize
    d_type=import_dataset.GetRasterBand(1).DataType
    # 设置目标坐标系
    target_coordinate=osr.SpatialReference()
    target_coordinate.ImportFromEPSG(int(target))
    tx=osr.CoordinateTransformation(source_coordinate,target_coordinate)
    # 计算输出图像四个角点的坐标
    (ulx,uly,_)=tx.TransformPoint(srs_trans[0],srs_trans[3])
    (urx,ury,_)=tx.TransformPoint(srs_trans[0]+srs_trans[1]*x_size,srs_trans[3])
    (llx,lly,_)=tx.TransformPoint(srs_trans[0],srs_trans[3]+srs_trans[5]*y_size)
    (lrx,lry,_)=tx.TransformPoint(srs_trans[0]+srs_trans[1]*x_size+srs_trans[2]*y_size,
                                  srs_trans[3]+srs_trans[4]*x_size+srs_trans[5]*y_size)

    min_x=min(ulx,urx,llx,lrx)
    max_x=max(ulx,urx,llx,lrx)
    min_y=min(uly,ury,lly,lry)
    max_y=max(uly,ury,lly,lry)

    # 创建输出图像，需要计算输出图像的尺寸（重投影以后图像的尺寸会发生变化）
    driver=gdal.GetDriverByName('GTiff')
    dst_ds=driver.Create(file_path+"/"+info["taskName"]+".tif",int((max_x-min_x)/450),int((max_y-min_y)/450),1,d_type)
    dst_trans=(min_x,450,srs_trans[2],max_y,srs_trans[4],-450)
    # 设置GeoTransform和Projection信息
    dst_ds.SetGeoTransform(dst_trans)
    dst_ds.SetProjection(target_coordinate.ExportToWkt())
    # 进行投影转换
    gdal.ReprojectImage(import_dataset,dst_ds,
                        source_coordinate.ExportToWkt(),target_coordinate.ExportToWkt(),
                        gdal.GRA_Bilinear)
    dst_ds.GetRasterBand(1).SetNoDataValue(0)  # 设置NoData值
    dst_ds.FlushCache()

    progress["exportProgress"]=100
    eel.updateTaskProgress(progress)
    del import_dataset
    del dst_ds


def analyze(info):
    if info["downType"] == "坐标转换":
        thread_pool.submit(coordinate_transition, info)

# 提取等值线
def get_contour_line(info):
    # 进度条字典x
    progressDict["id"] = info["id"]
    progressDict["type"] = "line"
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0
    # 存储路径
    save_path = os.path.join(info["savePath"], info["taskName"])
    # 创建目录
    os.makedirs(save_path)
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 导出文件路径
    file_name = info["taskName"] + "."+info["saveType"]
    file_path = os.path.join(save_path, file_name)
    # 导入文件类型
    import_type = info["url"].split(".",1)[1]
    # 导入文件路径
    import_path = info["url"]
    temp_dataset=""
    result=""
    if import_type == "IMG":
        result = iobjectspy.conversion.import_img(import_path,temp_udb,is_import_as_grid =True)
    elif import_type == "tif":
        result = iobjectspy.conversion.import_tif(import_path,temp_udb,is_import_as_grid =True)
    if result is not None:
        for item in result:
            if isinstance(item, str):
                temp_dataset = temp_udb.get_dataset(result[0])
            else:
                temp_dataset = temp_udb.get_dataset(result.name)
        line_dataset_vector = iobjectspy.analyst.grid_extract_isoline(temp_dataset, out_dataset_name=info["taskName"],
                                                                      interval=100, datum_value=0, resample_tolerance=0,
                                                                      smooth_method=None, smoothness=2,
                                                                      out_data=temp_udb, progress=analyze_progress)
        if line_dataset_vector:
            progressDict["progress"] = 100
            eel.updateTaskProgress(progressDict)
            # 根据格式参数选择导出方式
            if info["saveType"] == "shp":
                iobjectspy.conversion.export_to_shape(line_dataset_vector, file_path, progress=export_progress)
            elif info["saveType"] == "json":
                iobjectspy.conversion.export_to_geojson(line_dataset_vector, file_path, progress=export_progress)


# 提取等值面
def get_contour_polygon(info):
    # 进度条字典
    progressDict["id"] = info["id"]
    progressDict["type"] = "polygon"
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
    # 导入文件类型
    import_type = info["url"].split(".", 1)[1]
    # 导入文件路径
    import_path = info["url"]
    temp_dataset = ""
    result = ""
    if import_type == "IMG":
        result = iobjectspy.conversion.import_img(import_path, temp_udb, is_import_as_grid=True)
    elif import_type == "tif":
        result = iobjectspy.conversion.import_tif(import_path, temp_udb, is_import_as_grid=True)
    if result is not None:
        for item in result:
            if isinstance(item, str):
                temp_dataset = temp_udb.get_dataset(result[0])
            else:
                temp_dataset = temp_udb.get_dataset(result.name)
        polygon_dataset_vector = iobjectspy.analyst.grid_extract_isoregion(temp_dataset, out_dataset_name=info["taskName"],
                                                                      interval=100, datum_value=0, resample_tolerance=0,
                                                                      smooth_method=None, smoothness=2,
                                                                      out_data=temp_udb, progress=analyze_progress)
        if polygon_dataset_vector:
            progressDict["progress"] = 100
            eel.updateTaskProgress(progressDict)
            # 根据格式参数选择导出方式
            if info["saveType"] == "shp":
                iobjectspy.conversion.export_to_shape(polygon_dataset_vector, file_path, progress=export_progress)
            elif info["saveType"] == "json":
                iobjectspy.conversion.export_to_geojson(polygon_dataset_vector, file_path, progress=export_progress)

# 坐标转换
def coordinate_transition(info):
    # 进度条字典
    progressDict = {}
    progressDict["id"] = info["id"]
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0

    # 下载进度--导入进度--分析进度
    def import_progress(step_event):
        if step_event.percent <= 100:
            progressDict["progress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
        elif step_event.percent > 100:
            progressDict["progress"] = 100
            eel.updateTaskProgress(progressDict)

    # 导出进度
    def export_progress(step_event):
        if step_event.percent <= 100:
            progressDict["exportProgress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
        elif step_event.percent > 100:
            progressDict["exportProgress"] = 100
            eel.updateTaskProgress(progressDict)

    # 存储路径
    save_path = os.path.join(info["savePath"], info["taskName"])
    # 创建目录
    os.makedirs(save_path)
    # 创建内存数据源
    temp_udb = iobjectspy.data.create_datasource(":memory:")
    # 导出文件路径
    file_name = info["taskName"] + "." + info["saveType"]
    file_path = os.path.join(save_path, file_name)
    # 导入文件路径
    import_path = info["url"]
    result = iobjectspy.conversion.import_shape(import_path, temp_udb, progress=import_progress)
    temp_dataset = ""
    if result is not None:
        temp_dataset = temp_udb.get_dataset(result[0])
    # 创建datasetvector
    temp_vector = temp_udb.write_recordset(temp_dataset)
    print(info["coordinate"])
    prj_type=""
    if info["coordinate"] == "PCS_WGS_1984_UTM_49N":
        prj_type = iobjectspy.enums.PrjCoordSysType.PCS_WGS_1984_UTM_49N
    elif info["coordinate"] == "PCS_CHINA_2000_GK_13":
        prj_type = iobjectspy.enums.PrjCoordSysType.PCS_CHINA_2000_GK_13
    elif info["coordinate"] == "PCS_XIAN_1980_GK_13":
        prj_type = iobjectspy.enums.PrjCoordSysType.PCS_XIAN_1980_GK_13
    elif info["coordinate"] == "PCS_BEIJING_1954_GK_13":
        prj_type = iobjectspy.enums.PrjCoordSysType.PCS_BEIJING_1954_GK_13
    # 投影转换
    temp_result = iobjectspy.data.CoordSysTranslator.convert(temp_vector, iobjectspy.data.PrjCoordSys(
        prj_type), iobjectspy.data.CoordSysTransParameter(),coord_sys_trans_method=iobjectspy.enums.CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION,out_data=temp_udb)
    # 导出为shp
    iobjectspy.conversion.export_to_shape(temp_result, file_path, progress=export_progress)
# 坡度分析
def get_slope(info):
    # 进度条字典
    progressDict["id"] = info["id"]
    progressDict["type"] = "slope"
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
    # 导入文件类型
    import_type = info["url"].split(".", 1)[1]
    # 导入文件路径
    import_path = info["url"]
    temp_dataset = ""
    result = ""
    if import_type == "IMG":
        result = iobjectspy.conversion.import_img(import_path, temp_udb, is_import_as_grid=True,progress=analyze_progress)
    elif import_type == "tif":
        result = iobjectspy.conversion.import_tif(import_path, temp_udb, is_import_as_grid=True,progress=analyze_progress)
    if result is not None:
        temp_dataset = temp_udb.get_dataset(result[0])
    # 计算坡度
    slope_result = iobjectspy.analyst.calculate_slope(temp_dataset,iobjectspy.enums.SlopeType.DEGREE,0.00001,temp_udb)
    # 根据格式参数选择导出方式
    if info["saveType"] == "tif":
        iobjectspy.conversion.export_to_tif(slope_result, file_path, progress=export_progress)
    elif info["saveType"] == "img":
        iobjectspy.conversion.export_to_img(slope_result, file_path, progress=export_progress)
# 坡向分析
def get_aspect(info):
    # 进度条字典
    progressDict["id"] = info["id"]
    progressDict["type"] = "aspect"
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
    # 导入文件类型
    import_type = info["url"].split(".", 1)[1]
    # 导入文件路径
    import_path = info["url"]
    temp_dataset = ""
    result = ""
    if import_type == "IMG":
        result = iobjectspy.conversion.import_img(import_path, temp_udb, is_import_as_grid=True,
                                                  progress=analyze_progress)
    elif import_type == "tif":
        result = iobjectspy.conversion.import_tif(import_path, temp_udb, is_import_as_grid=True,
                                                  progress=analyze_progress)
    if result is not None:
        temp_dataset = temp_udb.get_dataset(result[0])
    # 计算坡度
    slope_result = iobjectspy.analyst.calculate_aspect(temp_dataset,temp_udb)
    # 根据格式参数选择导出方式
    if info["saveType"] == "tif":
        iobjectspy.conversion.export_to_tif(slope_result, file_path, progress=export_progress)
    elif info["saveType"] == "img":
        iobjectspy.conversion.export_to_img(slope_result, file_path, progress=export_progress)
def analyze_progress(step_event):
    if progressDict["type"] == "line":
        if step_event.percent <= 100:
            progressDict["progress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
    elif progressDict["type"] == "polygon":
        if step_event.title == "正在创建网络拓扑关系...":
            if step_event.percent <= 100:
                progressDict["progress"] = step_event.percent
                eel.updateTaskProgress(progressDict)
    elif progressDict["type"] == "coordinate":
        if step_event.percent <= 100:
            progressDict["progress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
    elif progressDict["type"] == "slope":
        if step_event.percent <= 100:
            progressDict["progress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
    elif progressDict["type"] == "aspect":
        if step_event.percent <= 100:
            progressDict["progress"] = step_event.percent
            eel.updateTaskProgress(progressDict)
def export_progress(step_event):
    if step_event.percent <= 100:
        progressDict["exportProgress"] = step_event.percent
        eel.updateTaskProgress(progressDict)