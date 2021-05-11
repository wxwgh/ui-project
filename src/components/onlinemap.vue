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
				name:"服务发布",
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
		if(post.name==="服务发布"){
			$this.$confirm(<custommaplistbox ref='custommaplistbox'/>, '服务发布', {
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
				//添加服务 至全局对象
				var temp = {
					id:$this.$UUID(),
					name:"自定义-"+$this.$refs.custommaplistbox.map_name,
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
					url:"CusTom.Normal."+$this.$refs.custommaplistbox.map_name,
					realUrl:$this.$refs.custommaplistbox.map_url,
					imageProvider:{url:$this.$refs.custommaplistbox.map_url},
				};
				$this.$store.state.custom_map_list.push(temp);
				//添加至provider对象
				L.TileLayer.ChinaProvider.providers.CusTom.Normal[$this.$refs.custommaplistbox.map_name] = $this.$refs.custommaplistbox.map_url;
				L.TileLayer.ChinaProvider.providers.CusTom["Subdomains"]=[];
				//添加服务 至indexed
				var id = $this.$store.state.custom_map_list_id;
				$this.myCommon.addIndexedDB(id,temp);
				$(".mapListBottom span").each(function(){
					if($(this).text()==="自定义地图列表"){
						$(this).trigger("click");
					}
				});
				$this.$refs.custommaplistbox.init_custommaplistbox();
			}).catch(() => {
				
			});
		}else{
			//功能按钮高亮
			for(let i=0;i<this.commonPost.length;i++){
				if(post.name===this.commonPost[i].name){
					this.commonPost[i].active=true;
				}else{
					this.commonPost[i].active=false;
				}
			}
			if(post.name==="百度地图"){
				this.$store.state.map_container.type="baidu_map";
				//刷新地图窗口
				this.reload();
			}else{
				if(this.$store.state.map_container.type!=="common_map"){
					this.$store.state.map_container.type="common_map";
					//刷新地图窗口
					this.reload();
				}
				// this.$router.push('/CommonMap');
			}
			this.myCommon.set_down_load_able(post.name);
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
							this.$store.state.map_container.layer = layer;
						}else{
							mapList[i].urls[j].isActive=false;
						}
					}
				}else{
					mapList[i].isShow=false;
				}
			}
			//设置地图缩放级别
			//this.myCommon.setMapZoom();
			//更新下载信息
			this.myCommon.updateNameAndUrl();
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
