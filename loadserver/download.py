#线程池
from concurrent.futures import ThreadPoolExecutor
import os
import eel
import math
from PIL import Image
import shutil
import requests
from contextlib import closing

#创建线程池
thread_pool = ThreadPoolExecutor(10)

def down_load(info):
    if info["downType"].find("瓦片下载") != -1:
        # 是否拼接标识xx
        isJoint = info["isJoint"]
        if isJoint:
            # 线程池开启线程
            thread_pool.submit(map_load_joint, info)
        else:
            thread_pool.submit(map_load, info)
    elif info["downType"].find("高程下载") != -1:
        thread_pool.submit(dem_load, info)

# 瓦片下载
def tile_load(info):
    # 是否拼接标识xx
    isJoint = info["isJoint"]
    if isJoint:
        # 线程池开启线程
        thread_pool.submit(map_load_joint,info)
    else:
        thread_pool.submit(map_load,info)

def map_load_joint(info):
    # 获取级别数组x
    zooms = info["zoom"]
    #进度条字典
    progressDict = {}
    progressDict["id"] = info["id"]
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0
    # 范围
    scope = info["scope"]
    # 下载总数
    total = info["total"]
    #获取左上坐标
    northWest = info["northWest"]
    # 分辨率数组
    resolutions = info["resolution"]
    # 当前下载瓦片数量
    tileIndex = 0
    for j in range(len(zooms)):
        # 内存图片数组
        images = []
        # 获取分辨率
        resolution = resolutions[j]
        # 获取存储路径
        path = os.path.join(info["savePath"], info["taskName"],str(zooms[j]))
        os.makedirs(path)
        tempStr = str(zooms[j]) + "." + info["saveType"]
        tfw_temp_str = str(zooms[j]) + ".tfw"
        prj_temp_str=str(zooms[j]) + ".prj"
        filePath = os.path.join(path, tempStr)
        tfwPath = os.path.join(path,tfw_temp_str)
        prjPath = os.path.join(path,prj_temp_str)
        for i in range(len(scope)):
            for key in scope[i]:
                if int(key) == zooms[j]:
                    temp = scope[i][key]
                    minX = temp["minX"]
                    minY = temp["minY"]
                    maxX = temp["maxX"]
                    maxY = temp["maxY"]
                    while minX <= maxX:
                        index = minY
                        temp_image=[]
                        while index <= maxY:
                            urlPath = info["url"].replace("{z}", str(zooms[j])).replace("{x}", str(minX)).replace("{y}",str(index))
                            imageContent = Image.open(requests.get(urlPath, stream=True).raw)
                            temp_image.append(imageContent)
                            tileIndex += 1
                            tempProgress = math.floor((tileIndex / total) * 100)
                            progressDict["progress"] = tempProgress
                            eel.updateTaskProgress(progressDict)
                            index += 1
                        minX += 1
                        images.append(temp_image)
        # # 获取图片总宽度和高度
        total_width=len(images)*256
        total_height = len(images[0]) * 256
        new_image = Image.new("RGB",(total_width, total_height))
        joinIndex=0
        for s in range(len(images)):
            # x偏移量
            x_off = s*256
            for c in range(len(images[s])):
                #y偏移量
                y_off=c*256
                new_image.paste(images[s][c], (x_off, y_off))
                joinIndex+=1
                temp_exportProgress = math.floor((joinIndex / total) * 100)
                progressDict["exportProgress"] = temp_exportProgress
                eel.updateTaskProgress(progressDict)
        # 参数quality将影响图片质量95为最好质量
        new_image.save(filePath,quality=95)
        # 创建tfw文件 用于标识tif的位置
        fd = open(tfwPath,mode="w",encoding="utf-8")
        # 写入x方向 像素分辨率
        fd.write(str(resolution)+'\r')
        # 写入平移量
        fd.write('0.0000000000\r')
        # 写入旋转角度
        fd.write('0.0000000000\r')
        # 写入y方向 像素分辨率
        fd.write("-"+str(resolution)+'\r')
        # 写入图像左上角x坐标
        fd.write(str(northWest["x"])+'\r')
        # 写入图像左上角y坐标
        fd.write(str(northWest["y"])+'\r')
        fd.close()

        # 生成坐标系文件
        # 创建prj文件 用于标识tif的位置
        prj = open(prjPath, mode="w", encoding="utf-8")
        # 坐标系字符串
        prj.write('PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"]]')
        prj.close()
# 瓦片下载
def map_load(info):
    # 获取级别数组
    zooms = info["zoom"]
    scope =info["scope"]
    total=info["total"]
    tileIndex=0
    progressDict={}
    progressDict["id"]=info["id"]
    progressDict["progress"]=0
    progressDict["exportProgress"]=0
    for j in range(len(zooms)):
        for i in range(len(scope)):
            for key in scope[i]:
                if int(key) == zooms[j]:
                    temp = scope[i][key]
                    minX = temp["minX"]
                    minY = temp["minY"]
                    maxX = temp["maxX"]
                    maxY = temp["maxY"]
                    while minX <= maxX:
                        path = os.path.join(info["savePath"],info["taskName"],str(zooms[j]),str(minX))
                        os.makedirs(path)
                        index=minY
                        while index <= maxY:
                            tempStr = str(index)+"."+info["saveType"]
                            filePath = os.path.join(path,tempStr)
                            urlPath = info["url"].replace("{z}",str(zooms[j])).replace("{x}",str(minX)).replace("{y}",str(index))
                            imageContent = requests.get(urlPath,stream=True)
                            with open(filePath,'wb') as f:
                                f.write(imageContent.content)
                                tileIndex+=1
                                temp_progress=math.floor((tileIndex/total)*100)
                                progressDict["progress"]=temp_progress
                                eel.updateTaskProgress(progressDict)
                                if temp_progress == 100:
                                    progressDict["exportProgress"] = 100
                                    eel.updateTaskProgress(progressDict)
                                f.close()
                            index+=1
                        minX+=1

    progressDict["exportProgress"] = 100
    eel.updateTaskProgress(progressDict)

#矢量下载
# def vector_load(info):
#     progressDict = {}
#     progressDict["id"] = info["id"]
#     progressDict["progress"] = 0
#     progressDict["exportProgress"] = 0
#     progressDict["message"] = ""
#
#     # 下载进度--导入进度--分析进度
#     def import_progress(step_event):
#         if step_event.message == "正往数据集里添加记录...":
#             if step_event.percent <= 100:
#                 print(step_event.message)
#                 progressDict["progress"] = step_event.percent
#                 eel.updateTaskProgress(progressDict)
#             elif step_event.percent > 100:
#                 progressDict["progress"] = 100
#                 eel.updateTaskProgress(progressDict)
#     # 导出进度
#     def export_progress(step_event):
#         if step_event.percent <= 100:
#             progressDict["exportProgress"] = step_event.percent
#             eel.updateTaskProgress(progressDict)
#         elif step_event.percent > 100:
#             progressDict["exportProgress"] = 100
#             eel.updateTaskProgress(progressDict)
#     # 存储目录
#     save_dir = os.path.join(info["savePath"],info["taskName"])
#     file_dir = Path(save_dir)
#     if file_dir.is_dir():
#         print(info["dataset_name"]+"目录已存在")
#     else:
#         # 创建目录
#         os.makedirs(save_dir)
#     # 下载地址
#     url = info["url"]
#     dataset_name = info["dataset_name"]
#     temp_str = dataset_name + "." + info["saveType"]
#     # 保存文件路径
#     file_path = os.path.join(save_dir, temp_str)
#     # 连接信息
#     connectInfo = iobjectspy.data.DatasourceConnectionInfo(url)
#     # 打开数据源
#     data_source = iobjectspy.data.Datasource.open(connectInfo)
#     # 创建内存数据源
#     temp_udb = iobjectspy.data.create_datasource(":memory:")
#     print(info["scope"])
#     dataset_overlay = iobjectspy.data.Geometry.from_json(info["scope"])
#     # 获取数据集
#     dataset = data_source.get_dataset(dataset_name)
#     # 叠加分析-矢量剪裁
#     try:
#         result_vector = iobjectspy.analyst.overlay(dataset,[dataset_overlay] , iobjectspy.enums.OverlayMode.CLIP,
#                                                    out_data=temp_udb, out_dataset_name=dataset_name, progress=import_progress)
#     except:
#         # 返回错误信息
#         progressDict["message"]=info["downType"]+"矢量数据下载失败,该范围下载无数据"
#         eel.updateTaskProgress(progressDict)
#     else:
#         # 导出文件
#         iobjectspy.conversion.export_to_shape(result_vector, file_path, progress=export_progress)
# 老版本互联网矢量下载
def vector_load2(info):
    progressDict = {}
    progressDict["id"] = info["id"]
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0
    # 存储路径
    path = os.path.join(info["savePath"],info["taskName"])
    # 创建目录
    os.makedirs(path)
    temp_str = info["taskName"]+"."+info["saveType"]
    file_path = os.path.join(path,temp_str)
    # 下载地址
    url=info["url"]
    # 文件总大小
    total=0
    with closing(requests.get(url, stream=True)) as response:
        # chunk_size参数表示一次请求的最大值
        for data in response.iter_content(chunk_size=1024):
            total += len(data)
    joinIndex=0
    with closing(requests.get(url, stream=True)) as response_down:
        with open(file_path, "wb") as f:
            for data_down in response_down.iter_content(chunk_size=1024):
                joinIndex+=len(data_down)
                temp_progress = math.floor((joinIndex/total) * 100)
                progressDict["progress"] = temp_progress
                eel.updateTaskProgress(progressDict)
                if temp_progress == 100:
                    progressDict["exportProgress"] = 100
                    eel.updateTaskProgress(progressDict)
                f.write(data_down)
# 高程下载
def dem_load(info):
    # dem文件地址
    url = "./dem"
    # 存储路径
    save_path = os.path.join(info["savePath"], info["taskName"])
    # 创建目录
    os.makedirs(save_path)
    minLng = int(info["scopeLngLat"]["minLng"])
    minLat = int(info["scopeLngLat"]["minLat"])
    maxLng = int(info["scopeLngLat"]["maxLng"])
    maxLat = int(info["scopeLngLat"]["maxLat"])
    # 列出文件夹下所有的目录与文件
    list = os.listdir(url)
    # 获取文件总数
    total=0
    progressDict = {}
    progressDict["id"] = info["id"]
    progressDict["progress"] = 0
    progressDict["exportProgress"] = 0
    for i in range(len(list)):
        # 获取文件地址
        path = os.path.join(url, list[i])
        # 判断是否是文件并且后缀为img
        if os.path.isfile(path) and os.path.splitext(path)[1] in ['.IMG']:
            # 获取经度
            fileLng = int(os.path.splitext(list[i])[0].split("E", 1)[1])
            # 获取纬度
            fileLat = int(os.path.splitext(list[i])[0].split("E", 1)[0].split("N", 1)[1])
            if fileLng >= minLng and fileLng <= maxLng:
                if fileLat >= minLat and fileLat <= maxLat:
                    total+=1
                    shutil.copy(path, save_path)
    down_index=0
    for j in range(len(list)):
        # 获取文件地址
        path = os.path.join(url, list[j])
        # 判断是否是文件并且后缀为img
        if os.path.isfile(path) and os.path.splitext(path)[1] in ['.IMG']:
            # 获取经度
            fileLng = int(os.path.splitext(list[j])[0].split("E", 1)[1])
            # 获取纬度
            fileLat = int(os.path.splitext(list[j])[0].split("E", 1)[0].split("N", 1)[1])
            if fileLng >= minLng and fileLng <= maxLng:
                if fileLat >= minLat and fileLat <= maxLat:
                    shutil.copy(path, save_path)
                    down_index+=1
                    temp_progress = math.floor((down_index / total) * 100)
                    progressDict["progress"] = temp_progress
                    eel.updateTaskProgress(progressDict)
                    if temp_progress == 100:
                        progressDict["exportProgress"] = 100
                        eel.updateTaskProgress(progressDict)
