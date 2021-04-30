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
	clearScope(){
		$store.state.scopeInfo.isXZQH="";
		$store.state.scopeInfo.adcode="";
		for(let i=0;i<$store.state.scopeInfo.scopeLayer.length;i++){
			$store.state.scopeInfo.scopeLayer[i].remove();
		}
		$store.state.scopeInfo.scopeLayer.splice(0,$store.state.scopeInfo.scopeLayer.length);
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
	update_scopeInfo(flag,adcode,layer,geojson){
		$store.state.scopeInfo.isXZQH=flag;
		if(adcode){
			$store.state.scopeInfo.adcode=adcode;
		}
		if(layer){
			$store.state.scopeInfo.scopeLayer.push(layer);
		}
		if(geojson){
			$store.state.scopeInfo.geojson=geojson;
		}
	},
	//更新地图名称和任务名称
	updateNameAndUrl(){
		var mapList = $store.state.mapList;
		for(let i=0;i<mapList.length;i++){
			if(mapList[i].isShow){
				$store.state.downloadInfo.mapName=mapList[i].name;
				for(let j=0;j<mapList[i].urls.length;j++){
					if(mapList[i].urls[j].isActive){
						// $store.state.downloadInfo.taskName=mapList[i].urls[j].name;
						$store.state.downloadInfo.url=mapList[i].urls[j].realUrl;
					}
				}
			}
		}
	},
	//清空表格
	clearDownLoadTableAndScope(){
		$store.state.downloadTableDatas.splice(0,$store.state.downloadTableDatas.length);
		$store.state.downloadInfo.scope.splice(0,$store.state.downloadInfo.scope.length);
	},
	//更新zoom和分辨率
	updateZoomAndResolution(datas){
		for(let i=0;i<datas.length;i++){
			$store.state.downloadInfo.zoom.push(datas[i].level);
			var temp_scale=parseInt(datas[i].scale.split(":")[1]);
			var temp_dpi=datas[i].dpi
			var temp_resolution=Math.round(0.0254*temp_scale/temp_dpi);
			$store.state.downloadInfo.resolution.push(temp_resolution);
		}
	},
	//清空zoom和分辨率数组
	clearZoomAndResolution(){
		$store.state.downloadInfo.zoom.splice(0,$store.state.downloadInfo.zoom.length);
		$store.state.downloadInfo.resolution.splice(0,$store.state.downloadInfo.resolution.length);
	},
	updateTotal(datas){
		for(let i=0;i<datas.length;i++){
			$store.state.downloadInfo.total+=datas[i].total;
		}
	},
	clearTotal(){
		$store.state.downloadInfo.total=0;
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
		}else if(data.activeName==="3"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="osm矢量下载";
			$store.state.downloadInfo.taskName=data.vectorNameInput;
			$store.state.downloadInfo.savePath=data.vectorDownInput;
			$store.state.downloadInfo.saveType=data.vectorOptionValue;
			$store.state.downloadInfo.url="../osm/osm.udbx";
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="contourline"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="提取等值线";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			$store.state.downloadInfo.saveType=data.option_value;
			$store.state.downloadInfo.url=data.import_file_path;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="contourpolygon"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="提取等值面";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			$store.state.downloadInfo.saveType=data.option_value;
			$store.state.downloadInfo.url=data.import_file_path;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="coordinate"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="坐标转换";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			for(let i =0;i<data.options.length;i++){
				if(data.options[i].value===data.option_value){
					$store.state.downloadInfo.coordinate=data.options[i].label
				}
			}
			$store.state.downloadInfo.saveType=data.saveType;
			$store.state.downloadInfo.url=data.import_file_path;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="slopebox"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="坡度分析";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			$store.state.downloadInfo.saveType=data.option_value;
			$store.state.downloadInfo.url=data.import_file_path;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="aspectbox"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="坡向分析";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			$store.state.downloadInfo.saveType=data.option_value;
			$store.state.downloadInfo.url=data.import_file_path;
			$store.state.downloadInfo.time=this.getDate();
		}else if(data.type==="export"){
			$store.state.downloadInfo.id=this.UUID();
			$store.state.downloadInfo.downType="导出矢量";
			$store.state.downloadInfo.taskName=data.task_name;
			$store.state.downloadInfo.savePath=data.save_path;
			$store.state.downloadInfo.saveType=data.option_value;
			$store.state.downloadInfo.type=$store.state.layerSelectInfo.type;
			$store.state.downloadInfo.coordinate = data.option_value2;
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
		var layer = $store.state.scopeInfo.scopeLayer[0];
		var bounds = layer.getBounds();
		
		// var correctLngLatMin = gcj02towgs84(parseFloat(bounds.getWest().toFixed(5)),parseFloat(bounds.getSouth().toFixed(5)));
		// var correctLngLatMax = gcj02towgs84(parseFloat(bounds.getEast().toFixed(5)),parseFloat(bounds.getNorth().toFixed(5)));
		// $store.state.downloadInfo.bounds=correctLngLatMin[0].toFixed(5)+","+correctLngLatMin[1].toFixed(5)+","+correctLngLatMax[0].toFixed(5)+","+correctLngLatMax[1].toFixed(5);// var correctLngLatMin = gcj02towgs84(parseFloat(bounds.getWest().toFixed(5)),parseFloat(bounds.getSouth().toFixed(5)));
		// $store.state.downloadInfo.bounds=bounds.getWest().toFixed(5)+","+bounds.getSouth().toFixed(5)+","+bounds.getEast().toFixed(5)+","+bounds.getNorth().toFixed(5);
		// $store.state.downloadInfo.url="http://overpass.openstreetmap.ru/cgi/xapi_meta?*[bbox="+$store.state.downloadInfo.bounds+"]";
		// console.log($store.state.downloadInfo.url);
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
					}else if(layerGroup[i].children[j].type==="Point"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({radius: 1,color:'blue',weight:1});
					}else if(layerGroup[i].children[j].type==="Line"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'blue',weight:1});
					}else if(layerGroup[i].children[j].type==="Region"&&layerGroup[i].children[j].layer){
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
					}else if(layerGroup[i].children[j].type==="Point"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({radius: 1,color:'red',weight:1});
					}else if(layerGroup[i].children[j].type==="Line"&&layerGroup[i].children[j].layer){
						layerGroup[i].children[j].layer.setStyle({color:'red',weight:1});
					}else if(layerGroup[i].children[j].type==="Region"&&layerGroup[i].children[j].layer){
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
	},
	//清空属性表数据
	clearAttributeTable(){
		var temp_datas = $store.state.attributeTable;
		temp_datas.splice(0,temp_datas.length);
	},
	// 更新表头
	update_attribute_header(){
		var option_value = $store.state.layerSelectInfo.option_value;
		var temp_datas = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_datas.length;i++){
			if(temp_datas[i].label===option_value){
				$store.state.attributeHeader = temp_datas[i].table_header;
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
		var map="";
		for(let i=0;i<$store.state.mapContainer.length;i++){
			if($store.state.mapContainer[i].isShow){
				map=$store.state.mapContainer[i].map;
			}
		}
		return map;
	},
	//获取图层
	getLayer(){
		var layer="";
		for(let i=0;i<$store.state.mapContainer.length;i++){
			if($store.state.mapContainer[i].isShow){
				layer=$store.state.mapContainer[i].layer;
			}
		}
		return layer;
	},
	// 切换路由时 选择二维视图
	setTwoView(type){
		var flag=false;
		for(let i=0;i<$store.state.mapContainer.length;i++){
			if($store.state.mapContainer[i].isShow){
				if(type!==$store.state.mapContainer[i].type){
					flag=true;
				}
			}
		}
		if(flag){
			$(".el-tabs__item").each(function(){
				if($(this).text()==="二维视图"){
					$(this).trigger("click");
				}
			});
		}
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
	updateTaskIndexedDB(data){
		var id = $store.state.downLoadTableId;
		var temp={
			id:data.id,
			taskName:data.taskName,
			mapName:data.mapName,
			downType:data.downType,
			time:data.time,
			savePath:data.savePath,
			progress:100,
			exportProgress:100,
		};
		//更新缓存
		this.updateIndexedDB(id,temp);
	},
	updateTaskTableDatas(data){
		var $this = this;
		var id = $store.state.downLoadTableId;
		var temp={
			id:data.id,
			taskName:data.taskName,
			downType:data.downType,
			time:data.time,
			savePath:data.savePath,
			progress:0,
			exportProgress:0,
		};
		$store.state.taskTableDatas.push(temp);
		//下载任务添加入缓存
		$this.addIndexedDB(id,temp);
		
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
		console.log(temp);
		//此处为深拷贝
		var temp_latlngs = JSON.parse(JSON.stringify(temp));
		console.log(temp_latlngs);
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
	// get_xzqh_geojson(layer){
	// 	var temp = layer.getLatLngs();
	// 	console.log(temp);
	// 	//此处为深拷贝
	// 	var temp_latlngs = JSON.parse(JSON.stringify(temp));
	// 	console.log(temp_latlngs);
	// 	for(let i=0;i<temp_latlngs.length;i++){
	// 		for(let j=0;j<temp_latlngs[i][0].length;j++){
	// 			temp_latlngs[i][0][j] = [temp_latlngs[i][0][j].lng,temp_latlngs[i][0][j].lat];
	// 			if(j===temp_latlngs[i][0].length-1){
	// 				temp_latlngs[i][0].push([temp_latlngs[i][0][0][0],temp_latlngs[i][0][0][1]])
	// 				break;
	// 			}
	// 		}
	// 	}
	// 	var geojson = {
	// 		Region:temp_latlngs,
	// 		id:1
	// 	};
	// 	return JSON.stringify(geojson);
	// }
}