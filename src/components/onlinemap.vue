<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<!-- <router-link to="/CommonMap" class="onlineButton">
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
			</router-link> -->
			<div class="topButton" v-for="post in commonPost" :class="{textActive:post.active,tabMouseOver:post.isShow}" @click="onlineMapButton(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>在线地图</span>
		</div>
	</div>
</template>

<script>
import custommaplistbox from '@/components/custommaplistbox.vue';
export default {
  name: 'onlinemap',
  components:{
  	custommaplistbox,
  },
  inject:["reload"],
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
			{
				name:"百度地图",
				url:require('../assets/mapdownload/Baidu.png'),
				isShow:false,
				type:"baiduMap",
				active:false
			},
			{
				name:"我的地图",
				url:require('../assets/mapdownload/release.png'),
				isShow:false,
				type:"commonMap",
				active:false
			},
		],
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
		var $this =this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		// 功能按钮高亮
		for(let i=0;i<this.commonPost.length;i++){
			if(post.name===this.commonPost[i].name){
				this.commonPost[i].active=true;
			}else{
				this.commonPost[i].active=false;
			}
		}
		//更新地理列表显示区域
		var mapList = this.$store.state.mapList;
		var custom_map_list = this.$store.state.custom_map_list[0];
		if(post.name==="我的地图"){
			custom_map_list.is_show = true;
			//隐藏固定地图列表
			for(let i=0;i<mapList.length;i++){
				mapList[i].isShow = false;
			}
		}else{
			for(let i=0;i<mapList.length;i++){
				if(mapList[i].name===post.name){
					mapList[i].isShow=true;
				}else{
					mapList[i].isShow=false;
				}
			}
			custom_map_list.is_show = false;
		}
		if(post.name==="百度地图"){
			if(this.$store.state.map_container.type!=="baidu_map"){
				this.$store.state.map_container.type="baidu_map";
				if(this.$store.state.tabActionName === "1" || this.$store.state.tabActionName === "first"){
					//刷新地图窗口
					this.reload();
					this.myCommon.clear_layers();
					this.$store.state.is_init_map = false;
				}else{
					this.$store.state.is_init_map = true;
				}
			}else{
				this.$store.state.is_init_map = false;
			}
		}else{
			if(this.$store.state.map_container.type!=="common_map"){
				this.$store.state.map_container.type="common_map";
				if(this.$store.state.tabActionName === "1" || this.$store.state.tabActionName === "first"){
					//刷新地图窗口
					this.reload();
					this.myCommon.clear_layers();
					this.$store.state.is_init_map = false;
				}else{
					this.$store.state.is_init_map = true;
				}
			}else{
				this.$store.state.is_init_map = false;
			}
			// this.$router.push('/CommonMap');
		}
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
