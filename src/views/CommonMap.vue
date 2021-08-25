<template>
	<div id="commonMap" ></div>
</template>

<script>
export default {
  name: 'CommonMap',
  mounted:function(){
  	//初始加载地图
  	this.initMap();
  },
  methods: {
	initMap(){
		var $this = this;
		var height = parseInt(window.innerHeight)-181;
		$("#commonMap").css("height",height);
		var map_container = this.$store.state.map_container;
		if(map_container.type==="common_map"){
			map_container.map=L.map("commonMap",{
				center: [39.550339, 100.114129],
				zoom: 3,
				minZoom:3,
				maxZoom: 18,
				// maxBounds: L.latLngBounds([
				// 	[-90, -180],
				// 	[90, 180]
				// ]),
				zoomControl: false,
				attributionControl: false,
				keyboard:false
			});
		}else if(map_container.type==="baidu_map"){
			map_container.map=L.map("commonMap",{
				crs:L.CRS.Baidu,
				center:[39.550339, 100.114129],
				zoom:3,
				minZoom:3,
				maxZoom: 18,
				// maxBounds: L.latLngBounds([
				// 	[-90, -180],
				// 	[90, 180]
				// ]),
				zoomControl: false,
				attributionControl: false,
				keyboard:false,
				//开启convas
				preferCanvas: true
			});
		}
		// 初始化地图事件
		this.myCommon.init_map_event();
		//初始化级别指示条
		this.myCommon.init_zoom_slider();
		this.myCommon.unbindMapEvent(map_container.map);
		// L.control.scale({maxWidth:100,metric:true,imperial:false}).addTo(map_container.map);
		window.onresize=function(){
			//地图窗口大小
			map_container.map.invalidateSize(true);
		}
		$this.$message({
			showClose: true,
			type: 'warning',
			message: '地图窗口已初始化'
		});
	}
  },
}
</script>
<style lang="less">
#commonMap{
	width:100%;
}
</style>
