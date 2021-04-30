<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<router-link to="/CommonMap" class="onlineButton">
				<div class="topButton" v-for="post in commonPost" :class="{textActive:post.active,tabMouseOver:post.isShow}" @click="onlineMapButton(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
					<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
					<div class="description">
						<span>{{post.name}}</span>
					</div>
				</div>
			</router-link>
			<router-link to="/BaiduMap" class="onlineButton">
				<div class="topButton" v-for="post in baiduPost" :class="{textActive:post.active,tabMouseOver:post.isShow}" @click="onlineMapButton(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
					<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
					<div class="description">
						<span>{{post.name}}</span>
					</div>
				</div>
			</router-link>
		</div>
		<div class="description">
			<span>在线地图</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'onlinemap',
  data(){
	return {
		commonPost:[
			{
				name:"高德地图",
				url:require('../assets/mapdownload/Gaode.png'),
				isShow:false,
				type:"commonMap",
				active:true
			},
			{
				name:"谷歌地图",
				url:require('../assets/mapdownload/google.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"OSM地图",
				url:require('../assets/mapdownload/OpenStreetMap.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"天地图",
				url:require('../assets/mapdownload/tianditu.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"必应地图",
				url:require('../assets/mapdownload/bingmap.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"腾讯地图",
				url:require('../assets/mapdownload/tengxun.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"易智瑞",
				url:require('../assets/mapdownload/esri.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"Here地图",
				url:require('../assets/mapdownload/heremap.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
			{
				name:"智图",
				url:require('../assets/mapdownload/zhitu.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
		],
		baiduPost:[
			{
				name:"百度地图",
				url:require('../assets/mapdownload/Baidu.png'),
				isShow:false,
				type:"baiduMap",
				active:false
			},
			// {
			// 	name:"数据发布",
			// 	url:require('../assets/mapdownload/release.png'),
			// 	isShow:false,
			// 	type:"baiduMap",
			// 	active:false
			// },
		]
	}
  },
  methods:{
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
	onlineMapButton(post){
		//功能按钮高亮
		for(let i=0;i<this.commonPost.length;i++){
			if(post.name===this.commonPost[i].name){
				this.commonPost[i].active=true;
			}else{
				this.commonPost[i].active=false;
			}
		}
		for(let i=0;i<this.baiduPost.length;i++){
			if(post.name===this.baiduPost[i].name){
				this.baiduPost[i].active=true;
			}else{
				this.baiduPost[i].active=false;
			}
		}
		// 切换至二维窗口
		this.myCommon.setTwoView(post.type);
		//更新地图类型
		this.myCommon.updateMapType(post.type);
		//清空三维图层
		this.$store.state.viewer.imageryLayers.removeAll();
		//更新列表
		var mapList = this.$store.state.mapList;
		for(let i=0;i<mapList.length;i++){
			if(mapList[i].name===post.name){
				mapList[i].isShow=true;
				for(let j=0;j<mapList[i].urls.length;j++){
					if(j===0){
						mapList[i].urls[j].isActive=true;
						//更新三维场景图层
						this.$store.state.viewer.imageryLayers.addImageryProvider(mapList[i].urls[j].imageProvider);
						//更新地图图层
						var layer = this.myCommon.getLayer();
						var map = this.myCommon.getMap();
						if(layer){
							layer.remove();
						}else{
							return false;
						}
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
			}else{
				mapList[i].isShow=false;
			}
		}
		//设置地图缩放级别
		this.myCommon.setMapZoom();
		//更新下载信息
		this.myCommon.updateNameAndUrl();
	}
  },
}
</script>

<style>
.onlineButton{
	display: flex;
	flex-direction: row;
	flex-wrap:nowrap;
	justify-content:flex-start;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
}
</style>
