# -- coding:utf-8 --
import os
import eel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
proj_str = os.path.dirname(sys.argv[0])+'/proj'
os.environ['PROJ_LIB'] = proj_str
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import numpy as np

# 获取导入tif文件路径
def get_tif_path():
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
    path = QFileDialog.getOpenFileName(rans, "请选择要导入的文件", "D:/", "Tif (*.tif);;IMG (*.IMG);")
    file_path = path[0]
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

# 等值线分析
def isoline_analyze(info):
    # 进度条字典
    progress = {}
    progress["id"] = info["id"]
    progress["progress"] = 0
    progress["exportProgress"] = 0
    progress["progress"] = 100
    eel.updateTaskProgress(progress)
    ogr.RegisterAll()
    import_file_path = info["import_file_path"]
    catalog_path = info["savePath"] + "/" + info["taskName"]
    # 判断文件夹是否存在
    file_flag = os.path.exists(catalog_path)
    if file_flag == False:
        os.makedirs(catalog_path)
    # 设置windows环境下识别中文
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
    in_ds = gdal.Open(import_file_path)
    data_width = in_ds.RasterXSize
    data_height = in_ds.RasterYSize
    data_count = in_ds.RasterCount
    # 读取图像数据波段
    data_band  = in_ds.GetRasterBand(1)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # 文件地址
    file_path = catalog_path + "/" + info["taskName"] + ".shp"
    data_source = driver.CreateDataSource(file_path)
    # 设置坐标系
    # srs = osr.SpatialReference()
    srs = in_ds.GetSpatialRef()
    # srs.ImportFromEPSG(4326)
    # 创建layer
    layer = data_source.CreateLayer(info["taskName"], srs, ogr.wkbLineString)
    # 设置表头字段
    field_name2 = ogr.FieldDefn("demid", ogr.OFTInteger)
    field_name2.SetWidth(30)
    layer.CreateField(field_name2)
    field_name = ogr.FieldDefn("elevation", ogr.OFTInteger)
    field_name.SetWidth(30)
    layer.CreateField(field_name)
    '''
    第一个参数为 图层波段
    第二个参数为 等高线间距
    第三个参数为 等高线起始高度
    第四个参数为 一组固定高度值,如果不为空 则 等高线间距 和 等高线起始高度 设置 将不起作用
    第五个参数为 是否使用无效值 False不使用 True使用
    第六个参数为 如果使用无效值,则生成等高线时,会忽略原无效值,并使用该数值
    第七个参数为 矢量图层
    第八个参数为 指定列号 id号会保留在指定属性字段 列号从0开始
    第九个参数为 指定列号 高程值会保留在指定属性字段 列号从0开始
    第十个参数为
    第十一个参数为
    '''
    temp_count = gdal.ContourGenerate(data_band, 50, 0, [], False, 0, layer, 0, 1)

    in_ds = None
    del in_ds

    data_source = None
    del data_source

    progress["exportProgress"] = 100
    eel.updateTaskProgress(progress)
# 等值面分析
def contour_analyze(info):
    pass
# 坡度分析
def slope_analyze(info):
    # 进度条字典
    progress = {}
    progress["id"] = info["id"]
    progress["progress"] = 0
    progress["exportProgress"] = 0
    progress["progress"] = 100
    eel.updateTaskProgress(progress)
    import_file_path = info["import_file_path"]
    catalog_path = info["savePath"]+"/"+info["taskName"]
    # 判断文件夹是否存在
    file_flag = os.path.exists(catalog_path)
    if file_flag == False:
        os.makedirs(catalog_path)
    #文件地址
    file_path = catalog_path+"/"+info["taskName"]+".tif"
    # 计算坡度
    slope = gdal.DEMProcessing(file_path,import_file_path,"slope")
    progress["exportProgress"] = 100
    eel.updateTaskProgress(progress)
# 坡向分析
def aspect_analyze(info):
    # 进度条字典
    progress = {}
    progress["id"] = info["id"]
    progress["progress"] = 0
    progress["exportProgress"] = 0
    progress["progress"] = 100
    eel.updateTaskProgress(progress)
    import_file_path = info["import_file_path"]
    catalog_path = info["savePath"] + "/" + info["taskName"]
    # 判断文件夹是否存在
    file_flag = os.path.exists(catalog_path)
    if file_flag == False:
        os.makedirs(catalog_path)
    # 文件地址
    file_path = catalog_path + "/" + info["taskName"] + ".tif"
    # 计算坡度
    aspect = gdal.DEMProcessing(file_path, import_file_path, "aspect",format='GTiff',trigonometric=0, zeroForFlat=1)
    progress["exportProgress"] = 100
    eel.updateTaskProgress(progress)