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
			// {
			// 	name:"提等值面",
			// 	url:require('../assets/maptools/surface.png'),
			// 	isShow:false,
			// },
			// {
			// 	name:"清除效果",
			// 	url:require('../assets/maptools/clear.png'),
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
			$this.$confirm(<contourlinebox ref='contourlinebox'/>, '提取等值线', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						$this.$refs.contourlinebox.init_panel();
						done();
					}else if(action==="cancel"){
						$this.$refs.contourlinebox.init_panel();
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
						}
						if($this.$refs.contourlinebox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				// 分析参数
				var data={
					id:$this.$UUID(),
					downType:"提取等值线",
					taskName:$this.$refs.contourlinebox.task_name,
					savePath:$this.$refs.contourlinebox.save_path,
					saveType:$this.$refs.contourlinebox.option_value,
					import_file_path:$this.$refs.contourlinebox.import_file_path,
					time:$this.getDate(),
					progress:0,
					exportProgress:0,
				}
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				isoline_analyze(data);
				async function isoline_analyze(data){
					await eel.isoline_analyze(data)();
					$this.$refs.contourlinebox.init_panel();
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
						$this.$refs.slopebox.init_panel();
						done();
					}else if(action==="cancel"){
						$this.$refs.slopebox.init_panel();
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
						}
						if($this.$refs.slopebox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				// 分析参数
				var data={
					id:$this.$UUID(),
					downType:"坡度分析",
					taskName:$this.$refs.slopebox.task_name,
					savePath:$this.$refs.slopebox.save_path,
					saveType:$this.$refs.slopebox.option_value,
					import_file_path:$this.$refs.slopebox.import_file_path,
					time:$this.getDate(),
					progress:0,
					exportProgress:0,
				}
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				slope_analyze(data);
				async function slope_analyze(data){
					await eel.slope_analyze(data)();
					$this.$refs.slopebox.init_panel();
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
						$this.$refs.aspectbox.init_panel();
						done();
					}else if(action==="cancel"){
						$this.$refs.aspectbox.init_panel();
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
						}
						if($this.$refs.aspectbox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				// 分析参数
				var data={
					id:$this.$UUID(),
					downType:"坡向分析",
					taskName:$this.$refs.aspectbox.task_name,
					savePath:$this.$refs.aspectbox.save_path,
					saveType:$this.$refs.aspectbox.option_value,
					import_file_path:$this.$refs.aspectbox.import_file_path,
					time:$this.getDate(),
					progress:0,
					exportProgress:0,
				}
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				aspect_analyze(data);
				async function aspect_analyze(data){
					await eel.aspect_analyze(data)();
					$this.$refs.aspectbox.init_panel();
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
						$this.$refs.contourpolygonbox.init_panel();
						done();
					}else if(action==="cancel"){
						$this.$refs.contourpolygonbox.init_panel();
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
						}
						if($this.$refs.contourpolygonbox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
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
					$this.$refs.contourpolygonbox.init_panel();
				}
			}).catch(() => {
				
			});
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
