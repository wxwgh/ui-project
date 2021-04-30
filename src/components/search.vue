<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in searchPost" :class="{tabMouseOver:post.isShow}" @click="searchClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>搜索</span>
		</div>
	</div>
</template>

<script>
import searchpoibox from '@/components/searchpoibox.vue';
import searchlocationbox from '@/components/searchlocationbox.vue';
import searchplacebox from '@/components/searchplacebox.vue';
export default {
  name: 'search',
  data(){
    return {
		selectLength:10,
		fontLength:10,
		pageNum:50,
		searchPost:[
			{
				name:"坐标定位",
				url:require('../assets/vectorplot/location.png'),
				isShow:false,
				
			},
			{
				name:"地名搜索",
				url:require('../assets/vectorplot/toponymy.png'),
				isShow:false,
				
			},
			{
				name:"poi搜索",
				url:require('../assets/vectorplot/search.png'),
				isShow:false,
				
			},
		],
	}
  },
  computed:{
	zoom:function(){
		var map = this.myCommon.getMap();
		return map.getZoom();
	}
  },
  methods:{
	searchClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		$this.myCommon.clearOperation();
		if(post.name==="坐标定位"){
			$this.$confirm(<searchlocationbox ref='searchlocationbox'/>, '坐标定位', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var locationRegex = /^[0-9]+.+[0-9]+,+[0-9]+.+[0-9]+$/;
						if(!locationRegex.test($this.$refs.searchlocationbox.location_value)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '坐标格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var value = $this.$refs.searchlocationbox.location_value;
				var tempLatlng = value.split(",");
				var latlng = L.latLng(tempLatlng[1],tempLatlng[0]);
				var points=[];
				points.push(latlng);
				var marker = $this.myCommon.createMarker(latlng,value);
				$this.myCommon.setLocation(latlng,$this.zoom);
				//判断是否有坐标定位图层
				var layerGroup = $this.$store.state.layerGroups[0].children;
				var flag=false;
				var parentId=null;
				var layer_parent="";
				for(let i=0;i<layerGroup.length;i++){
					if(layerGroup[i].label==="坐标定位"){
						flag=true;
						parentId=layerGroup[i].id;
						layer_parent=layerGroup[i];
					}
				}
				var temp_list =["id","Name","parentId"];
				if(!flag){
					var table_header=[];
					for(let i=0;i<temp_list.length;i++){
						var temp={
							id:$this.$UUID(),
							alias:temp_list[i],
							name:temp_list[i],
						}
						table_header.push(temp);
					}
					//图层参数
					var option = {
						id:parentId,
						index:"2",
						label:"坐标定位",
						isTip:false,
						isPlot:true,
						type:"marker",
						isShow:true,
						icon:"fa fa-eye-slash",
						table_header:table_header,
						header_keys:temp_list,
						isSelect:true,
						children:[]
					}
					//创建图层
					$this.myCommon.createLayer(option);
					layer_parent=option;
					var temp={
						label:"坐标定位",
						type:"marker"
					}
					//添加至图层选中列表
					$this.myCommon.add_select_layer(temp);
					//更新header
					$this.myCommon.update_attribute_header();
					// 清除选取图层列表
					$this.myCommon.clear_operation_list();
					//更新当前选取图层列表
					$this.myCommon.update_operation_list([temp]);
				}
				var coordinate=[points[0].lng,points[0].lat];
				//获取geojsonid
				var geojson_id = layer_parent.children.length+1;
				var geojson={
					Point:coordinate,
					id:geojson_id
				}
				var label=null;
				var isTip=null;
				if(value.length>22){
					label = value.substring(0,22)+"...";
					isTip=true;
				}else{
					label=value;
					isTip=false;
				}
				var id = $this.$UUID();
				var attribute={};
				for(let i=0;i<temp_list.length;i++){
					if(temp_list[i]==="id"){
						attribute[temp_list[i]]=id;
					}else if(temp_list[i]==="Name"){
						attribute[temp_list[i]]="定位图层";
					}else if(temp_list[i]==="parentId"){
						attribute[temp_list[i]]=id;
					}else{
						attribute[temp_list[i]]="";
					}
					
				}
				var option2 = {
					id:id,
					parentId:parentId,
					index:"3",
					label:label,
					name:$this.$refs.searchlocationbox.location_value,
					isOperation:false,
					isTip:isTip,
					isShow:true,
					icon:"fa fa-eye-slash",
					isSelect:true,
					type:"marker",
					layer:marker,
					geojson:JSON.stringify(geojson),
					attribute:attribute,
					points:points,
				};
				//创建图层
				$this.myCommon.createLayer(option2);
			}).catch(() => {
				
			});
		}else if(post.name==="地名搜索"){
			if($this.$store.state.scopeInfo.scopeLayer.length===0){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前没有范围'
				});
				return false;
			}
			$this.$confirm(<searchplacebox ref='searchplacebox'/>, '地名搜索', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						if(!taskRegex.test($this.$refs.searchplacebox.place_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '地名格式不正确'
							});
							return false;
						}
						if($this.$refs.searchplacebox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '已有同名图层,请重名搜索结果图层'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var value = $this.$refs.searchplacebox.place_name;
				$this.searchResult(value);
				$this.$refs.searchplacebox.place_name="";
			}).catch(() => {
				
			});
		}else if(post.name==="poi搜索"){
			if($this.$store.state.scopeInfo.scopeLayer.length===0){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前没有范围'
				});
				return false;
			}
			$this.$confirm(<searchpoibox ref='searchpoibox'/>, 'poi搜索', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						if(!taskRegex.test($this.$refs.searchpoibox.poi_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: 'poi关键字格式不正确'
							});
							return false;
						}
						if($this.$refs.searchpoibox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '已有同名图层,请重命名搜索结果图层'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var value = $this.$refs.searchpoibox.poi_name;
				$this.searchResult(value);
				$this.$refs.searchpoibox.poi_name="";
			}).catch(() => {
				
			});
		}
	},
	searchResult(value){
		var $this=this;
		var id = $this.$UUID();
		var temp_list =["id","name","type","parentId"];
		var table_header=[];
		for(let i=0;i<temp_list.length;i++){
			var temp={
				id:$this.$UUID(),
				alias:temp_list[i],
				name:temp_list[i],
			}
			table_header.push(temp);
		}
		//图层参数
		var option = {
			id:id,
			index:"2",
			label:value,
			isTip:false,
			isPlot:false,
			isShow:true,
			type:"marker",
			icon:"fa fa-eye-slash",
			table_header:table_header,
			header_keys:temp_list,
			isSelect:true,
			children:[]
		}
		//创建图层
		$this.myCommon.createLayer(option);
		var layer_group = $this.$store.state.layerGroups[0].children;
		var layer_parent = "";
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].id===option.id){
				layer_parent=layer_group[i];
			}
		}
		
		var temp={
			label:value,
			type:"marker"
		}
		//添加至图层选中列表
		$this.myCommon.add_select_layer(temp);
		//更新header
		$this.myCommon.update_attribute_header();
		// 清除选取图层列表
		$this.myCommon.clear_operation_list();
		//更新当前选取图层列表
		$this.myCommon.update_operation_list([temp]);
		if($this.$store.state.scopeInfo.isXZQH){
			var url="https://restapi.amap.com/v3/place/text?s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&city="+$this.$store.state.scopeInfo.adcode+"&citylimit=false&extensions=all&language=zh_cn&callback=jsonp_991342_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/api/javascript-api/example/poi-search/keywords-search&csid=B7489A1F-1304-4922-81A1-1E3E4538E28F&sdkversion=1.4.15&keywords="+value;
			$this.axios({
				method: 'get',
				url: url
			}).then(function(result){
				console.log(result);
				var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
				var page = null;
				if(temp.count%$this.pageNum===0){
					page = parseInt(temp.count/$this.pageNum);
				}else{
					page = parseInt(temp.count/$this.pageNum)+1;
				}
				var select = [];
				//根据页数进行穷举查询
				for(let x=1;x<=page;x++){
					var url="https://restapi.amap.com/v3/place/text?s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page="+x+"&city="+$this.$store.state.scopeInfo.adcode+"&citylimit=false&extensions=all&language=zh_cn&callback=jsonp_991342_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/api/javascript-api/example/poi-search/keywords-search&csid=B7489A1F-1304-4922-81A1-1E3E4538E28F&sdkversion=1.4.15&keywords="+value;
					$this.axios({
						method: 'get',
						url: url
					}).then(function(result){
						var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
						for(let i=0;i<temp.pois.length;i++){
							var tempLatlng = temp.pois[i].location.split(",");
							var latlng = L.latLng(tempLatlng[1],tempLatlng[0]);
							var points=[];
							points.push(latlng);
							var marker =null;
							var label=null;
							var isTip=null;
							if(temp.pois[i].name.length>$this.fontLength){
								label = temp.pois[i].name.substring(0,$this.fontLength)+"...";
								isTip=true;
							}else{
								label=temp.pois[i].name;
								isTip=false;
							}
							var isSelect=null;
							var icon = null;
							if(i<$this.selectLength&&select.length<=$this.selectLength){
								select.push(i);
								isSelect=true;
								icon = "fa fa-eye-slash";
								marker = $this.myCommon.createMarker(latlng,temp.pois[i].name);
							}else if(i>=$this.selectLength||select.length>$this.selectLength){
								isSelect=false;
								icon ="fa fa-eye";
								marker=null;
							}
							var coordinate=[points[0].lng,points[0].lat];
							//获取geojsonid
							var geojson_id = layer_parent.children.length+1;
							var geojson={
								Point:coordinate,
								id:geojson_id
							}
							var layer_id = $this.$UUID();
							var attribute={};
							for(let j=0;j<temp_list.length;j++){
								if(temp_list[j]==="id"){
									attribute[temp_list[j]]=temp.pois[i].id;
								}else if(temp_list[j]==="name"){
									attribute[temp_list[j]]=temp.pois[i].name;
								}else if(temp_list[j]==="type"){
									attribute[temp_list[j]]=temp.pois[i].type;
								}else if(temp_list[j]==="parentId"){
									attribute[temp_list[j]]=layer_id;
								}else{
									attribute[temp_list[j]]="";
								}
								
							}
							var option = {
								id:layer_id,
								parentId:id,
								index:"3",
								label:label,
								name:temp.pois[i].name,
								isOperation:false,
								isTip:isTip,
								isShow:true,
								icon:icon,
								isSelect:isSelect,
								type:"marker",
								layer:marker,
								geojson:JSON.stringify(geojson),
								attribute:attribute,
								points:points,
							};
							//创建图层
							$this.myCommon.createLayer(option);
						}
					})
				}
				var center = $this.$store.state.scopeInfo.scopeLayer[0].getCenter();
				$this.myCommon.setLocation(center,$this.zoom);
			})
		}else{
			var bounds = $this.$store.state.scopeInfo.scopeLayer[0].getBounds();
			var latlngs = $this.$store.state.scopeInfo.scopeLayer[0].getLatLngs()[0];
			var center = $this.$store.state.scopeInfo.scopeLayer[0].getCenter();
			var polygonBounds="";
			for(let i=0;i<latlngs.length;i++){
				if(i===latlngs.length-1){
					polygonBounds+=latlngs[i].lng+","+latlngs[i].lat;
				}else{
					polygonBounds+=latlngs[i].lng+","+latlngs[i].lat+";";
				}
			}
			var url="https://restapi.amap.com/v3/place/polygon?polygon="+polygonBounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+value;
			$this.axios({
			  method: 'get',
			  url: url
			}).then(function (result) {
				var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
				var page = null;
				if(temp.count%$this.pageNum===0){
					page = parseInt(temp.count/$this.pageNum);
				}else{
					page = parseInt(temp.count/$this.pageNum)+1;
				}
				var select = [];
				//根据页数进行穷举查询
				for(let x=1;x<=page;x++){
					var url="https://restapi.amap.com/v3/place/polygon?polygon="+polygonBounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page="+x+"&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+value;
					$this.axios({
						method: 'get',
						url: url
					}).then(function(result){
						var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
						for(let i=0;i<temp.pois.length;i++){
							var tempLatlng = temp.pois[i].location.split(",");
							var latlng = L.latLng(tempLatlng[1],tempLatlng[0]);
							var points=[];
							points.push(latlng);
							var marker =null;
							var label=null;
							var isTip=null;
							if(temp.pois[i].name.length>$this.fontLength){
								label = temp.pois[i].name.substring(0,$this.fontLength)+"...";
								isTip=true;
							}else{
								label=temp.pois[i].name;
								isTip=false;
							}
							var isSelect=null;
							var icon = null;
							if(i<$this.selectLength&&select.length<=$this.selectLength){
								select.push(i);
								isSelect=true;
								icon = "fa fa-eye-slash";
								marker = $this.myCommon.createMarker(latlng,temp.pois[i].name);
							}else if(i>=$this.selectLength||select.length>$this.selectLength){
								isSelect=false;
								icon ="fa fa-eye";
								marker=null;
							}
							var coordinate=[points[0].lng,points[0].lat];
							//获取geojsonid
							var geojson_id = layer_parent.children.length+1;
							var geojson={
								Point:coordinate,
								id:geojson_id
							}
							var layer_id = $this.$UUID();
							var attribute={};
							for(let j=0;j<temp_list.length;j++){
								if(temp_list[j]==="id"){
									attribute[temp_list[j]]=layer_id;
								}else if(temp_list[j]==="name"){
									attribute[temp_list[j]]=temp.pois[i].name;
								}else if(temp_list[j]==="type"){
									attribute[temp_list[j]]=temp.pois[i].type;
								}else if(temp_list[j]==="parentId"){
									attribute[temp_list[j]]=layer_id;
								}else{
									attribute[temp_list[j]]="";
								}
							}
							var option = {
								id:layer_id,
								parentId:id,
								index:"3",
								label:label,
								name:temp.pois[i].name,
								isOperation:false,
								isTip:isTip,
								isShow:true,
								icon:icon,
								isSelect:isSelect,
								type:"marker",
								layer:marker,
								geojson:JSON.stringify(geojson),
								attribute:attribute,
								points:points,
							};
							//创建图层
							$this.myCommon.createLayer(option);
						}
					})
				}
				$this.myCommon.setLocation(center,$this.zoom);
			})	
		}
	},
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
  },
}
</script>

<style lang="less">
</style>
