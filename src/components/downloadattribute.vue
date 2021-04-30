<template>
	<div class="taskParent">
		<el-table :data="tableDatas" border size="mini" :height="tableHeight">
			<el-table-column prop="id" label="标识" v-if="false"></el-table-column>
			<el-table-column prop="taskName" label="任务名称"></el-table-column>
			<el-table-column prop="downType" label="数据类型"></el-table-column>
			<el-table-column prop="time" label="创建时间"></el-table-column>
			<el-table-column min-width="150" prop="savePath" label="保存地址"></el-table-column>
			<el-table-column min-width="150" prop="progress" label="下载进度">
				<template slot-scope="scope">
					<el-progress :percentage="scope.row.progress" ></el-progress>
				</template>
			</el-table-column>
			<el-table-column min-width="150" prop="exportProgress" label="导出进度">
				<template slot-scope="scope">
					<el-progress :percentage="scope.row.exportProgress" ></el-progress>
				</template>
			</el-table-column>
			<el-table-column width="150" min-width="150" label="操作" >
				<template slot-scope="scope">
					<el-button icon="el-icon-folder" circle size="mini" @click="openDownFile(scope)"></el-button>
					<el-button icon="el-icon-delete" circle size="mini" @click="deleteTask(scope)"></el-button>
				</template>
			</el-table-column>
		</el-table>
	</div>
</template>

<script>
export default {
  name: 'downloadattribute',
  data(){
    return {
		tableHeight:"100%",
		tableDatas:this.$store.state.taskTableDatas,
	}
  },
  mounted:function(){
 	var height = parseInt(window.innerHeight)-181;
 	$(".taskParent").css("height",height);
  },
  methods:{
	deleteTask(data){
		var $this = this;
		this.$confirm('文件删除后不可恢复, 是否继续?', '删除下载文件', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			type: 'warning'
		}).then(() => {
			//删除下载任务
			$this.myCommon.deleteTaskTableDatas(data.row);
			//删除文件
			var path = data.row.savePath+"\\"+data.row.taskName;
			deleteFile(path);
			async function deleteFile(path){
				await eel.delete_file(path)();
			}
		}).catch(() => {
			
		});
	},
	openDownFile(data){
		var path = data.row.savePath+"\\"+data.row.taskName;
		openFile(path);
		//打开下载文件夹
		// 调用python中的函数,注意需要在定义前加上async声明异步
		async function openFile(path){
			await eel.open_file(path)();
		}
	},
  },
}
</script>

<style lang="less">
.taskParent{
	width: 100%;
	height:100%;
	display: flex;
	flex-direction: column;
	justify-content:flex-start;
}
</style>
