<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in mapDownLoadPost" :class="{tabMouseOver:post.isShow}" @click="downLoadClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>下载相关</span>
		</div>
	</div>
</template>

<script>
import mapdownloadbox from '@/components/mapdownloadbox.vue';
export default {
  name: 'mapdownload',
  components:{
  	mapdownloadbox,
  },
  data(){
    return {
		mapDownLoadPost:[
			{
				name:"地图下载",
				url:require('../assets/mapdownload/vector.png'),
				isShow:false,
				
			},
			{
				name:"下载任务",
				url:require('../assets/mapdownload/DownLoadManager.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
  	downLoadClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		var temp_data = this.myCommon.isLoginAndTime();
		if(!temp_data.flag){
			this.$message(temp_data.options);
			return temp_data.flag
		}
		if(post.name==="地图下载"){
			//判断是否有范围
			if(this.$store.state.scopeInfo.scopeLayer.length===0){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前没有范围'
				});
				return false;
			}
			//更新下载表格数据
			this.myCommon.updateDownLoadTable();
			//清空下载级别和比例尺
			// this.myCommon.clearZoomAndResolution();
			this.$confirm(<mapdownloadbox ref="mapdownloadbox" />, '地图下载', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				customClass:"mapdownloadClass",
				beforeClose:function(action, instance, done){
					if(action==="close"){
						//初始化下载表单
						$this.$refs.mapdownloadbox.init_poi_panel();
						$this.$refs.mapdownloadbox.init_tile_panel();
						$this.$refs.mapdownloadbox.init_dem_panel();
						done();
					}else if(action==="cancel"){
						//初始化下载表单
						$this.$refs.mapdownloadbox.init_poi_panel();
						$this.$refs.mapdownloadbox.init_tile_panel();
						$this.$refs.mapdownloadbox.init_dem_panel();
						done();
					}else if(action==="confirm"){
						if($this.$refs.mapdownloadbox.activeName==="1"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.tileNameInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.tileDownInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.$refs.down_table.selection.length===0){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '请选择下载级别'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.isName){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}else{
								done();
							}
						}else if($this.$refs.mapdownloadbox.activeName==="2"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.demNameInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.demDownInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.isName){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}else{
								done();
							}
						}else if($this.$refs.mapdownloadbox.activeName==="3"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.poi_name)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!taskRegex.test($this.$refs.mapdownloadbox.poi_search_name)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '搜索关键字不能为空'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.poi_save_path)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.is_poi_name){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}else{
								done();
							}
						}
					}
				}
			}).then(() => {
				if($this.$refs.mapdownloadbox.activeName==="1"){
					var mapList = $this.$store.state.mapList;
					var map_name = "";
					var url = "";
					for(let i=0;i<mapList.length;i++){
						if(mapList[i].isShow){
							map_name=mapList[i].name;
							for(let j=0;j<mapList[i].urls.length;j++){
								if(mapList[i].urls[j].isActive){
									url=mapList[i].urls[j].realUrl;
								}
							}
						}
					}
					//构建影像下载信息
					var data = {
						id:$this.$UUID(),
						downType:map_name+"影像下载",
						map_name:map_name,
						taskName:$this.$refs.mapdownloadbox.tileNameInput,
						savePath:$this.$refs.mapdownloadbox.tileDownInput,
						tile_is_clip:$this.$refs.mapdownloadbox.tile_is_clip,
						is_joint:$this.$refs.mapdownloadbox.tile_radio,
						url:url,
						scope:$this.$store.state.scopeInfo.geojson,
						time:$this.getDate(),
						zoom:[],
						total:0
					};
					var selection = $this.$refs.mapdownloadbox.$refs.down_table.selection;
					for(let i=0;i<selection.length;i++){
						data.zoom.push(selection[i].level);
						data.total=data.total+selection[i].total;
					}
					console.log(data);
					$this.myCommon.openTaskTable();
					//调用后端下载函数
					tile_load(data);
					async function tile_load(data){
						//python瓦片下载函数
						await eel.tile_load(data)();
						$this.$refs.mapdownloadbox.init_tile_panel();
					}
				}else if($this.$refs.mapdownloadbox.activeName==="2"){
					//更新下载信息
					$this.myCommon.updateDownLoadInfo($this.$refs.mapdownloadbox);
					var data = $this.$store.state.downloadInfo;
					//更新下载任务表
					$this.myCommon.updateTaskTableDatas(data);
					$this.myCommon.openTaskTable();
					//调用后端下载函数
					dem_load(data);
					async function dem_load(data){
						//python瓦片下载函数
						await eel.dem_load(data)();
						$this.$refs.mapdownloadbox.init_dem_panel();
					}
					
				}else if($this.$refs.mapdownloadbox.activeName==="3"){
					//构建导出参数对象
					var info ={
						savePath:$this.$refs.mapdownloadbox.poi_save_path,
						taskName:$this.$refs.mapdownloadbox.poi_name,
						source:"4326",
						target:"4326",
						seven:"",
						features:[],
						attributes:[],
						saveType:$this.$refs.mapdownloadbox.poi_save_format,
					}
					if($this.$store.state.scopeInfo.isXZQH){
						get_poi_temp();
						async function get_poi_temp(){
							$this.$store.state.loading=true;
							var data = await get_poi_xzqh();
							if(data){
								console.log(data);
								$this.$store.state.loading=false;
								// 调用后台导出功能
								var temp_info={
									id:$this.$UUID(),
									downType:"POI下载",
									taskName:$this.$refs.mapdownloadbox.poi_name,
									savePath:$this.$refs.mapdownloadbox.poi_save_path,
									saveType:$this.$refs.mapdownloadbox.poi_save_format,
									type:"point",
									source:"4326",
									target:"4326",
									seven:"",
									time:$this.getDate(),
									features:data.features,
									attributes:data.attributes,
								}
								console.log(temp_info)
								//更新下载任务表
								$this.myCommon.updateTaskTableDatas(temp_info);
								$this.myCommon.openTaskTable();
								//导出数据
								export_features(temp_info);
								async function export_features(temp_info){
									await eel.export_features(temp_info)();
									$this.$refs.mapdownloadbox.init_poi_panel();
								}
							}
						}
						async function get_poi_xzqh(){
							var url="https://restapi.amap.com/v3/place/text?s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&city="+$this.$store.state.scopeInfo.adcode+"&citylimit=false&extensions=all&language=zh_cn&callback=jsonp_991342_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/api/javascript-api/example/poi-search/keywords-search&csid=B7489A1F-1304-4922-81A1-1E3E4538E28F&sdkversion=1.4.15&keywords="+$this.$refs.mapdownloadbox.poi_search_name;
							var result = await $this.axios({
								method: 'get',
								url: url
							})
							var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
							var page = null;
							if(temp.count%50===0){
								page = parseInt(temp.count/50);
							}else{
								page = parseInt(temp.count/50)+1;
							}
							var select = [];
							//根据页数进行穷举查询
							for(let x=1;x<=page;x++){
								var url="https://restapi.amap.com/v3/place/text?s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page="+x+"&city="+$this.$store.state.scopeInfo.adcode+"&citylimit=false&extensions=all&language=zh_cn&callback=jsonp_991342_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/api/javascript-api/example/poi-search/keywords-search&csid=B7489A1F-1304-4922-81A1-1E3E4538E28F&sdkversion=1.4.15&keywords="+$this.$refs.mapdownloadbox.poi_search_name;
								var result = await $this.axios({
									method: 'get',
									url: url
								})
								var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
								for(let i=0;i<temp.pois.length;i++){
									var temp_lnglat=$this.gcj02towgs84(parseFloat(temp.pois[i].location.split(",")[0]),parseFloat(temp.pois[i].location.split(",")[1]));
									var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
									var temp_attribute = {
										id:temp.pois[i].id,
										name:temp.pois[i].name,
										address:temp.pois[i].address,
										tel:temp.pois[i].tel,
										timestamp:temp.pois[i].timestamp,
										type:temp.pois[i].type,
									};
									info.attributes.push(temp_attribute);
									info.features.push([[latlng.lat,latlng.lng]]);
								}
							}
							return info;
						}
						
					}else{
						var layers = $this.$store.state.scopeInfo.scopeLayer;
						var bounds = "";
						if(layers.length>1){
							for(let i=0;i<layers.length;i++){
								if(i===0){
									bounds = layers[i].getBounds();
								}else{
									bounds = bounds.extend(layers[i].getBounds());
								}
							}
							var temp_bounds = "";
							// 获取左上坐标
							temp_bounds+=bounds.getNorthWest().lng+","+bounds.getNorthWest().lat+";";
							temp_bounds+=bounds.getSouthEast().lng+","+bounds.getSouthEast().lat;
							bounds = temp_bounds;
						}else{
							var latlngs = layers[0].getLatLngs()[0];
							for(let i=0;i<latlngs.length;i++){
								if(i===latlngs.length-1){
									bounds+=latlngs[i].lng+","+latlngs[i].lat;
								}else{
									bounds+=latlngs[i].lng+","+latlngs[i].lat+";";
								}
							}
						}
						$this.$store.state.loading=true;
						get_poi_temp();
						async function get_poi_temp(){
							var data = await get_poi_xzqh();
							if(data){
								console.log(data);
								$this.$store.state.loading=false;
								// 调用后台导出功能
								var temp_info={
									id:$this.$UUID(),
									downType:"POI下载",
									taskName:$this.$refs.mapdownloadbox.poi_name,
									savePath:$this.$refs.mapdownloadbox.poi_save_path,
									saveType:$this.$refs.mapdownloadbox.poi_save_format,
									type:"point",
									source:"4326",
									target:"4326",
									seven:"",
									time:$this.getDate(),
									features:data.features,
									attributes:data.attributes,
								}
								console.log(temp_info)
								//更新下载任务表
								$this.myCommon.updateTaskTableDatas(temp_info);
								$this.myCommon.openTaskTable();
								//导出数据
								export_features(temp_info);
								async function export_features(temp_info){
									await eel.export_features(temp_info)();
									$this.$refs.mapdownloadbox.init_poi_panel();
								}
								
							}
						}
						async function get_poi_xzqh(){
							var url="https://restapi.amap.com/v3/place/polygon?polygon="+bounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+$this.$refs.mapdownloadbox.poi_search_name;
							var result = await $this.axios({
							  method: 'get',
							  url: url
							})
							var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
							var page = null;
							if(temp.count%50===0){
								page = parseInt(temp.count/50);
							}else{
								page = parseInt(temp.count/50)+1;
							}
							var select = [];
							//根据页数进行穷举查询
							for(let x=1;x<=page;x++){
								var url="https://restapi.amap.com/v3/place/polygon?polygon="+bounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page="+x+"&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+$this.$refs.mapdownloadbox.poi_search_name;
								var result = await $this.axios({
									method: 'get',
									url: url
								})
								var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
								for(let i=0;i<temp.pois.length;i++){
									var temp_lnglat=$this.gcj02towgs84(parseFloat(temp.pois[i].location.split(",")[0]),parseFloat(temp.pois[i].location.split(",")[1]));
									var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
									var temp_attribute = {
										id:temp.pois[i].id,
										name:temp.pois[i].name,
										address:temp.pois[i].address,
										tel:temp.pois[i].tel,
										timestamp:temp.pois[i].timestamp,
										type:temp.pois[i].type,
									};
									info.attributes.push(temp_attribute);
									info.features.push([[latlng.lat,latlng.lng]]);
								}
							}
							return info;
						}
					}
				}
			}).catch(() => {
				
			});
		}else if(post.name==="下载任务"){
			this.myCommon.openTaskTable();
		}
  	},
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
	// getDate(){
	// 	var time=new Date().getFullYear() +"/" + (new Date().getMonth()+1)+"/"+new Date().getDate()+" "+new Date().getHours() +":"+ new Date().getMinutes()+":"+new Date().getSeconds();
	// 	return time;
	// },
  },
}
</script>

<style lang="less">
.mapdownloadClass{
	width:500px;
	height:500px;
}
</style>
