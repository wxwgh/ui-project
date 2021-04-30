<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in showSetPost" :class="{tabMouseOver:post.isShow}" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>显示设置</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'showset',
  data(){
    return {
		showSetPost:[
			{
				name:"经纬格网",
				url:require('../assets/vectorplot/mapgrid.png'),
				isShow:false,
				
			},
			{
				name:"自定格网",
				url:require('../assets/vectorplot/custom.png'),
				isShow:false,
				
			},
			{
				name:"标准分幅",
				url:require('../assets/vectorplot/standard.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
  	showSetClick(post){
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
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
