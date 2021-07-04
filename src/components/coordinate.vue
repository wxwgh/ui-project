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
			// {
			// 	name:"投影转换",
			// 	url:require('../assets/maptools/coordinate.png'),
			// 	isShow:false,
				
			// },
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
		}else if(post.name==="投影转换"){
			$this.$confirm(<coordinatetransitionbox ref='coordinatetransitionbox'/>, '投影转换', {
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
						var importRegex = /(\.tif)/;
						if(!taskRegex.test($this.$refs.coordinatetransitionbox.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if(!importRegex.test($this.$refs.coordinatetransitionbox.import_file_path)){
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
						if($this.$refs.coordinatetransitionbox.option_value===""){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '源坐标系不能为空'
							});
							return false;
						}
						if($this.$refs.coordinatetransitionbox.option_value2===""){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '目标坐标系不能为空'
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
				var source = ""
				for(let i=0;i<$this.$refs.coordinatetransitionbox.options.length;i++){
					if($this.$refs.coordinatetransitionbox.option_value===$this.$refs.coordinatetransitionbox.options[i].value){
						source = $this.$refs.coordinatetransitionbox.options[i].label;
					}
				}
				var target=""
				for(let i=0;i<$this.$refs.coordinatetransitionbox.options2.length;i++){
					if($this.$refs.coordinatetransitionbox.option_value2===$this.$refs.coordinatetransitionbox.options2[i].value){
						target = $this.$refs.coordinatetransitionbox.options2[i].label;
					}
				}
				// 坐标转换功能参数
				var info={
					id:$this.$UUID(),
					import_file_path:$this.$refs.coordinatetransitionbox.import_file_path,
					downType:"投影转换",
					taskName:$this.$refs.coordinatetransitionbox.task_name,
					savePath:$this.$refs.coordinatetransitionbox.save_path,
					source:source,
					target:target,
					export_format:$this.$refs.coordinatetransitionbox.export_format,
					time:$this.myCommon.getDate(),
				}
				console.log(info);
				//更新下载任务表
				$this.myCommon.updateTaskTableDatas(info);
				$this.myCommon.openTaskTable();
				//调用后端处理函数
				tif_coordinate_trans(info);
				async function tif_coordinate_trans(info){
					await eel.tif_coordinate_trans(info)();
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
