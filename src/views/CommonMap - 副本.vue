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
		var map_list = this.$store.state.mapList;
		if(map_container.type==="common_map"){
			map_container.map=L.map("commonMap",{
				center: map_list[0].center,
				zoom: map_list[0].urls[0].minZoom,
				minZoom:map_list[0].urls[0].minZoom,
				maxZoom: map_list[0].urls[0].maxZoom,
				zoomControl: false,
				attributionControl: false,
			});
			map_container.layer = L.tileLayer.chinaProvider(map_list[0].urls[0].url).addTo(map_container.map);
		}else if(map_container.type==="baidu_map"){
			map_container.map=L.map("commonMap",{
				crs:map_list[9].crs,
				center: map_list[9].center,
				zoom:map_list[9].urls[0].minZoom,
				minZoom:map_list[9].urls[0].minZoom,
				maxZoom: map_list[9].urls[0].maxZoom,
				zoomControl: false,
				attributionControl: false,
			});
			map_container.layer = L.tileLayer.chinaProvider(map_list[9].urls[0].url).addTo(map_container.map);
		}
		// 初始化地图事件
		this.myCommon.init_map_event();
		//初始化级别指示条
		this.myCommon.init_zoom_slider();
		this.myCommon.unbindMapEvent(map_container.map);
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
