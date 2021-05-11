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
				name:"提等值面",
				url:require('../assets/maptools/surface.png'),
				isShow:false,
			},
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
			$this.$confirm(<contourlinebox ref='contourlinebox'/>, '提取等值线', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var importRegex = /[a-zA-Z]:\/.(IMG|img|tif)/;
						var pathRegex = /[a-zA-Z]:\//;
						if(!taskRegex.test($this.$refs.contourlinebox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.contourlinebox.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.contourlinebox.save_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '存储地址,格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				//更新下载信息
				$this.myCommon.updateDownLoadInfo($this.$refs.contourlinebox);
				var data = $this.$store.state.downloadInfo;
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				contourLine(data);
				async function contourLine(data){
					await eel.get_contour_line(data)();
				}
			}).catch(() => {
				
			});
		}else if(post.name==="提等值面"){
			$this.$confirm(<contourpolygonbox ref='contourpolygonbox'/>, '提取等值面', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var importRegex = /[a-zA-Z]:\/.(IMG|img|tif)/;
						var pathRegex = /[a-zA-Z]:\//;
						if(!taskRegex.test($this.$refs.contourpolygonbox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.contourpolygonbox.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.contourpolygonbox.save_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '存储地址,格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				//更新下载信息
				$this.myCommon.updateDownLoadInfo($this.$refs.contourpolygonbox);
				var data = $this.$store.state.downloadInfo;
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				contourPolygon(data);
				async function contourPolygon(data){
					await eel.get_contour_polygon(data)();
				}
			}).catch(() => {
				
			});
		}else if(post.name==="坡度分析"){
			$this.$confirm(<slopebox ref='slopebox'/>, '坡度分析', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var importRegex = /[a-zA-Z]:\/.(IMG|img|tif)/;
						var pathRegex = /[a-zA-Z]:\//;
						if(!taskRegex.test($this.$refs.slopebox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.slopebox.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.slopebox.save_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '存储地址,格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				//更新下载信息
				$this.myCommon.updateDownLoadInfo($this.$refs.slopebox);
				var data = $this.$store.state.downloadInfo;
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				getSlope(data);
				async function getSlope(data){
					await eel.get_slope(data)();
				}
			}).catch(() => {
				
			});
		}else if(post.name==="坡向分析"){
			$this.$confirm(<aspectbox ref='aspectbox'/>, '坡向分析', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var importRegex = /[a-zA-Z]:\/.(IMG|img|tif)/;
						var pathRegex = /[a-zA-Z]:\//;
						if(!taskRegex.test($this.$refs.aspectbox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.aspectbox.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.aspectbox.save_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '存储地址,格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				//更新下载信息
				$this.myCommon.updateDownLoadInfo($this.$refs.aspectbox);
				var data = $this.$store.state.downloadInfo;
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				getAspect(data);
				async function getAspect(data){
					await eel.get_aspect(data)();
				}
			}).catch(() => {
				
			});
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
