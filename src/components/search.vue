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
		fontLength:7,
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
				var features=[];
				features.push([latlng.lat,latlng.lng]);
				var marker = $this.myCommon.createMarker(latlng,value);
				$this.myCommon.setLocation(latlng,$this.zoom);
				//判断是否有坐标定位图层
				var layerGroup = $this.$store.state.layerGroups[0].children;
				var flag=false;
				var layer_parent="";
				for(let i=0;i<layerGroup.length;i++){
					if(layerGroup[i].label==="坐标定位"){
						flag=true;
						layer_parent=layerGroup[i];
						break;
					}
				}
				var temp_list =["name","parentId","mydescribe"];
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
						id:$this.$UUID(),
						index:"2",
						count:0,
						label:"坐标定位",
						isTip:false,
						isPlot:true,
						type:"marker",
						isShow:true,
						coordinate:"4326",
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
					}else if(temp_list[i]==="name"){
						attribute[temp_list[i]]="定位图层";
					}else if(temp_list[i]==="parentId"){
						attribute[temp_list[i]]=layer_parent.id;
					}else{
						attribute[temp_list[i]]="用户自定义坐标";
					}
					
				}
				var option2 = {
					id:id,
					parentId:layer_parent.id,
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
					attribute:attribute,
					features:features,
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
						$this.$refs.searchplacebox.place_name="";
						done();
					}else if(action==="cancel"){
						$this.$refs.searchplacebox.place_name="";
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
							    message: '已有同名图层,请重命名搜索结果图层'
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
		}
	},
	searchResult(value){
		var $this=this;
		var id = $this.$UUID();
		var temp_list =["id","name","address","tel","timestamp","type","parentId"];
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
			count:0,
			label:value,
			isTip:false,
			isPlot:false,
			isShow:true,
			type:"marker",
			coordinate:"4326",
			icon:"fa fa-eye-slash",
			table_header:table_header,
			header_keys:temp_list,
			isSelect:true,
			children:[]
		}
		//创建图层
		$this.myCommon.createLayer(option);
		var layer_parent = option;
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
		$this.$store.state.loading=true;
		if($this.$store.state.scopeInfo.isXZQH){
			var url="https://restapi.amap.com/v3/place/text?s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&city="+$this.$store.state.scopeInfo.adcode+"&citylimit=false&extensions=all&language=zh_cn&callback=jsonp_991342_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/api/javascript-api/example/poi-search/keywords-search&csid=B7489A1F-1304-4922-81A1-1E3E4538E28F&sdkversion=1.4.15&keywords="+value;
			$this.axios({
				method: 'get',
				url: url
			}).then(function(result){
				var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
				var page = null;
				if(parseInt(temp.count) === 0){
					$this.$store.state.loading=false;
					$this.$message({
					    showClose: true,
						type: 'error',
					    message: '没有查询到数据'
					});
					$this.$refs.searchplacebox.place_name=""
					return false;
				}
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
							// var tempLatlng = temp.pois[i].location.split(",");
							var temp_lnglat=$this.gcj02towgs84(parseFloat(temp.pois[i].location.split(",")[0]),parseFloat(temp.pois[i].location.split(",")[1]));
							var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
							var features=[];
							features.push([latlng.lat,latlng.lng]);
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
							}else{
								isSelect=false;
								icon ="fa fa-eye";
								marker=null;
							}
							var layer_id = $this.$UUID();
							var attribute={
								id:temp.pois[i].id,
								name:temp.pois[i].name,
								address:temp.pois[i].address,
								tel:temp.pois[i].tel,
								timestamp:temp.pois[i].timestamp,
								type:temp.pois[i].type,
								parentId:layer_id,
							};
							if(temp.pois[i].address instanceof Array){
								attribute.address="";
							}
							if(temp.pois[i].tel instanceof Array){
								attribute.tel = "";
							}
							var option2 = {
								id:layer_id,
								parentId:layer_parent.id,
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
								attribute:attribute,
								features:features,
							};
							//创建图层
							$this.myCommon.createLayer(option2);
						}
						$this.$store.state.loading=false;
					})
				}
			})
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
			var url="https://restapi.amap.com/v3/place/polygon?polygon="+bounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page=1&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+value;
			$this.axios({
			  method: 'get',
			  url: url
			}).then(function (result) {
				var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
				var page = null;
				if(parseInt(temp.count) === 0){
					$this.$store.state.loading=false;
					$this.$message({
					    showClose: true,
						type: 'error',
					    message: '没有查询到数据'
					});
					$this.$refs.searchplacebox.place_name=""
					return false;
				}
				if(temp.count%$this.pageNum===0){
					page = parseInt(temp.count/$this.pageNum);
				}else{
					page = parseInt(temp.count/$this.pageNum)+1;
				}
				var select = [];
				//根据页数进行穷举查询
				for(let x=1;x<=page;x++){
					var url="https://restapi.amap.com/v3/place/polygon?polygon="+bounds+"&s=rsv3&children=&key="+$this.$store.state.gaodeKey+"&offset=50&page="+x+"&extensions=all&language=zh_cn&callback=jsonp_92507_&platform=JS&logversion=2.0&appname=https://developer.amap.com/demo/javascript-api/example/poi-search/polygon-search&csid=58010E3A-66A1-49A4-B134-FF6B6966DF15&sdkversion=1.4.15&keywords="+value;
					$this.axios({
						method: 'get',
						url: url
					}).then(function(result){
						var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
						for(let i=0;i<temp.pois.length;i++){
							var temp_lnglat=$this.gcj02towgs84(parseFloat(temp.pois[i].location.split(",")[0]),parseFloat(temp.pois[i].location.split(",")[1]));
							var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
							var features=[];
							features.push([latlng.lat,latlng.lng]);
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
							}else{
								isSelect=false;
								icon ="fa fa-eye";
								marker=null;
							}
							var layer_id = $this.$UUID();
							var attribute={
								id:temp.pois[i].id,
								name:temp.pois[i].name,
								address:temp.pois[i].address,
								tel:temp.pois[i].tel,
								timestamp:temp.pois[i].timestamp,
								type:temp.pois[i].type,
								parentId:layer_id.id,
							};
							if(temp.pois[i].address instanceof Array){
								attribute.address="";
							}
							if(temp.pois[i].tel instanceof Array){
								attribute.tel = "";
							}
							var option2 = {
								id:layer_id,
								parentId:layer_parent.id,
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
								attribute:attribute,
								features:features,
							};
							//创建图层
							$this.myCommon.createLayer(option2);
						}
						$this.$store.state.loading=false;
					})
				}
				
			})	
		}
		$(".mapListBottom span").each(function(){
			if($(this).text()==="图层管理"){
				$(this).trigger("click");
			}
		});
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
