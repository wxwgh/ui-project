<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in analyzePost" :class="{tabMouseOver:post.isShow}" @click="analyzeClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>地形分析</span>
		</div>
	</div>
</template>

<script>
import contourlinebox from '@/components/contourlinebox.vue';
import contourpolygonbox from '@/components/contourpolygonbox.vue';
import slopebox from '@/components/slopebox.vue';
import aspectbox from '@/components/aspectbox.vue';
export default {
  name: 'analyze',
  data(){
    return {
		analyzePost:[
			{
				name:"坡度分析",
				url:require('../assets/maptools/slope.png'),
				isShow:false,
			},
			{
				name:"坡向分析",
				url:require('../assets/maptools/aspect.png'),
				isShow:false,
			},
			{
				name:"提等值线",
				url:require('../assets/maptools/isoline.png'),
				isShow:false,
			},
			{
				name:"清除效果",
				url:require('../assets/maptools/clear.png'),
				isShow:false,
			},
			// {
			// 	name:"提等值面",
			// 	url:require('../assets/maptools/surface.png'),
			// 	isShow:false,
			// },
		],
	}
  },
  methods:{
  	analyzeClick(post){
		var $this =this;
  		var map = this.myCommon.getMap();
  		this.myCommon.unbindMapEvent(map);
  		this.myCommon.switchMouseStyle(false,map);
  		this.myCommon.clearOperation();
		if(post.name==="提等值线"){
			// 创建一个拥有高程阴影和等高线的组合样式
			function getElevationContourMaterial() {
				return new Cesium.Material({
					fabric: {
						type: 'ElevationColorContour',
						materials: {
							contourMaterial: {
								type: 'ElevationContour'
							},
							elevationRampMaterial: {
								type: 'ElevationRamp'
							}
						},
						components: {
							diffuse: 'contourMaterial.alpha == 0.0 ? elevationRampMaterial.diffuse : contourMaterial.diffuse',
							alpha: 'max(contourMaterial.alpha, elevationRampMaterial.alpha)'
						}
					},
					translucent: false
				});
			}
			var minHeight = -414.0; // 最低接近死海高度
			var maxHeight = 8777.0; // 最高接近珠峰高度
			var contourColor = Cesium.Color.RED.withAlpha(0.4); // 等高线的颜色
			var contourSpacing = 150.0; // 等高线的等间距
			var contourWidth = 1.0; // 等高线的宽度
			
			// 3、高程阴影+等高线
			var material = getElevationContourMaterial();
			var shadingUniforms = material.materials.elevationRampMaterial.uniforms;
			shadingUniforms.minimumHeight = minHeight;
			shadingUniforms.maximumHeight = maxHeight;
			shadingUniforms.image = getColorRamp();
			
			var contourUniforms = material.materials.contourMaterial.uniforms;
			contourUniforms.width = contourWidth;
			contourUniforms.spacing = contourSpacing;
			contourUniforms.color = contourColor;
			
			function getColorRamp() {
				var ramp = document.createElement('canvas');
				ramp.width = 100;
				ramp.height = 1;
				var ctx = ramp.getContext('2d');
				var values = [0.0, 0.045, 0.1, 0.15, 0.37, 0.54, 1.0];
				var grd = ctx.createLinearGradient(0, 0, 100, 0);
				grd.addColorStop(values[0], 'rgba(0,0,0,0.8)'); //black
				grd.addColorStop(values[1], 'rgba(39,71,224,0.8)'); //blue
				grd.addColorStop(values[2], 'rgba(211,59,125,0.8)'); //pink
				grd.addColorStop(values[3], 'rgba(211,48,56,0.8)'); //red
				grd.addColorStop(values[4], 'rgba(255,151,66,0.8)'); //orange
				grd.addColorStop(values[5], 'rgba(255,215,0,0.8)'); //yellow
				grd.addColorStop(values[6], 'rgba(255,255,255,0.8)'); //white
				ctx.fillStyle = grd;
				ctx.fillRect(0, 0, 100, 1);
				return ramp;
			}
			this.$store.state.viewer.scene.globe.material = material;
		}else if(post.name==="坡度分析"){
			var material = Cesium.Material.fromType('SlopeRamp');
			var shadingUniforms = material.uniforms;
			shadingUniforms.image = getColorRamp();
	
			this.$store.state.viewer.scene.globe.material = material;
	
			function getColorRamp() {
				var ramp = document.createElement('canvas');
				ramp.width = 100;
				ramp.height = 1;
				var ctx = ramp.getContext('2d');
				var values = [0.0, 0.29, 0.5, Math.sqrt(2)/2, 0.87, 0.91, 1.0];
				var grd = ctx.createLinearGradient(0, 0, 100, 0);
				grd.addColorStop(values[0], 'rgba(0,0,0,0.8)'); //black
				grd.addColorStop(values[1], 'rgba(39,71,224,0.8)'); //blue
				grd.addColorStop(values[2], 'rgba(211,59,125,0.8)'); //pink
				grd.addColorStop(values[3], 'rgba(211,48,56,0.8)'); //red
				grd.addColorStop(values[4], 'rgba(255,151,66,0.8)'); //orange
				grd.addColorStop(values[5], 'rgba(255,215,0,0.8)'); //yellow
				grd.addColorStop(values[6], 'rgba(255,255,255,0.8)'); //white
				ctx.fillStyle = grd;
				ctx.fillRect(0, 0, 100, 1);
				return ramp;
			}
		}else if(post.name==="坡向分析"){
			var material = Cesium.Material.fromType('AspectRamp');
			var shadingUniforms = material.uniforms;
			shadingUniforms.image = getColorRamp();
	
			this.$store.state.viewer.scene.globe.material = material;
	
			function getColorRamp() {
				var ramp = document.createElement('canvas');
				ramp.width = 100;
				ramp.height = 1;
				var ctx = ramp.getContext('2d');
				var values = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0];
				var grd = ctx.createLinearGradient(0, 0, 100, 0);
				grd.addColorStop(values[0], 'rgba(0,0,0,0.8)'); //black
				grd.addColorStop(values[1], 'rgba(39,71,224,0.8)'); //blue
				grd.addColorStop(values[2], 'rgba(211,59,125,0.8)'); //pink
				grd.addColorStop(values[3], 'rgba(211,48,56,0.8)'); //red
				grd.addColorStop(values[4], 'rgba(255,151,66,0.8)'); //orange
				grd.addColorStop(values[5], 'rgba(255,215,0,0.8)'); //yellow
				grd.addColorStop(values[6], 'rgba(255,255,255,0.8)'); //white
				ctx.fillStyle = grd;
				ctx.fillRect(0, 0, 100, 1);
				return ramp;
			}
		}else if(post.name==="清除效果"){
			this.$store.state.viewer.scene.globe.material = this.$store.state.material;
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

<style lang="less">
</style>
