<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in mapDownLoadPost" :class="{tabMouseOver:post.isShow}" @click="downLoadClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>下载相关</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'mapdownload',
  data(){
    return {
		mapDownLoadPost:[
			{
				name:"地图下载",
				url:require('../assets/mapdownload/vector.png'),
				isShow:false,
				
			},
			{
				name:"下载任务",
				url:require('../assets/mapdownload/DownLoadManager.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
  	downLoadClick(post){
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
