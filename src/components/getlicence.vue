<template>
	<div>
		<el-input v-model="task_name" size="small" placeholder="任务名称" @input="isSameName()"></el-input>
		<el-input v-model="save_path" size="small" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="savePathChoose()"></i>
		</el-input>
		<el-calendar class="aliasInputClass" v-model="value">
		</el-calendar>
	</div>
</template>

<script>
export default {
  name: 'getlicence',
  data(){
    return {
		task_name:"",
		save_path:"",
		value:"",
		isName:false,
	}
  },
  methods:{
	savePathChoose(){
	  	var $this =this;
	  	getSavePath();
	  	async function getSavePath(){
	  		$this.save_path =await eel.get_save_path()();
	  	}
	},
	isSameName(){
		var $this =this;
		var path = this.save_path+"\\"+this.task_name;
		is_samename(path);
		async function is_samename(path){
			//python瓦片下载函数
			$this.isName =await eel.is_samename(path)();
		}
	}
  },
}
</script>

<style lang="less">
.aliasInputClass>.el-calendar__body{
	max-height: 200px;
	overflow-y: auto;
}
.el-calendar-table .el-calendar-day{
	height:48px;
	line-height: 48px;
	text-align: center;
}
.el-calendar-table thead th{
	text-align: center;
}
</style>
