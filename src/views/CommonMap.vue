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
		this.$store.state.mapContainer[0].map=L.map("commonMap",{
			center: this.$store.state.mapList[0].center,
			zoom: this.$store.state.mapList[0].urls[0].minZoom,
			minZoom:this.$store.state.mapList[0].urls[0].minZoom,
			maxZoom: this.$store.state.mapList[0].urls[0].maxZoom,
			zoomControl: false,
			attributionControl: false,
			// worldCopyJump:true,
		})
		// L.control.pan().addTo(this.$store.state.mapContainer[0].map);
		// L.control.zoomslider().addTo(this.$store.state.mapContainer[0].map);
		this.$store.state.mapContainer[0].layer = L.tileLayer.chinaProvider(this.$store.state.mapList[0].urls[0].url).addTo(this.$store.state.mapContainer[0].map);
		$this.myCommon.unbindMapEvent(this.$store.state.mapContainer[0].map);
		window.onresize=function(){
			//地图窗口大小
			$this.$store.state.mapContainer[0].map.invalidateSize(true);
		}
	}
  },
}
</script>
<style lang="less">
#commonMap{
	width:100%;
}
</style>
