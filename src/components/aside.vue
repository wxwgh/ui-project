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
export default {
  name: 'myaside',
  components:{
  	layertree,
	navigationtree,
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
		],
		mapList:this.$store.state.mapList
	}
  },
  methods:{
	mapListMainClick(post){
		//获取map
		var map = this.myCommon.getMap();
		var layer = this.myCommon.getLayer();
		if(layer){
			//删除图层
			layer.remove();
		}
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
					this.myCommon.updateLayer(layer);
				}else{
					mapList[i].urls[j].isActive=false;
				}
			}
		}
		//设置地图缩放级别
		this.myCommon.setMapZoom();
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
	line-height: 48px;
	font-size: 13px;
	font-weight: 500;
	color: #303133;
	border-bottom: 1px solid #E4E7ED;
	width: 100%;
}
.mapListBottom{
	line-height: 48px;
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
	line-height: 48px;
	
}
.mapListUlClass>li{
	cursor:pointer;
}
.mapListMainImage{
	width: 24px;
	height: 24px;
	vertical-align:middle;
	margin-right: 10px;
	margin-left: 20px;
	margin-bottom: 2px;
	box-shadow: 1px 1px 1px #888888;
}
</style>
