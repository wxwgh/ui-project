<template>
	<div class="taskParent">
		<el-table :data="get_datas" border size="mini" :height="tableHeight">
			<el-table-column prop="id" label="标识" v-if="false"></el-table-column>
			<el-table-column prop="taskName" label="任务名称" show-overflow-tooltip></el-table-column>
			<el-table-column prop="downType" label="数据类型" show-overflow-tooltip></el-table-column>
			<el-table-column prop="time" label="创建时间" show-overflow-tooltip></el-table-column>
			<el-table-column min-width="150" prop="savePath" label="保存地址" show-overflow-tooltip></el-table-column>
			<el-table-column min-width="150" prop="progress" label="下载进度">
				<template slot-scope="scope">
					<el-progress :percentage="scope.row.progress"></el-progress>
				</template>
			</el-table-column>
			<el-table-column min-width="150" prop="exportProgress" label="导出进度">
				<template slot-scope="scope">
					<el-progress :percentage="scope.row.exportProgress"></el-progress>
				</template>
			</el-table-column>
			<el-table-column width="150" min-width="150" label="操作">
				<template slot-scope="scope" >
					<div v-if="scope.row.break_show_flag">
						<!-- 标识为true 表示开始状态 显示暂停按钮 -->
						<el-button icon="el-icon-video-pause" circle size="mini" :disabled="scope.row.task_disable" v-if="scope.row.task_flag" @click="task_stop_click(scope)"></el-button>
						<el-button icon="el-icon-video-play" circle size="mini" :disabled="scope.row.task_disable" v-else @click="task_start_click(scope)"></el-button>
						<el-button icon="el-icon-folder" circle size="mini" @click="openDownFile(scope)"></el-button>
						<el-button icon="el-icon-delete" circle size="mini" @click="deleteTask(scope)"></el-button>
					</div>
					<div v-else>
						<el-button icon="el-icon-folder" circle size="mini" @click="openDownFile(scope)"></el-button>
						<el-button icon="el-icon-delete" circle size="mini" @click="deleteTask(scope)"></el-button>
					</div>
				</template>
			</el-table-column>
		</el-table>
	</div>
</template>

<script>
	export default {
		name: 'downloadattribute',
		data() {
			return {
				tableHeight: "100%",
			}
		},
		computed: {
			get_datas: function() {
				return this.$store.state.taskTableDatas;
			}
		},
		mounted: function() {
			var height = parseInt(window.innerHeight) - 181;
			$(".taskParent").css("height", height);
		},
		methods: {
			//开始按钮
			task_start_click(scope){
				scope.row.task_flag=true;
				scope.row.break_flag=true;
				//调用后台 开启线程
				start_thread(scope.row)
				async function start_thread(data){
					await eel.start_thread(data)();
				}
				//更新开始暂停标识
				this.myCommon.update_task_flag(scope.row.id);
			},
			//暂停按钮
			task_stop_click(scope){
				scope.row.task_flag=false;
				scope.row.break_flag=true;
				//调用后台 暂停线程
				stop_thread(scope.row.id)
				async function stop_thread(id){
					await eel.stop_thread(id)();
				}
				//更新开始暂停标识
				this.myCommon.update_task_flag(scope.row.id);
			},
			deleteTask(data) {
				var $this = this;
				this.$confirm('文件删除后不可恢复, 是否继续?', '删除下载文件', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					closeOnClickModal: false,
					type: 'warning'
				}).then(() => {
					//删除下载任务
					$this.myCommon.deleteTaskTableDatas(data.row);
					//删除文件
					var path = data.row.savePath + "\\" + data.row.taskName;
					deleteFile(path);
					async function deleteFile(path) {
						await eel.delete_file(path)();
					}
				}).catch(() => {

				});
			},
			openDownFile(data) {
				var path = data.row.savePath + "\\" + data.row.taskName;
				openFile(path);
				//打开下载文件夹
				// 调用python中的函数,注意需要在定义前加上async声明异步
				async function openFile(path) {
					await eel.open_file(path)();
				}
			},
		},
	}
</script>

<style lang="less">
	.taskParent {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
	}
</style>
