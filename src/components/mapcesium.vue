<template>
	<div id="mapCesium"></div>
</template>

<script>
export default {
  name: 'mapcesium',
  mounted:function(){
    //初始化三维场景
	this.initMapCesium();
  },
  methods:{
  	initMapCesium(){
		var height = parseInt(window.innerHeight)-181;
		$("#mapCesium").css("height",height);
		var Cesium = this.Cesium;
		Cesium.Ion.defaultAccessToken ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NTQ1MTdmMS1iZmNjLTQ5M2EtYTE2Ni1jMmQzZGFiOGFkN2UiLCJpZCI6MzAxODAsInNjb3BlcyI6WyJhc2wiLCJhc3IiLCJhc3ciLCJnYyIsInByIl0sImlhdCI6MTU5MzMzMjI2OH0.RwENja-T_-cP_OK4ZohAD1Wx76ys4H8xk3A_bfQWmeQ';
		this.$store.state.viewer = new Cesium.Viewer("mapCesium", {
			animation: false,  //是否显示动画控件
	        baseLayerPicker: false, //是否显示图层选择控件
	        geocoder: false, //是否显示地名查找控件
	        timeline: false, //是否显示时间线控件
	        sceneModePicker: false, //是否显示投影方式控件
	        navigationHelpButton: false, //是否显示帮助信息控件
	        infoBox: false, //是否显示点击要素之后显示的信息
			fullscreenButton:false,//隐藏右下角全屏按钮
			homeButton:false,//右上角家功能
	        imageryProvider : new Cesium.UrlTemplateImageryProvider({
	            url: "http://webrd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
	        }),
			terrainProvider:new Cesium.CesiumTerrainProvider({
				//CesiumLab提供的世界12级地形
				// url:"https://lab.earthsdk.com/terrain/42752d50ac1f11e99dbd8fd044883638"
				//CesiumLab提供的中国14级地形
				url:"https://lab.earthsdk.com/terrain/577fd5b0ac1f11e99dbd8fd044883638",
				requestVertexNormals: true,
				requestWaterMask: true
			})
	    });
		//开启深度测试
		this.$store.state.viewer.scene.globe.enableLighting = true;
		this.$store.state.material = this.$store.state.viewer.scene.globe.material;
		//隐藏logo
		$(".cesium-viewer-bottom").css("display","none");
		this.$store.state.viewer.camera.setView({
		    destination : Cesium.Cartesian3.fromDegrees(100.114129, 39.550339, 26000000.0)
		});
  	},
  },
}
</script>

<style lang="less">
#mapCesium{
	width:100%;
}
</style>
