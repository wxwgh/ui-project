# -- coding:utf-8 --
import os
import eel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

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

# 等值线分析
def isoline_analyze():
    pass
