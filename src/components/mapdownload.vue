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
import mapdownloadbox from '@/components/mapdownloadbox.vue';
export default {
  name: 'mapdownload',
  components:{
  	mapdownloadbox,
  },
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
		var $this = this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		var temp_data = this.myCommon.isLoginAndTime();
		if(!temp_data.flag){
			this.$message(temp_data.options);
			return temp_data.flag
		}
		if(post.name==="地图下载"){
			//判断是否有范围
			if(this.$store.state.scopeInfo.scopeLayer.length===0){
				this.$alert('当前没有范围', '提示', {confirmButtonText: '确定',}).catch(() => {});
				return false;
			}
			//更新下载表格数据
			this.myCommon.updateDownLoadTable();
			//清空下载级别和比例尺
			this.myCommon.clearZoomAndResolution();
			this.$confirm(<mapdownloadbox ref="mapdownloadbox" />, '地图下载', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				customClass:"mapdownloadClass",
				beforeClose:function(action, instance, done){
					if(action==="close"){
						//初始化矢量下载表单
						$this.$refs.mapdownloadbox.init_vector();
						done();
					}else if(action==="cancel"){
						//初始化矢量下载表单
						$this.$refs.mapdownloadbox.init_vector();
						done();
					}else if(action==="confirm"){
						if($this.$refs.mapdownloadbox.activeName==="1"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.tileNameInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.tileDownInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$store.state.downloadInfo.zoom.length===0){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '请选择下载级别'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.isName){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}else{
								done();
							}
						}else if($this.$refs.mapdownloadbox.activeName==="2"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.demNameInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.demDownInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.isName){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}else{
								done();
							}
						}else if($this.$refs.mapdownloadbox.activeName==="3"){
							var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
							var pathRegex = /[a-zA-Z]:\//;
							if(!taskRegex.test($this.$refs.mapdownloadbox.vectorNameInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '任务名称,格式不正确'
								});
								return false;
							}
							if(!pathRegex.test($this.$refs.mapdownloadbox.vectorDownInput)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '存储地址,格式不正确'
								});
								return false;
							}
							if($this.$refs.mapdownloadbox.is_vector_name){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '该路径下已存在同名文件'
								});
								return false;
							}
							if($this.$store.state.downloadInfo.vector_load_info.dataset_names.length===0){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '请选择下载图层'
								});
								return false;
							}else{
								done();
							}
						}
					}
				}
			}).then(() => {
				if($this.$refs.mapdownloadbox.activeName==="1"){
					//更新下载信息
					$this.myCommon.updateDownLoadInfo($this.$refs.mapdownloadbox);
					var data = $this.$store.state.downloadInfo;
					//更新下载任务表
					$this.myCommon.updateTaskTableDatas(data);
					$this.myCommon.openTaskTable();
					//调用后端下载函数
					downLoad(data);
					async function downLoad(data){
						//python瓦片下载函数
						await eel.tile_load(data)();
					}
					
					
				}else if($this.$refs.mapdownloadbox.activeName==="2"){
					//更新下载信息
					$this.myCommon.updateDownLoadInfo($this.$refs.mapdownloadbox);
					var data = $this.$store.state.downloadInfo;
					//更新下载任务表
					$this.myCommon.updateTaskTableDatas(data);
					$this.myCommon.openTaskTable();
					//调用后端下载函数
					demLoad(data);
					async function demLoad(data){
						//python瓦片下载函数
						await eel.dem_load(data)();
					}
					
				}else if($this.$refs.mapdownloadbox.activeName==="3"){
					//更新矢量下载信息
					var data = $this.$store.state.downloadInfo.vector_load_info;
					data.scope=$this.$store.state.scopeInfo.geojson;
					data.taskName=$this.$refs.mapdownloadbox.vectorNameInput;
					data.savePath=$this.$refs.mapdownloadbox.vectorDownInput;
					data.saveType=$this.$refs.mapdownloadbox.vectorOptionValue;
					data.time = $this.getDate();
					for(let i=0;i<data.dataset_names.length;i++){
						//更新下载任务表
						data.downType=data.dataset_names[i].describe+"osm矢量下载";
						data.id=data.dataset_names[i].id;
						$this.myCommon.updateTaskTableDatas(data);
					}
					// 打开任务下载版面
					$this.myCommon.openTaskTable();
					//调用后端下载函数
					vector_load(data);
					async function vector_load(data){
						//python瓦片下载函数
						await eel.vector_load(data)();
					}
				}
			}).catch(() => {
				
			});
		}else if(post.name==="下载任务"){
			this.myCommon.openTaskTable();
		}
  	},
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
	getDate(){
		var time=new Date().getFullYear() +"/" + (new Date().getMonth()+1)+"/"+new Date().getDate()+" "+new Date().getHours() +":"+ new Date().getMinutes()+":"+new Date().getSeconds();
		return time;
	},
  },
}
</script>

<style lang="less">
.mapdownloadClass{
	width:500px;
	height:500px;
}
</style>
