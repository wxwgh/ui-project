<template>
	<div id="baiduMap"></div>
</template>

<script>
export default {
  name: 'BaiduMap',
  mounted:function(){
  	//初始加载地图
  	this.initMap();
  },
  methods: {
	initMap(){
		var $this = this;
		var height = parseInt(window.innerHeight)-181;
		$("#baiduMap").css("height",height);
		this.$store.state.mapContainer[1].map=L.map("baiduMap",{
			crs:this.$store.state.mapList[this.$store.state.mapList.length-1].crs,
			center: this.$store.state.mapList[this.$store.state.mapList.length-1].center,
			zoom: this.$store.state.mapList[this.$store.state.mapList.length-1].urls[0].minZoom+2,
			minZoom:this.$store.state.mapList[this.$store.state.mapList.length-1].urls[0].minZoom,
			maxZoom: this.$store.state.mapList[this.$store.state.mapList.length-1].urls[0].maxZoom,
			zoomControl: false,
			attributionControl: false,
		});
		// L.control.pan().addTo(this.$store.state.mapContainer[1].map);
		// L.control.zoomslider().addTo(this.$store.state.mapContainer[1].map);
		this.$store.state.mapContainer[1].layer = L.tileLayer.chinaProvider(this.$store.state.mapList[this.$store.state.mapList.length-1].urls[0].url).addTo(this.$store.state.mapContainer[1].map);
		window.onresize=function(){
			$this.$store.state.mapContainer[1].map.invalidateSize(true);
		}
	}
  },
}
</script>

<style lang="less">
#baiduMap{
	width: 100%;
}
</style>
