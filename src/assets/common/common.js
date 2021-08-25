import $store from '@/store/index.js';
//引入坐标转换工具
var transform = require('tile-lnglat-transform');
//引入turf
import * as turf from '@turf/turf';
export default{
	UUID(){
		function S4() {
			return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
		}
					
		return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4())
	},
	unbindMapEvent(map){
		map.off("mousedown");
		map.off("mousemove");
		map.off("contextmenu");
	},
	switchMouseStyle(flag,map){
		var $this = this;
		if(flag){
			L.DomUtil.setClass(map._container,'mapCursor');
		}else{
			L.DomUtil.setClass(map._container,'mapUnCursor');
		}
	},
	mouseOver(post){
		post.isShow=true;
	},
	mouseLeave(post){
		post.isShow=false;
	},
	// 清除分幅图层
	clear_show_set_layer(){
		for(let i=0;i<$store.state.show_set.grid_layer.length;i++){
			$store.state.show_set.grid_layer[i].remove();
		}
		$store.state.show_set.grid_layer.splice(0,$store.state.show_set.grid_layer.length);
		//清空geojson
		$store.state.show_set.grid_geojson="";
		$store.state.show_set.zoom="";
	},
	clearScope(){
		$store.state.scopeInfo.isXZQH="";
		$store.state.scopeInfo.adcode="";
		for(let i=0;i<$store.state.scopeInfo.scopeLayer.length;i++){
			$store.state.scopeInfo.scopeLayer[i].remove();
		}
		$store.state.scopeInfo.scopeLayer.splice(0,$store.state.scopeInfo.scopeLayer.length);
	},
	// 清除测量结果
	clear_measure(){
		var layers = $store.state.measure_layers;
		if(layers.length>0){
			for(let i=0;i<layers.length;i++){
				layers[i].remove();
			}
			layers=[];
		}
	},
	// 隐藏删除所有图层管理器中的图层
	clear_layers(){
		var layers = $store.state.layerGroups[0].children;
		for(let i=0;i<layers.length;i++){
			layers[i].isSelect=false;
			layers[i].icon="fa fa-eye";
			for(let j=0;j<layers[i].children.length;j++){
				if(layers[i].children[j].isSelect){
					layers[i].children[j].isSelect=false;
					layers[i].children[j].icon="fa fa-eye";
					if(layers[i].children[j].layer){
						layers[i].children[j].layer.remove();
					}
				}
			}
		}
	},
	updateLayerName(name){
		var tempData = $store.state.layerGroups[0].children;
		var option_value = $store.state.layerSelectInfo.option_value;
		for(let j=0;j<tempData.length;j++){
			if(tempData[j].label===option_value){
				tempData[j].label=name;
			}
		}
	},
	createLayer(option){
		if(option.index==="2"){
			$store.state.layerGroups[0].children.push(option);
		}else if(option.index==="3"){
			for(let i=0;i<$store.state.layerGroups[0].children.length;i++){
				if($store.state.layerGroups[0].children[i].id===option.parentId){
					$store.state.layerGroups[0].children[i].children.push(option);
					$store.state.layerGroups[0].children[i].count=parseInt($store.state.layerGroups[0].children[i].count)+1;
				}
			}
		}
	},
	deleteLayer(data){
		if(data.index==="2"){
			var tempData = $store.state.layerGroups[0].children;
			for(let i=0;i<tempData.length;i++){
				if(data.id===tempData[i].id){
					for(let j=0;j<tempData[i].children.length;j++){
						if(tempData[i].children[j].layer){
							tempData[i].children[j].layer.remove();
						}
					}
					tempData.splice(i,1);
				}
			}
			//清空图层选中列表
			var options = $store.state.layerSelectInfo.options;
			for(let i=0;i<options.length;i++){
				if(options[i].label===data.label){
					options.splice(i,1);
				}
			}
		}else if(data.index==="3"){
			var tempData = $store.state.layerGroups[0].children;
			for(let i=0;i<tempData.length;i++){
				for(let j=0;j<tempData[i].children.length;j++){
					if(data.id===tempData[i].children[j].id){
						if(tempData[i].children[j].layer){
							tempData[i].children[j].layer.remove();
						}
						tempData[i].children.splice(j,1);
						tempData[i].count-=1;
					}
				}
			}
		}
	},
	//创建marker
	createMarker(latlng,value){
		var map = this.getMap();
		var myIcon = L.icon({
		    iconUrl: require('../../assets/marker/marker-icon.png'),
		    shadowUrl: require('../../assets/marker/marker-shadow.png'),
			iconSize: [25, 41],
			iconAnchor: [12, 41],
			popupAnchor: [1, -34],
			shadowSize: [41, 41],
		});
		var marker = L.marker(latlng, {icon: myIcon}).addTo(map);
		var popup = L.popup({autoClose:true,closeOnClick:true}).setLatLng(latlng).setContent(value);
		marker.on("mouseover",function(){
			$(".leaflet-interactive").css("cursor","pointer");
		})
		marker.on("mouseout",function(){
			$(".leaflet-interactive").css("cursor","");
		})
		marker.bindPopup(popup);
		return marker;
	},
	update_scopeInfo(flag,adcode,layers,geojson){
		$store.state.scopeInfo.isXZQH=flag;
		if(adcode){
			$store.state.scopeInfo.adcode=adcode;
		}
		for(let i=0;i<layers.length;i++){
			$store.state.scopeInfo.scopeLayer.push(layers[i]);
		}
		if(geojson){
			$store.state.scopeInfo.geojson = geojson;
		}
	},
	//清空表格
	clearDownLoadTableAndScope(){
		$store.state.downloadTableDatas.splice(0,$store.state.downloadTableDatas.length);
	},
	//更新下载信息
	updateDownLoadInfo(data){
		if(data.activeName==="1"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType=$store.state.downloadInfo.mapName+"瓦片下载";
			$store.state.downloadInfo.taskName=data.tileNameInput;
			$store.state.downloadInfo.savePath=data.tileDownInput;
			$store.state.downloadInfo.saveType=data.tileOptionValue;
			$store.state.downloadInfo.isJoint=data.tileChecked;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.activeName==="2"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="dem高程下载";
			$store.state.downloadInfo.taskName=data.demNameInput;
			$store.state.downloadInfo.savePath=data.demDownInput;
			$store.state.downloadInfo.saveType=data.demOptionValue;
			$store.state.downloadInfo.url="../dem";
			$store.state.downloadInfo.time=this.getDate();
		}
	},
	getDate(){
		var time=new Date().getFullYear() +"/" + (new Date().getMonth()+1)+"/"+new Date().getDate()+" "+new Date().getHours() +":"+ new Date().getMinutes()+":"+new Date().getSeconds();
		return time;
	},
	//更新下载表格
	updateDownLoadTable(){
		//清空表格
		this.clearDownLoadTableAndScope();
		// 获取比例尺数组和dpi
		var scale=[];
		var dpi="";
		for(let i=0;i<$store.state.mapList.length;i++){
			if($store.state.mapList[i].isShow){
				scale=$store.state.mapList[i].scale;
				dpi=$store.state.mapList[i].dpi;
			}
		}
		var layers = $store.state.scopeInfo.scopeLayer;
		var bounds = "";
		if(layers.length>1){
			for(let i=0;i<layers.length;i++){
				if(i===0){
					bounds = layers[i].getBounds();
				}else{
					bounds = bounds.extend(layers[i].getBounds());
				}
			}
		}else{
			bounds = layers[0].getBounds();
		}
		
		$store.state.downloadInfo.scopeLngLat={
			minLng:parseInt(bounds.getWest()),
			minLat:parseInt(bounds.getSouth()),
			maxLng:parseInt(bounds.getEast()),
			maxLat:parseInt(bounds.getNorth()),
		}
		//西北 左上
		var northWest = bounds.getNorthWest();
		$store.state.downloadInfo.northWest = this.latLngToMercator(northWest);
		//西南 左下
		var southWest = bounds.getSouthWest();
		//东北 右上
		var northEast = bounds.getNorthEast();
		//获取级别范围
		var minZoom = "";
		var maxZoom="";
		var mapList = $store.state.mapList;
		for(let i=0;i<mapList.length;i++){
			if(mapList[i].isShow){
				for(let j=0;j<mapList[i].urls.length;j++){
					if(mapList[i].urls[j].isActive){
						minZoom=mapList[i].urls[j].minZoom;
						maxZoom=mapList[i].urls[j].maxZoom;
					}
				}
			}
		}
		for(let i=minZoom;i<maxZoom+1;i++){
			var tile1 = this.latLngToTile(southWest,i);
			var tile2 = this.latLngToTile(northEast,i);
			var minX = tile1.tileX<tile2.tileX?tile1.tileX:tile2.tileX;
			var maxX = tile1.tileX>tile2.tileX?tile1.tileX:tile2.tileX;
			var minY = tile1.tileY<tile2.tileY?tile1.tileY:tile2.tileY;
			var maxY = tile1.tileY>tile2.tileY?tile1.tileY:tile2.tileY;
			//获取瓦片总数
			var num = (maxX-minX+1)*(maxY-minY+1);
			//获取瓦片大小
			var temp = num*30;
			var downsize="";
			if(temp<1024){
				downsize = temp+"KB";
			}else if(temp >= 1024 && temp < 1048576){
				downsize = (temp/1024).toFixed(2)+"MB";
			}else if (temp >= 1048576 && temp < 1073741824){
				downsize = (temp/1024/1024).toFixed(2)+"GB";
			}else{
				downsize = (temp/1024/1024/1024).toFixed(2)+"T";
			}
			var tableData = {
				level:i,
				scale:scale[i],
				resolution:(0.0254*parseInt(scale[i].split(":")[1])/dpi).toFixed(2)+"米",
				total:num,
				downsize:downsize,
				dpi:dpi,
				progress_info:{
					//级别
					z:i,
					//列号
					x:minX,
					//行号
					y:minY,
				},
			};
			var tempScope={}
			tempScope[i]={
				minX:minX,
				minY:minY,
				maxX:maxX,
				maxY:maxY
			}
			$store.state.downloadInfo.scope.push(tempScope);
			$store.state.downloadTableDatas.push(tableData);
		}
	},
	// 高德,谷歌,OSM经纬度转瓦片坐标
	lat_lng_to_tile_gaode(lat,lng,level){
		var TileLnglatTransformGaode = transform.TileLnglatTransformGaode;
		console.log(TileLnglatTransformGaode);
		var data = TileLnglatTransformGaode.lnglatToTile(lng,lat,level);
		console.log(data);
		return data;
	},
	//百度经纬度转瓦片坐标
	lat_lng_to_tile_baidu(lat,lng,level){
		var TileLnglatTransformBaidu = transform.TileLnglatTransformBaidu;
		var data = TileLnglatTransformBaidu.lnglatToTile(lng,lat,level);
		return data;
	},
	latLngToTile(latLng,level){
		var TileLnglatTransformGaode = transform.TileLnglatTransformGaode;
		var data = TileLnglatTransformGaode.lnglatToTile(latLng.lng,latLng.lat,level);
		return data;
	},
	latLngToMercator(latLng) {
		var mercator = {
			x: 0,
			y: 0
		};
		var x = latLng.lng * 20037508.34 / 180;
		var y = Math.log(Math.tan((90 + latLng.lat) * Math.PI / 360)) / (Math.PI / 180);
		y = y * 20037508.34 / 180;
		mercator.x = x;
		mercator.y = y;
		return mercator;
	},	
	//设置当前图层节点 全部选中
	setOperation(layer_name){
		var layerGroup = $store.state.layerGroups[0].children;
		for(let i=0;i<layerGroup.length;i++){
			if(layerGroup[i].label===layer_name){
				for(let j=0;j<layerGroup[i].children.length;j++){
					layerGroup[i].children[j].isOperation=true;
					if(layerGroup[i].children[j].type==="marker"&&layerGroup[i].children[j].layer){
						var myIcon = L.icon({
						    iconUrl: require('../../assets/marker/marker-icon-blue.png'),
						    shadowUrl: require('../../assets/marker/marker-shadow.png'),
							iconSize: [25, 41],
							iconAnchor: [12, 41],
							popupAnchor: [1, -34],
							shadowSize: [41, 41],
						});
						layerGroup[i].children[j].layer.setIcon(myIcon);
					}else if(layerGroup[i].children[j].type==="point"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({radius: 1,color:'blue',weight:1});
					}else if(layerGroup[i].children[j].type==="line"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'blue',weight:1});
					}else if(layerGroup[i].children[j].type==="region"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'blue',weight:1});
					}
				}
			}
		}
	},
	//清除选中
	clearOperation(){
		var layerGroup = $store.state.layerGroups[0].children;
		for(let i=0;i<layerGroup.length;i++){
			for(let j=0;j<layerGroup[i].children.length;j++){
				if(layerGroup[i].children[j].isOperation){
					layerGroup[i].children[j].isOperation=false;
					if(layerGroup[i].children[j].type==="marker"&&layerGroup[i].children[j].layer){
						var myIcon = L.icon({
						    iconUrl: require('../../assets/marker/marker-icon.png'),
						    shadowUrl: require('../../assets/marker/marker-shadow.png'),
							iconSize: [25, 41],
							iconAnchor: [12, 41],
							popupAnchor: [1, -34],
							shadowSize: [41, 41],
						});
						layerGroup[i].children[j].layer.setIcon(myIcon);
					}else if(layerGroup[i].children[j].type==="point"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({radius: 1,color:'red',weight:1});
					}else if(layerGroup[i].children[j].type==="line"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'red',weight:1});
					}else if(layerGroup[i].children[j].type==="region"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'red',weight:1});
					}
				}
			}
		}
	},
	//判断是否有选中对象
	isOperationSelect(){
		var layerGroup = $store.state.layerGroups[0].children;
		var flag=false;
		for(let i=0;i<layerGroup.length;i++){
			for(let j=0;j<layerGroup[i].children.length;j++){
				if(layerGroup[i].children[j].isOperation){
					flag=true;
				}
			}
		}
		return flag;
	},
	//定位函数
	setLocation(center,zoom){
		var map = this.getMap();
		map.setView(center,zoom);
	},
	//创建点
	createPoint(points){
		var map = this.getMap();
		var layer = L.circle(points[0], {radius: 1,color:'red',weight:1}).addTo(map);
		return layer;
	},
	//创建线
	createLine(points){
		var map = this.getMap();
		var layer = L.polyline(points, {color: "red",weight:1}).addTo(map);
		return layer;
	},
	//创建面
	createPolygon(points){
		var map = this.getMap();
		var polygon = L.polygon(points,{color:'red',weight:1}).addTo(map);
		return polygon;
	},
	//设置单个矢量 表数据
	setAttributeData(data){
		var temp_datas = $store.state.attributeTable;
		temp_datas.push(data);
	},
	//设置图层 表数据
	setAllAttributeData(name){
		var datas = $store.state.layerGroups[0].children;
		var temp_datas = $store.state.attributeTable;
		for(let i=0;i<datas.length;i++){
			if(name===datas[i].label){
				for(let j=0;j<datas[i].children.length;j++){
					temp_datas.push(datas[i].children[j].attribute);
				}
			}
		}
		//更新表头
		this.update_attribute_header();
	},
	//清空属性表数据
	clearAttributeTable(){
		$store.state.attributeTable.splice(0,$store.state.attributeTable.length);
	},
	// 更新表头
	update_attribute_header(){
		$store.state.attributeHeader.splice(0,$store.state.attributeHeader.length);
		var option_value = $store.state.layerSelectInfo.option_value;
		var temp_datas = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_datas.length;i++){
			if(temp_datas[i].label===option_value){
				for(let j=0;j<temp_datas[i].table_header.length;j++){
					$store.state.attributeHeader.push(temp_datas[i].table_header[j]);
				}
			}
		}
	},
	//添加至选中图层列表
	add_select_layer(data){
		var temp={
			value:data.label,
			label:data.label,
			type:data.type
		}
		$store.state.layerSelectInfo.type=data.type;
		$store.state.layerSelectInfo.option_value=data.label;
		$store.state.layerSelectInfo.options.push(temp);
	},
	//更新选中图层
	update_select_layer(data){
		$store.state.layerSelectInfo.option_value=data.label;
		$store.state.layerSelectInfo.type=data.type;
		$store.state.layerSelectInfo.coordinate = data.coordinate;
	},
	//清空选中图层列表
	clear_select_layer(){
		$store.state.layerSelectInfo.option_value="";
		$store.state.layerSelectInfo.type="";
		$store.state.layerSelectInfo.options=[];
	},
	//清空选取图层列表
	clear_operation_list(){
		$store.state.layerOperationInfo.option_value="";
		$store.state.layerOperationInfo.type="";
		$store.state.layerOperationInfo.options=[];
	},
	//更新选取图层列表
	update_operation_list(names){
		//设置选中
		$store.state.layerOperationInfo.option_value=names[0].label;
		$store.state.layerOperationInfo.type=names[0].type;
		//设置列表
		for(let i=0;i<names.length;i++){
			var temp={};
			temp.label=names[i].label;
			temp.value=names[i].label;
			temp.type=names[i].type;
			$store.state.layerOperationInfo.options.push(temp);
		}
	},
	//打开属性表
	openAttributeTable(){
		$(".el-tabs__item").each(function(){
			if($(this).text()==="属性表"){
				$(this).trigger("click");
			}
		});
	},
	//获取map
	getMap(){
		var map = $store.state.map_container.map;
		return map;
	},
	//获取图层
	getLayer(){
		var layer = $store.state.map_container.layer;
		return layer;
	},
	//更新地图类型
	updateMapType(type){
		for(let i=0;i<$store.state.mapContainer.length;i++){
			if($store.state.mapContainer[i].type===type){
				$store.state.mapContainer[i].isShow=true;
			}else{
				$store.state.mapContainer[i].isShow=false;
			}
		}
	},
	updateLayer(layer){
		for(let i=0;i<$store.state.mapContainer.length;i++){
			if($store.state.mapContainer[i].isShow){
				$store.state.mapContainer[i].layer=layer;
			}
		}
	},
	//设置地图级别
	setMapZoom(){
		var map = this.getMap();
		var mapList = $store.state.mapList;
		var minZoom="";
		var maxZoom="";
		for(let i=0;i<mapList.length;i++){
			if(mapList[i].isShow){
				for(let j=0;j<mapList[i].urls.length;j++){
					if(mapList[i].urls[j].isActive){
						minZoom=mapList[i].urls[j].minZoom;
						maxZoom=mapList[i].urls[j].maxZoom;
					}
				}
			}
		}
		map.setMinZoom(minZoom);
		map.setMaxZoom(maxZoom);
	},
	updateTaskTableDatas(data){
		var id = $store.state.downLoadTableId;
		//更新下载任务表全局字典
		$store.state.taskTableDatas.push(data);
		//下载任务添加入缓存
		this.addIndexedDB(id,data);
		
	},
	deleteTaskTableDatas(data){
		var tableData = $store.state.taskTableDatas;
		var id = $store.state.downLoadTableId;
		for(let i=0;i<tableData.length;i++){
			if(data.id===tableData[i].id){
				tableData.splice(i,1);
				//删除缓存
				this.deleteIndexedDB(id,data);
			}
		}
	},
	openTaskTable(){
		$(".el-tabs__item").each(function(){
			if($(this).text()==="下载任务"){
				$(this).trigger("click");
			}
		});
	},
	deleteIndexedDB(id,data){
		var request = indexedDB.open("download",1);
		//成功回调函数
		request.onsuccess = function(e) {
			var db = e.target.result;
			//创建一个事务对象 指定表名 和操作模式
			var trans = db.transaction(id,"readwrite");
			//获取表格对象
			var store = trans.objectStore(id);
			//获取游标对象
			var objCursor = store.openCursor();
			objCursor.onsuccess = function(e){
				var cursor = e.target.result;
				if(cursor){
					if(cursor.value.id===data.id){
						store.delete(cursor.key);
					}
					cursor.continue();
				}else{
					db.close();
				}
			}
		};
	},
	//获取用户许可时间
	get_user_time(id,name){
		//打开一个数据库 并指定名称
		var request = indexedDB.open("download",1);
		//成功回调函数
		request.onsuccess = function(e) {
			var db = e.target.result;
			//创建一个事务对象 指定表名 和操作模式
			var trans = db.transaction(id,"readwrite");
			//获取表格对象
			var store = trans.objectStore(id);
			//获取游标对象
			var objCursor = store.openCursor();
			objCursor.onsuccess = function(e){
				var cursor = e.target.result;
				if(cursor){
					if(cursor.value.name===name){
						$store.state.administratorInfo.time= cursor.value.time;
						$store.state.administratorInfo.describe=cursor.value.describe;
						$store.state.administratorInfo.isAdmin=cursor.value.isAdmin;
					}
					cursor.continue();
				}
			}
			db.close();
		};
	},
	addIndexedDB(id,data){
		var request = indexedDB.open("download",1);
		//成功回调函数
		request.onsuccess = function(e) {
			var db = e.target.result;
			//创建一个事务对象 指定表名 和操作模式
			var trans = db.transaction(id,"readwrite");
			//获取表格对象
			var store = trans.objectStore(id);
			store.add(data);
			db.close();
		};
	},
	//更新下载进度
	updateProgress(id,progress){
		var tableDatas= $store.state.taskTableDatas;
		for(let i=0;i<tableDatas.length;i++){
			if(id===tableDatas[i].id){
				tableDatas[i].progress=progress;
			}
		}
	},
	//更新导出进度
	updateExportProgress(id,exportProgress){
		var tableDatas= $store.state.taskTableDatas;
		for(let i=0;i<tableDatas.length;i++){
			if(id===tableDatas[i].id){
				tableDatas[i].exportProgress=exportProgress;
			}
		}
	},
	//更新进度信息
	update_progress_info(id,progress_info){
		var tableDatas= $store.state.taskTableDatas;
		for(let i=0;i<tableDatas.length;i++){
			if(id===tableDatas[i].id){
				tableDatas[i].progress_info=progress_info;
			}
		}
	},
	//更新缓存
	update_task_indexeddb(progress_id){
		var id = $store.state.downLoadTableId;
		var datas =	$store.state.taskTableDatas;
		var temp ="";
		for(let i=0;i<datas.length;i++){
			if(progress_id === datas[i].id){
				temp=datas[i]
			}
		}
		//更新缓存
		this.updateIndexedDB(id,temp);
	},
	updateIndexedDB(id,data){
		//打开一个数据库 并指定名称
		// let id = this.$data.mapContainer[0].tableId;
		var request = indexedDB.open("download",1);
		//成功回调函数
		request.onsuccess = function(e) {
			var db = e.target.result;
			//创建一个事务对象 指定表名 和操作模式
			var trans = db.transaction(id,"readwrite");
			//获取表格对象
			var store = trans.objectStore(id);
			//获取游标对象
			var objCursor = store.openCursor();
			objCursor.onsuccess = function(e){
				var cursor = e.target.result;
				if(cursor){
					if(cursor.value.id===data.id){
						cursor.update(data);
					}
					cursor.continue();
				}
			}
			db.close();
		};
	},
	// updateTaskIndexedDB(data){
	// 	var id = $store.state.downLoadTableId;
	// 	var datas =	$store.state.taskTableDatas;
	// 	var temp ="";
	// 	for(let i=0;i<datas.length;i++){
	// 		if(data.id === datas[i].id){
	// 			temp={
	// 				id:datas[i].id,
	// 				taskName:datas[i].taskName,
	// 				downType:datas[i].downType,
	// 				time:datas[i].time,
	// 				savePath:datas[i].savePath,
	// 				task_flag:datas[i].task_flag,
	// 				task_disable:datas[i].task_disable,
	// 				progress:datas[i].progress,
	// 				exportProgress:datas[i].exportProgress,
	// 			}
	// 		}
	// 	}
	// 	//更新缓存
	// 	this.updateIndexedDB(id,temp);
	// },
	isLoginAndTime(){
		var data = {
			options:{},
			flag:true
		};
		var time = new Date($store.state.administratorInfo.time).getTime();
		var time_now = new Date().getTime();
		if(time<time_now){
			data.options={
				showClose: true,
				type: 'error',
				message: '许可到期,请及时更新许可'
			}
			data.flag = false;
		}
		return data;
	},
	get_geojson(layer){
		var temp = layer.getLatLngs();
		//此处为深拷贝
		var temp_latlngs = JSON.parse(JSON.stringify(temp));
		for(let i=0;i<temp_latlngs.length;i++){
			for(let j=0;j<temp_latlngs[i].length;j++){
				temp_latlngs[i][j] = [temp_latlngs[i][j].lng,temp_latlngs[i][j].lat];
				if(j===temp_latlngs[i].length-1){
					temp_latlngs[i].push([temp_latlngs[i][0][0],temp_latlngs[i][0][1]])
					break;
				}
			}
		}
		var geojson = {
			Region:temp_latlngs,
			id:1
		};
		return JSON.stringify(geojson);
	},
	//清空自定义地图列表选中状态
	clear_custom_active(){
		var temp_list = $store.state.custom_map_list;
		for(let i=0;i<temp_list.length;i++){
			temp_list[i].isActive=false;
		}
	},
	init_change_slider(){
		var ruler_height = 147;
		var cursor_top = 135;
		var map = $store.state.map_container.map;
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		var current_zoom = map.getZoom();
		var temp_zoom="";
		if(current_zoom<=min_zoom){
			temp_zoom = min_zoom;
		}else if(current_zoom>min_zoom&&current_zoom<max_zoom){
			temp_zoom = current_zoom;
		}else if(map.getZoom()>=max_zoom){
			temp_zoom = max_zoom;
		}
		
		// 获取间隔数or级别数
		var steps = max_zoom - min_zoom;
		//获取间隔高度
		var step_height = ruler_height/steps;
		var step_top = cursor_top/steps;
		//设置mask高度
		$store.state.zoom_slider_info.mask_height = (max_zoom-temp_zoom)*step_height;
		//设置cursor位置
		$store.state.zoom_slider_info.cursor_top = (max_zoom-temp_zoom)*step_top;
	},
	//初始化级别指示条
	init_zoom_slider(){
		var ruler_height = 147;
		var cursor_top = 135;
		var map = $store.state.map_container.map;
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		var current_zoom = map.getZoom();
		// 获取间隔数or级别数
		var steps = max_zoom - min_zoom;
		//获取间隔高度
		var step_height = ruler_height/steps;
		var step_top = cursor_top/steps;
		//设置mask高度
		$store.state.zoom_slider_info.mask_height = (max_zoom-current_zoom)*step_height;
		//设置cursor位置
		$store.state.zoom_slider_info.cursor_top = (max_zoom-current_zoom)*step_top;
	},
	//初始化地图事件
	init_map_event(){
		var $this =this;
		var map = $store.state.map_container.map;
		map.on("zoomlevelschange",function(){
			$this.init_change_slider();
		})
		map.on("zoomend",function(){
			$this.init_zoom_slider();
			
		})
	},
	set_down_load_able(type){
		if(type.indexOf("谷歌地图")!=-1){
			$store.state.down_load_able.is_poi_able=true;
			$store.state.down_load_able.is_dem_able=false;
		}else if(type.indexOf("OSM")!==-1){
			$store.state.down_load_able.is_poi_able=true;
			$store.state.down_load_able.is_dem_able=true;
		}else if(type.indexOf("自定义")!==-1){
			$store.state.down_load_able.is_poi_able=true;
			$store.state.down_load_able.is_dem_able=true;
		}else if(type.indexOf("高德")!==-1){
			$store.state.down_load_able.is_poi_able=false;
			$store.state.down_load_able.is_dem_able=true;
		}else{
			$store.state.down_load_able.is_poi_able=true;
			$store.state.down_load_able.is_dem_able=true;
		}
	},
}