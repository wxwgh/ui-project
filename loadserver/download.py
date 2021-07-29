#线程池
from concurrent.futures import ThreadPoolExecutor
import os
import eel
import math
from PIL import Image
import shutil
import requests
from requests.adapters import HTTPAdapter
import json
from contextlib import closing
import sys
proj_str = os.path.dirname(sys.argv[0])+'/proj'
os.environ['PROJ_LIB'] = proj_str
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

#创建线程池
thread_pool = ThreadPoolExecutor(5)

def tile_load(info):
    # 开启线程
    thread_pool.submit(map_load, info)
# 影像下载
def map_load(info):
    # 地图名称
    map_name = info["map_name"]
    print(map_name)
    # 是否边界剪裁
    tile_is_clip=info["tile_is_clip"]
    # 是否拼接
    is_joint=info["is_joint"]
    # 获取数组级别
    zooms=info["zoom"]
    #进度条字典
    progress={}
    progress["id"]=info["id"]
    progress["progress"]=0
    progress["exportProgress"]=0
    # 下载范围
    scope=info["scope"]
    # 下载总数
    total=info["total"]
    # 当前下载瓦片数量
    tileIndex=0
    # 代理
    proxies={"http":None,"https":None}
    # eel.updateTaskProgress(progress)
    features=scope["features"]
    file_paths=[]
    # 循环多面
    for i in range(len(features)):
        # 单个面路径
        polygon_path = ""
        if features[i]["properties"]["id"] != "自绘多边形" and features[i]["properties"]["id"] != "导入多边形" and features[i]["properties"]["id"] != "行政区划面":
            polygon_path = info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]
        elif len(features) >1 :
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]+str(i)
        elif len(features) == 1 :
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]
        print(polygon_path)
        # 创建面对象
        polygon=ogr.CreateGeometryFromJson(json.dumps(features[i]["geometry"]))
        # 获取元素范围
        bounds = polygon.GetEnvelope()
        # 获取左上角点
        north_west = {
            "lat":bounds[3],
            "lng":bounds[0]
        }
        # 获取右下角
        south_east = {
            "lat":bounds[2],
            "lng":bounds[1]
        }
        # 根据zoom下载散列瓦片
        for j in range(len(zooms)):
            resolution =""
            tile1=""
            tile2=""
            if map_name == "百度地图":
                resolution = get_resolution_baidu(north_west,zooms[j])
                # 通过左上 级别获取瓦片范围
                tile1 = eel.lat_lng_to_tile_baidu(north_west["lat"],north_west["lng"],zooms[j])()
                # 通过右下 级别获取瓦片范围
                tile2 = eel.lat_lng_to_tile_baidu(south_east["lat"], south_east["lng"], zooms[j])()
            else:
                resolution =get_resolution_gaode(north_west,zooms[j])
                # 通过左上 级别获取瓦片范围
                tile1 = eel.lat_lng_to_tile_gaode(north_west["lat"], north_west["lng"], zooms[j])()
                # 通过右下 级别获取瓦片范围
                tile2 = eel.lat_lng_to_tile_gaode(south_east["lat"], south_east["lng"], zooms[j])()
            temp_info={
                "url":polygon_path+"/"+str(zooms[j]),
                "north_west":north_west,
                "resolution":resolution,
                "zoom":zooms[j]
            }
            file_paths.append(temp_info)
            minX =tile1["tileX"] if(tile1["tileX"]<tile2["tileX"]) else tile2["tileX"]
            maxX = tile1["tileX"] if (tile1["tileX"]>tile2["tileX"]) else tile2["tileX"]
            minY = tile1["tileY"] if (tile1["tileY"]<tile2["tileY"]) else tile2["tileY"]
            maxY = tile1["tileY"] if (tile1["tileY"]>tile2["tileY"]) else tile2["tileY"]
            while minX<=maxX:
                x_path = polygon_path+"/"+str(zooms[j])+"/"+str(minX)
                os.makedirs(x_path)
                index=minY
                while index<=maxY:
                    y_path = x_path +"/"+str(index)+".png"
                    print(y_path)
                    url=info["url"].replace("{z}",str(zooms[j])).replace("{x}",str(minX)).replace("{y}",str(index))
                    print(url)
                    x = 0
                    while x < 1000000:
                        try:
                            result=requests.get(url,stream=True,proxies=proxies,timeout=10)
                            with open(y_path,'wb') as f:
                                f.write(result.content)
                                tileIndex+=1
                                temp_progress=math.floor((tileIndex/total)*100)
                                progress["progress"]=temp_progress
                                eel.updateTaskProgress(progress)
                                f.close()
                            index+=1
                            break
                        except requests.exceptions.RequestException as e:
                            x+=1
                minX+=1
    print(file_paths)
    # 是否拼接大图
    # if is_joint == "拼接大图":
    #     # 根据不同的地图 进行相应的拼接方式
    #     if map_name == "百度地图":
    #         pass
    #     else:
    #         # 遍历文件地址集合
    #         for s in len(file_paths):
    #             for root,dirs,files in os.walk(file_paths[s]):
    #                 for dir in dirs:
    #                     print(dir)
    #
    #     # 是否按边界剪裁 如果为true则进行剪裁
    #     if tile_is_clip:
    #         pass
    #     else:
    #         pass
    # elif is_joint == "原始瓦片":
    #     progress["exportProgress"]=100
    #     eel.updateTaskProgress(progress)
    #     print("原始瓦片导出成功")


# 获取高德,谷歌,OSM分辨率
def get_resolution_gaode(north_west,level):
    num = math.pow(2, level)
    resolution=6378137.0*2*math.pi*math.cos(north_west["lat"])/256/num
    return resolution
# 获取百度分辨率
def get_resolution_baidu(north_west,level):
    resolution = math.pow(2, (18 - level)) * math.cos(north_west["lat"])
    return resolution
# 经纬度坐标转高德,谷歌,OSM瓦片坐标
def lat_lng_to_tile_gaode(lat,lng,level):
    # 某一瓦片等级下瓦片地图X轴(Y轴)上的瓦片数目
    tile_num = math.pow(2,level)

    # 经度转瓦片坐标x
    x = (lng+180)/360
    tile_x = math.floor(x * tile_num)
    # 纬度转瓦片坐标y
    lat_rad=lat*math.pi/180
    y=(1-math.log(math.tan(lat_rad)+1/math.cos(lat_rad))/math.pi)/2
    tile_y = math.floor(y*tile_num)
    return {
        "tile_x":tile_x,
        "tile_y":tile_y
    }
def map_load_joint2(info):
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
        #获取图片总宽度和高度
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
def map_load2(info):
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
                                f.close()
                            index+=1
                        minX+=1

    progressDict["exportProgress"] = 100
    eel.updateTaskProgress(progressDict)

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
