<template>
	<div>
		<el-input v-model="task_name" size="small" placeholder="任务名称" @input="isSameName()"></el-input>
		<el-input v-model="url_name" size="small" placeholder="计算机物理地址,例如:00-15-5D-16-C2-52" class="aliasInputClass"></el-input>
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
		url_name:"",
		save_path:"",
		value:"",
		isName:false,
	}
  },
  methods:{
	savePathChoose(){
	  	var $this =this;
	  	get_export_path();
	  	async function get_export_path(){
	  		$this.save_path =await eel.get_export_path()();
	  	}
	},
	isSameName(){
		var $this =this;
		var path = this.save_path+"\\"+this.task_name;
		is_samename(path);
		async function is_samename(path){
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
