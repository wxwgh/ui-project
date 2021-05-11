<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in coordinatePost" :class="{tabMouseOver:post.isShow}" @click="coordinateClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>坐标转换</span>
		</div>
	</div>
</template>

<script>
import dfmtransitionbox from '@/components/dfmtransitionbox.vue';
import coordinatetransitionbox from '@/components/coordinatetransitionbox.vue';
export default {
  name: 'coordinate',
  components:{
  	dfmtransitionbox,
	coordinatetransitionbox
  },
  data(){
    return {
		coordinatePost:[
			{
				name:"投影转换",
				url:require('../assets/maptools/coordinate.png'),
				isShow:false,
				
			},
			{
				name:"度分转换",
				url:require('../assets/maptools/limit.png'),
				isShow:false,
			},
		],
	}
  },
  methods:{
  	coordinateClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		if(post.name==="度分转换"){
			this.$confirm(<dfmtransitionbox ref="dfmtransitionbox" />, '度分秒转换', {
			    showCancelButton:false,
			    showConfirmButton:false,
				closeOnClickModal:false
			}).then(() => {
			}).catch(() => {
				
			});
		}else if(post.name==="坐标转换"){
			$this.$confirm(<coordinatetransitionbox ref='coordinatetransitionbox'/>, '坐标转换', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						$this.$refs.coordinatetransitionbox.initCoordinate();
						done();
					}else if(action==="cancel"){
						$this.$refs.coordinatetransitionbox.initCoordinate();
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var pathRegex = /[a-zA-Z]:\//;
						if(!taskRegex.test($this.$refs.coordinatetransitionbox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.coordinatetransitionbox.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if($this.$refs.coordinatetransitionbox.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.coordinatetransitionbox.save_path)){
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
				var data = $this.$store.state.downloadInfo.coordinate_trans_info;
				data.id=$this.$UUID();
				data.url=$this.$refs.coordinatetransitionbox.import_file_path;
				data.downType="坐标转换";
				data.taskName=$this.$refs.coordinatetransitionbox.task_name;
				data.savePath=$this.$refs.coordinatetransitionbox.save_path;
				data.coordinate = $this.$refs.coordinatetransitionbox.option_label;
				data.saveType=$this.$refs.coordinatetransitionbox.saveType;
				data.time=$this.myCommon.getDate();
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(data);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				coordinateTransition(data);
				async function coordinateTransition(data){
					await eel.coordinate_transition(data)();
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
