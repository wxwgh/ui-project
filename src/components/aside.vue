<template>
	<div id="mapListParent">
		<template v-for="post in mapListHeader">
			<div class="mapListHeader" v-if="post.isShow" :id="post.id">
				<el-image class="asideImage" :src="post.image" fit='fill'></el-image>
				<span>{{post.name}}</span>
			</div>
		</template>
		<div class="mapListMain">
			<div v-if="mapListHeader[0].isShow">
				<template v-for="post in mapList">
					<ul v-if="post.isShow" :id="post.id" class="mapListUlClass">
						<li v-for="p in post.urls" :id="p.id" :class="{textActive:p.isActive,mapListOver:p.isShow}" @click="mapListMainClick(p)" @mouseleave="mouseLeave(p)" @mouseover="mouseOver(p)">
							<el-image class="mapListMainImage" :src="p.image" fit='fill'></el-image>
							<span>{{p.name}}</span>
						</li>
					</ul>
				</template>
				<el-tree v-if="get_is_show" :data="get_custom_map_list" default-expand-all :expand-on-click-node="false" >
					<span class="custom-tree-node" slot-scope="{node,data}"  @click.stop="mymap_tree_click(data)">
						<span v-if="data.index==='1'">
							<span>{{node.label}}</span>
						</span>
						<span v-else-if="data.index==='2'" class="map_child_class">
							<el-image :src="data.image" class="map_child_image"></el-image>
							<span>{{node.label}}</span>
						</span>
						<span v-if="data.index==='1'">
							<el-button size="mini" type="text">{{data.count}}</el-button>
							<el-button size="mini" type="text" icon="el-icon-plus" @click.stop="add_click()"></el-button>
						</span>
						<span v-else>
							<el-button size="mini" type="text" icon="el-icon-minus" @click.stop="delete_click(node,data)"></el-button>
						</span>
					</span>
				</el-tree>
			</div>
			<div v-if="mapListHeader[1].isShow">
				<!-- 图层树 -->
				<layertree></layertree>
			</div>
			<div v-if="mapListHeader[2].isShow">
				<!-- 导航树 -->
				<navigationtree></navigationtree>
			</div>
		</div>
		<template v-for="post in mapListBottom">
			<div class="mapListBottom" :class="{textActive:post.isActive,mapListOver:post.isShow}" :id="post.id" @click="mapListBottomClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="asideImage" :src="post.image" fit='fill'></el-image>
				<span>{{post.name}}</span>
			</div>
		</template>
	</div>
</template>

<script>
import layertree from '@/components/layertree.vue';
import navigationtree from '@/components/navigationtree.vue';
import custommaplistbox from '@/components/custommaplistbox.vue';
export default {
  name: 'myaside',
  components:{
  	layertree,
	navigationtree,
	custommaplistbox,
  },
  data(){
	return {
		mapListHeader:[
			{
				id:this.$UUID(),
				name:"地图列表",
				image:require('../assets/maplist/mapList.png'),
				isShow:true
			},
			{
				id:this.$UUID(),
				name:"图层管理",
				image:require('../assets/maplist/layerManager.png'),
				isShow:false
			},
			{
				id:this.$UUID(),
				name:"快速导航",
				image:require('../assets/maplist/xzqh.png'),
				isShow:false
			},
			// {
			// 	id:this.$UUID(),
			// 	name:"自定义地图列表",
			// 	image:require('../assets/maplist/release.png'),
			// 	isShow:false
			// },
		],
		mapListBottom:[
			{
				id:this.$UUID(),
				name:"地图列表",
				image:require('../assets/maplist/mapList.png'),
				isShow:false,
				isActive:true
			},
			{
				id:this.$UUID(),
				name:"图层管理",
				image:require('../assets/maplist/layerManager.png'),
				isShow:false,
				isActive:false
			},
			{
				id:this.$UUID(),
				name:"快速导航",
				class:"asideImage",
				image:require('../assets/maplist/xzqh.png'),
				isShow:false,
				isActive:false
			},
			// {
			// 	id:this.$UUID(),
			// 	name:"自定义地图列表",
			// 	class:"asideImage",
			// 	image:require('../assets/maplist/release.png'),
			// 	isShow:false,
			// 	isActive:false
			// },
		],
		mapList:this.$store.state.mapList
	}
  },
  computed:{
  	  get_custom_map_list:function(){
  		  return this.$store.state.custom_map_list;
  	  },
	  get_is_show:function(){
		  return this.$store.state.custom_map_list[0].is_show;
	  },
  },
  methods:{
	//点击地图
	mymap_tree_click(data){
		var $this =this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		var layer = this.myCommon.getLayer();
		if(data.index==="1"){
			return false;
		}else if(data.index==="2"){
			//判断是否有底图
			if(layer){
				//删除图层
				layer.remove();
			}
			//清空三维图层
			this.$store.state.viewer.imageryLayers.removeAll();
			var map_list = $this.$store.state.custom_map_list[0].children;
			for(let i=0;i<map_list.length;i++){
				if(data.id === map_list[i].id){
					map_list[i].isActive = true;
					if(map_list[i].type === "wmts"){
						layer = L.tileLayer.chinaProvider(map_list[i].url).addTo(map);
						//更新三维场景图层
						this.$store.state.viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider(map_list[i].imageProvider));
					}else if(map_list[i].type === "wms"){
						var layer_name = map_list[i].realUrl.slice(map_list[i].realUrl.lastIndexOf("/")+1,map_list[i].realUrl.length);
						layer = L.tileLayer.wms(map_list[i].realUrl, {
						    layers: layer_name,
						    format: 'image/png',
						    transparent: true,
						    attribution: "Weather data © 2012 IEM Nexrad"
						}).addTo(map);
						this.$store.state.viewer.imageryLayers.addImageryProvider(new Cesium.WebMapServiceImageryProvider(map_list[i].imageProvider))
					}
					this.$store.state.map_container.layer = layer;
				}
			}
			// 取消所有base地图选中状态
			var map_base_list = this.$store.state.mapList;
			for(let i=0;i<map_base_list.length;i++){
				for(let j=0;j<map_base_list[i].urls.length;j++){
					map_base_list[i].urls[j].isActive=false;
				}
				
			}
		}
	},
	//添加自定义地图
	add_click(){
		var $this =this;
		$this.$confirm(<custommaplistbox ref='custommaplistbox'/>, '添加地图', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					$this.$refs.custommaplistbox.init_custommaplistbox();
					done();
				}else if(action==="cancel"){
					$this.$refs.custommaplistbox.init_custommaplistbox();
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					if(!taskRegex.test($this.$refs.custommaplistbox.map_name)){
						$this.$message({
							showClose: true,
							type: 'error',
							message: '服务名称,格式不正确'
						});
						return false;
					}
					if(!taskRegex.test($this.$refs.custommaplistbox.map_url)){
						$this.$message({
							showClose: true,
							type: 'error',
							message: '服务地址,格式不正确'
						});
						return false;
					}
					if($this.$refs.custommaplistbox.isName){
						$this.$message({
							showClose: true,
							type: 'error',
							message: '已有同名服务'
						});
						return false;
					}else{
						done();
					}
					
				}
			}
		}).then(() => {
			// 判断地址类型
			var type ="";
			var imageProvider="";
			if($this.$refs.custommaplistbox.map_url.indexOf("{x}")!=-1){
				type = "wmts";
				//添加至provider对象
				L.TileLayer.ChinaProvider.providers.CusTom.Normal["自定义-"+$this.$refs.custommaplistbox.map_name] = $this.$refs.custommaplistbox.map_url.split(":")[1];
				L.TileLayer.ChinaProvider.providers.CusTom["Subdomains"]=[];
				imageProvider={
					url:$this.$refs.custommaplistbox.map_url,
				};
			}else{
				type = "wms";
				var layer_name = $this.$refs.custommaplistbox.map_url.slice($this.$refs.custommaplistbox.map_url.lastIndexOf("/")+1,$this.$refs.custommaplistbox.map_url.length);
				imageProvider={
					url:$this.$refs.custommaplistbox.map_url,
					layers:layer_name,
					parameters:{
						format:'image/png',
						transparent: true,
						attribution: "Weather data © 2012 IEM Nexrad"
					}
				}
			}
			//添加服务 至全局对象
			var temp = {
				id:$this.$UUID(),
				label:"自定义-"+$this.$refs.custommaplistbox.map_name,
				index:"2",
				type:type,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				isActive:false,
				isShow:false,
				minZoom: 3,
				maxZoom: 18,
				image:require('../assets/custommaplist/custom.png'),
				url:"CusTom.Normal."+"自定义-"+$this.$refs.custommaplistbox.map_name,
				realUrl:$this.$refs.custommaplistbox.map_url,
				imageProvider:imageProvider,
			};
			$this.$store.state.custom_map_list[0].children.push(temp);
			$this.$store.state.custom_map_list[0].count +=1;
			//添加服务 至indexed
			var id = $this.$store.state.custom_map_list_id;
			$this.myCommon.addIndexedDB(id,temp);
			$this.$refs.custommaplistbox.init_custommaplistbox();
		}).catch(() => {
			
		});
	},
	// 删除自定义地图
	delete_click(node,data){
		var $this = this;
		this.$confirm('地图删除后不可恢复, 是否继续?', '删除地图', {
		    confirmButtonText: '确定',
		    cancelButtonText: '取消',
			closeOnClickModal:false,
		    type: 'warning'
		}).then(() => {
			var map_list = $this.$store.state.custom_map_list[0].children;
			var id = $this.$store.state.custom_map_list_id;
			for(let i=0;i<map_list.length;i++){
				if(map_list[i].id === data.id){
					map_list.splice(i,1);
					$this.$store.state.custom_map_list[0].count -=1;
					// 缓存中删除地图
					$this.myCommon.deleteIndexedDB(id,data);
					break;
				}
			}
		}).catch(() => {
			
		});
		
	},
	mapListMainClick(post){
		//获取map
		var map = this.myCommon.getMap();
		var layer = this.myCommon.getLayer();
		if(layer){
			//删除图层
			layer.remove();
		}
		this.myCommon.set_down_load_able(post.name);
		//清空三维图层
		this.$store.state.viewer.imageryLayers.removeAll();
		var mapList = this.$store.state.mapList;
		for(let i=0;i<mapList.length;i++){
			for(let j=0;j<mapList[i].urls.length;j++){
				if(mapList[i].urls[j].name===post.name){
					mapList[i].urls[j].isActive=true;
					//更新三维场景图层
					this.$store.state.viewer.imageryLayers.addImageryProvider(mapList[i].urls[j].imageProvider);
					if(post.name.indexOf("必应")!==-1){
						var options={
							bingMapsKey:mapList[i].urls[j].key,
							imagerySet:mapList[i].urls[j].url
						}
						layer = L.tileLayer.bing(options).addTo(map);
					}else{
						layer = L.tileLayer.chinaProvider(mapList[i].urls[j].url).addTo(map);
					}
					this.$store.state.map_container.layer = layer;
				}else{
					mapList[i].urls[j].isActive=false;
				}
			}
		}
		//更新下载信息
		this.myCommon.updateNameAndUrl();
	},
	mapListBottomClick(post){
		if(post.name==="图层管理"){
			var temp_data = this.myCommon.isLoginAndTime();
			if(!temp_data.flag){
				this.$message(temp_data.options);
				return temp_data.flag
			}
		}
		for(let i=0;i<this.mapListBottom.length;i++){
			if(post.name===this.mapListBottom[i].name){
				this.mapListBottom[i].isActive=true;
				this.mapListHeader[i].isShow=true;
			}else{
				this.mapListBottom[i].isActive=false;
				this.mapListHeader[i].isShow=false;
			}
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

<style>
.asideImage{
	width: 24px;
	height: 24px;
	vertical-align:middle;
	margin-right: 5px;
	margin-left: 5px;
	margin-bottom: 2px;
}
.navigationImage{
	width: 24px;
	height: 24px;
	margin-right: 10px;
	margin-left: 5px;
	box-shadow: 1px 1px 1px #888888;
}
.el-collapse-item__content{
	padding-bottom: 0;
}
#mapListParent{
	display: flex;
	flex-direction: column;
	justify-content:flex-start;
	width:100%;
	height: 100%;
	border-right:1px solid #E4E7ED;
}
.mapListHeader{
	line-height: 39px;
	font-size: 13px;
	font-weight: 500;
	color: #303133;
	border-bottom: 1px solid #E4E7ED;
	width: 100%;
}
.mapListBottom{
	line-height: 39px;
	font-size: 13px;
	font-weight: 500;
	color: #303133;
	border-bottom: 1px solid #E4E7ED;
	width: 100%;
	cursor: pointer;
}
.mapListMain{
	flex-grow: 1;
	flex-flow: column;
	width: 100%;
	height: 0;
	overflow-y: auto;
	border-bottom: 1px solid #E4E7ED;
}
.mapListOver{
	background-color: #409eff1a;
}
.mapListUlClass{
	width: 100%;
	height: 100%;
	font-size: 13px;
	color: #303133;
	line-height: 38px;
	
}
.mapListUlClass>li{
	cursor:pointer;
}
.mapListMainImage{
	width: 20px;
	height: 20px;
	vertical-align:middle;
	margin-right: 10px;
	margin-left: 20px;
	margin-bottom: 2px;
	box-shadow: 1px 1px 1px #888888;
}
.map_child_class{
	display:flex;
	flex-direction:row;
	justify-content:space-between;
	align-items:center;
	
}
.map_child_image{
	width:14px;
	height:14px;
	margin-right:3px;
}
</style>
