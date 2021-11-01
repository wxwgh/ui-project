#线程池
from concurrent.futures import ThreadPoolExecutor
import os
import eel
import math
import PIL
from PIL import Image
import numpy as np
import shutil
import requests
from natsort import natsorted
import imghdr
import random
# from urllib import request
# import urllib.request
import json
import sys
proj_str = os.path.dirname(sys.argv[0])+'/proj'
os.environ['PROJ_LIB'] = proj_str
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

#创建线程池
thread_pool = ThreadPoolExecutor(5)

# 当前运行的线程集合
thread_list={}

# 停止线程
def stop_thread(id):
    global thread_list
    thread_list[id]=False
# 开启新线程
def start_thread(info):
    global thread_list
    thread_list[info["id"]] = True
    if info["downType"].find("影像下载")!=-1:
        thread_pool.submit(map_load, info)
    elif info["downType"].find("高程下载")!=-1:
        thread_pool.submit(dem_load,info)
def tile_load(info):
    global thread_list
    thread_list[info["id"]] = True
    if info["downType"].find("影像下载")!=-1:
        thread_pool.submit(map_load, info)
    elif info["downType"].find("高程下载")!=-1:
        thread_pool.submit(dem_load,info)
# 影像下载
def map_load(info):
    global thread_list
    # 获取瓦片地址信息
    file_paths=info["file_paths"]
    # 多记录面标识
    multirecord_flag = info["multirecord_flag"]
    # 地图名称
    map_name = info["map_name"]
    print(map_name)
    # 是否边界剪裁
    tile_is_clip=info["tile_is_clip"]
    # 是否拼接
    is_joint=info["is_joint"]
    print(is_joint)
    # 获取数组级别
    zooms=info["zoom"]
    #进度条字典
    progress={}
    progress["id"]=info["id"]
    progress["progress"]=0
    progress["exportProgress"]=0
    progress["file_paths"]=[]
    # 下载范围
    scope=info["scope"]
    # 下载总数
    total=info["total"]
    # 当前下载瓦片数量
    from_index=info["from_index"]
    # 断点续传标识
    break_flag = info["break_flag"]
    # 代理
    proxies={"http":None,"https":None}
    features=scope["features"]
    # 循环多记录面
    tile_index=0
    for i in range(len(features)):
        # 单个面路径
        polygon_path = ""
        if multirecord_flag:
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]+str(i)
        else:
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]
        # 创建面对象
        polygon=ogr.CreateGeometryFromJson(json.dumps(features[i]["geometry"]))
        # 获取元素范围
        bounds = polygon.GetEnvelope()
        print(bounds)
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
        # 获取左下角
        south_west = {
            "lat": bounds[2],
            "lng": bounds[0]
        }
        # 根据zoom下载散列瓦片
        for j in range(len(zooms)):
            resolution =""
            tile1=""
            tile2=""
            if map_name == "百度地图":
                resolution = get_resolution_gaode(north_west,zooms[j])
                # 通过左上 级别获取瓦片范围
                tile1 = eel.lat_lng_to_tile_baidu(north_west["lat"],north_west["lng"],zooms[j])()
                # 通过右下 级别获取瓦片范围
                tile2 = eel.lat_lng_to_tile_baidu(south_east["lat"], south_east["lng"], zooms[j])()
            elif map_name == "腾讯地图":
                resolution = get_resolution_gaode(north_west, zooms[j])
                # 通过左上 级别获取瓦片范围
                tile1 = eel.lat_lng_to_tile_tencent(north_west["lat"], north_west["lng"], zooms[j])()
                # 通过右下 级别获取瓦片范围
                tile2 = eel.lat_lng_to_tile_tencent(south_east["lat"], south_east["lng"], zooms[j])()
            else:
                resolution =get_resolution_gaode(north_west,zooms[j])
                # 通过左上 级别获取瓦片范围
                tile1 = eel.lat_lng_to_tile_gaode(north_west["lat"], north_west["lng"], zooms[j])()
                # 通过右下 级别获取瓦片范围
                tile2 = eel.lat_lng_to_tile_gaode(south_east["lat"], south_east["lng"], zooms[j])()
            temp_info={
                "url":polygon_path+"/"+str(zooms[j]),
                "south_west":south_west,
                "resolution":resolution,
                "zoom":zooms[j]
            }
            temp_flag=True
            for t in range(len(file_paths)):
                if file_paths[t]["url"] == temp_info["url"]:
                    temp_flag=False
            if temp_flag:
                file_paths.append(temp_info)
            minX =tile1["tileX"] if(tile1["tileX"]<tile2["tileX"]) else tile2["tileX"]
            maxX = tile1["tileX"] if (tile1["tileX"]>tile2["tileX"]) else tile2["tileX"]
            minY = tile1["tileY"] if (tile1["tileY"]<tile2["tileY"]) else tile2["tileY"]
            maxY = tile1["tileY"] if (tile1["tileY"]>tile2["tileY"]) else tile2["tileY"]
            num = (maxX - minX + 1) * (maxY - minY + 1)
            print("瓦片总数:"+str(num))
            while minX<=maxX:
                x_path = polygon_path+"/"+str(zooms[j])+"/"+str(minX)
                # 判断文件夹是否存在
                file_flag = os.path.exists(x_path)
                if file_flag==False:
                    os.makedirs(x_path)
                index=minY
                while index<=maxY:
                    tile_index += 1
                    # 判断是否是断点续传任务
                    if break_flag==True:
                        if from_index !=0:
                            # 判断当前瓦片计数 是否小于等于 当前下载数量
                            if tile_index <= from_index:
                                index+=1
                                # 当前瓦片已下载
                                continue
                            else:
                                # 此节点未下载,从此处开始下载
                                break_flag=False
                    y_path = x_path +"/"+str(index)+".png"
                    url=""
                    if map_name == "必应地图":
                        # 获取四叉数编码
                        bing_key = eel.lat_lng_to_quadkey_bing(index,minX,zooms[j])()
                        url = info["url"].replace("{quadkey}",str(bing_key))
                    else:
                        url=info["url"].replace("{z}",str(zooms[j])).replace("{x}",str(minX)).replace("{y}",str(index))
                    print(url)
                    x = 0
                    while x < 1000000:
                        try:
                            # 判断线程是否中断
                            if thread_list[info["id"]] == False:
                                print("线程中断")
                                return False
                            # result=requests.get(url,stream=True,proxies=proxies,timeout=10)
                            temp_image=""
                            if map_name == "天地图":
                                # 使用随机请求头
                                temp_header={
                                    'Accept':'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                                    'Accept-Encoding':'gzip, deflate',
                                    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
                                    'Connection':'keep-alive',
                                    'Host':'t3.tianditu.gov.cn',
                                    'Referer':'http://localhost:8080/',
                                    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
                                }
                                temp_image = Image.open(requests.get(url,headers=temp_header,stream=True,proxies=proxies,timeout=10).raw)
                                resizedImage = temp_image.resize((256, 256), PIL.Image.ANTIALIAS)
                            elif map_name.find("自定义")!=-1:
                                temp_image = requests.get(url, stream=True, proxies=proxies, timeout=10)
                            else:
                                temp_image = Image.open(requests.get(url, stream=True, proxies=proxies, timeout=10).raw)
                                resizedImage = temp_image.resize((256, 256),PIL.Image.ANTIALIAS)
                            with open(y_path,'wb') as f:
                                if map_name.find("自定义")!=-1:
                                    f.write(temp_image.content)
                                else:
                                    resizedImage.save(y_path, quality=95)
                                from_index+=1
                                temp_progress=math.floor((from_index/total)*100)
                                progress["progress"]=temp_progress
                                progress["from_index"]=from_index
                                progress["file_paths"]=file_paths
                                eel.updateTaskProgress(progress)
                                f.close()
                            index+=1
                            break
                        except Exception as e:
                            print(e)
                            x+=1
                minX+=1
    # 是否拼接大图
    joint_index=0
    if is_joint == "拼接大图":
        # 遍历文件地址集合
        for s in range(len(file_paths)):
            new_image_path = file_paths[s]["url"] + "/" + str(file_paths[s]["zoom"]) + ".jpg"
            new_tif_path = file_paths[s]["url"] + "/" + str(file_paths[s]["zoom"]) + ".tif"
            new_image_prj = file_paths[s]["url"] + "/" + str(file_paths[s]["zoom"]) + ".prj"
            new_image_tfw = file_paths[s]["url"] + "/" + str(file_paths[s]["zoom"])+ ".jgw"
            resolution = file_paths[s]["resolution"]
            # north_west_mi = lnglat_to_Mercator(file_paths[s]["north_west"])
            south_west_mi = file_paths[s]["south_west"]
            images = []
            # 获取瓦片拼接存储地址
            for item in natsorted(os.listdir(file_paths[s]["url"])):
                temp_images = []
                if os.path.isdir(file_paths[s]["url"] + "/" + item):
                    # 文件按名称排序(数字名称)
                    temp_files = natsorted(os.listdir(file_paths[s]["url"] + "/" + item))
                    # temp_files.sort(key=lambda q: int(q.split('.png')[0]))
                    for item2 in temp_files:
                        image_content = Image.open(file_paths[s]["url"] + "/" + item + "/" + item2)
                        print(file_paths[s]["url"] + "/" + item + "/" + item2)
                        temp_images.append(image_content)
                        joint_index += 1
                        export_progress = math.floor((joint_index / total) * 100)
                        progress["exportProgress"] = export_progress
                        eel.updateTaskProgress(progress)
                    # 根据不同的地图 进行相应的拼接方式
                    if map_name == "百度地图" or map_name =="腾讯地图":
                        temp_images.reverse()
                    images.append(temp_images)
            # 获取图片总宽度和高度
            total_width = len(images) * 256
            total_height = len(images[0]) * 256
            new_image = Image.new("RGB", (total_width, total_height))
            for f in range(len(images)):
                # x偏移量
                x_off = f * 256
                for c in range(len(images[f])):
                    # y偏移量
                    y_off = c * 256
                    new_image.paste(images[f][c], (x_off, y_off))
            # 参数quality将影响图片质量95为最好质量
            new_image.save(new_image_path, quality=95)
            # 创建tfw文件 用于标识tif的位置
            fd = open(new_image_tfw, mode="w", encoding="utf-8")
            # 写入x方向 像素分辨率
            fd.write(str(resolution) + '\r')
            # 写入平移量
            fd.write('0.0000000000\r')
            # 写入旋转角度
            fd.write('0.0000000000\r')
            # 写入y方向 像素分辨率
            fd.write(str(resolution) + '\r')
            # 写入图像左下角x坐标
            fd.write(str(south_west_mi["lng"]) + '\r')
            # 写入图像左下角y坐标
            fd.write(str(south_west_mi["lat"]) + '\r')
            fd.close()

            # 生成坐标系文件
            # 创建prj文件 用于标识tif的位置
            prj = open(new_image_prj, mode="w", encoding="utf-8")
            # 坐标系字符串
            # prj.write(
            #     'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"]]')
            prj.write('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],AUTHORITY["EPSG","4326"]]')
            prj.close()
            driver = gdal.GetDriverByName('GTiff')
            in_ds = gdal.Open(new_image_path)
            #  获取仿射矩阵信息,投影信息
            im_geotrans = in_ds.GetGeoTransform()
            # print(im_geotrans)
            im_proj = in_ds.GetProjection()
            data_width = in_ds.RasterXSize
            data_height = in_ds.RasterYSize
            im_data = in_ds.ReadAsArray(0, 0, data_width, data_height)
            if 'int8' in im_data.dtype.name:
                datatype = gdal.GDT_Byte
            elif 'int16' in im_data.dtype.name:
                datatype = gdal.GDT_UInt16
            else:
                datatype = gdal.GDT_Float32
            if len(im_data.shape) == 2:
                im_data = np.array([im_data])
            im_bands, im_height, im_width = im_data.shape
            # 创建tif文件
            out_ds = driver.Create(new_tif_path, im_width, im_height, im_bands, datatype)
            out_ds.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
            out_ds.SetProjection(im_proj)  # 写入投影
            for c in range(im_bands):
                out_ds.GetRasterBand(c + 1).WriteArray(im_data[c])
            # 是否按边界剪裁 如果为true则进行剪裁
            if tile_is_clip:
                pass
            else:
                pass
    elif is_joint == "原始瓦片":
        progress["exportProgress"]=100
        eel.updateTaskProgress(progress)
        print("原始瓦片导出成功")

# 高德,谷歌,OSM经纬度转墨卡托坐标系
def lnglat_to_Mercator(north_west):
    lng = north_west["lng"]*20037508.34/180
    temp_lat = math.log(math.tan((90 + north_west["lat"]) * math.pi / 360)) / (math.pi / 180)
    lat = temp_lat * 20037508.34 / 180
    return {
        "lng":lng,
        "lat":lat
    }
# 获取分辨率 采用国际180度切片方案 原点:-180,90 dpi:96 size:256
def get_resolution_gaode(north_west,level):
    resolution=""
    if int(level) == 0:
        resolution = 0.703125000000001
    elif int(level) == 1:
        resolution = 0.351562500000001
    elif int(level) == 2:
        resolution = 0.17578125
    elif int(level) == 3:
        resolution = 8.78906250000002E-02
    elif int(level) == 4:
        resolution = 4.39453125000001E-02
    elif int(level) == 5:
        resolution = 0.02197265625
    elif int(level) == 6:
        resolution = 0.010986328125
    elif int(level) == 7:
        resolution = 5.49316406250001E-03
    elif int(level) == 8:
        resolution = 0.00274658203125
    elif int(level) == 9:
        resolution = 0.001373291015625
    elif int(level) == 10:
        resolution = 6.86645507812501E-04
    elif int(level) == 11:
        resolution = 3.43322753906251E-04
    elif int(level) == 12:
        resolution = 1.71661376953125E-04
    elif int(level) == 13:
        resolution = 8.58306884765626E-05
    elif int(level) == 14:
        resolution = 4.29153442382813E-05
    elif int(level) == 15:
        resolution = 2.14576721191407E-05
    elif int(level) == 16:
        resolution = 1.07288360595703E-05
    elif int(level) == 17:
        resolution = 5.36441802978517E-06
    elif int(level) == 18:
        resolution = 2.68220901489258E-06
    elif int(level) == 19:
        resolution = 1.34110450744629E-06
    return resolution
def get_resolution_gaode2(north_west,level):
    num = math.pow(2, int(level))
    resolution=6378137.0*2*math.pi*math.cos(north_west["lat"])/256/num
    return resolution
# 获取百度分辨率
def get_resolution_baidu(north_west,level):
    resolution = math.pow(2, (18 - level)) * math.cos(north_west["lat"])
    return resolution


# 高程下载
def dem_load(info):
    global thread_list
    print('高程下载')
    # 存储路径
    save_path = os.path.join(info["savePath"], info["taskName"])
    # 多记录面标识
    multirecord_flag = info["multirecord_flag"]
    # 进度条字典
    progress = {}
    progress["id"] = info["id"]
    progress["progress"] = 0
    progress["exportProgress"] = 0
    # 下载范围
    scope = info["scope"]
    # 下载总数
    total = info["total"]
    print("瓦片总数:" + str(total))
    # 当前下载瓦片数量
    from_index = info["from_index"]
    # 断点续传标识
    break_flag = info["break_flag"]
    # 代理
    proxies = {"http": None, "https": None}
    features = scope["features"]
    # 循环多记录面
    tile_index = 0
    for i in range(len(features)):
        # 单个面路径
        polygon_path = ""
        if multirecord_flag:
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]+str(i)
        else:
            polygon_path=info["savePath"]+"/"+info["taskName"]+"/"+features[i]["properties"]["id"]
        # 判断文件夹是否存在
        file_flag = os.path.exists(polygon_path)
        if file_flag == False:
            # 创建目录
            os.makedirs(polygon_path)
        # 创建面对象
        polygon=ogr.CreateGeometryFromJson(json.dumps(features[i]["geometry"]))
        # 获取元素范围
        bounds = polygon.GetEnvelope()
        minX = math.floor(bounds[0])
        minY = math.floor(bounds[2])
        maxX = math.floor(bounds[1])
        maxY = math.floor(bounds[3])
        while minX <= maxX:
            index = minY
            while index <= maxY:
                tile_index += 1
                # 判断是否是断点续传任务
                if break_flag == True:
                    if from_index != 0:
                        # 判断当前瓦片计数 是否小于等于 当前下载数量
                        if tile_index <= from_index:
                            index += 1
                            # 当前瓦片已下载
                            continue
                        else:
                            # 此节点未下载,从此处开始下载
                            break_flag = False
                file_path = polygon_path + "/"+"N"+str(index)+"E"+str(minX)+".IMG"
                print(file_path)
                url = info["url"]+"/"+"N"+str(index)+"E"+str(minX)+".IMG"
                print(url)
                # 判断线程是否中断
                if thread_list[info["id"]] == False:
                    print('线程已终止')
                    return False
                x = 0
                while x < 1000000:
                    try:
                        result = requests.get(url, stream=True, proxies=proxies, timeout=10)
                        with open(file_path, 'wb') as f:
                            f.write(result.content)
                            from_index += 1
                            temp_progress = math.floor((from_index / total) * 100)
                            progress["progress"] = temp_progress
                            progress["from_index"] = from_index
                            eel.updateTaskProgress(progress)
                            f.close()
                        index += 1
                        break
                    except requests.exceptions.RequestException as e:
                        x += 1
            minX += 1
    progress["exportProgress"] = 100
    eel.updateTaskProgress(progress)
    print('导出成功')
# 老版高程下载
def dem_load22(info):
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
