<template>
	<div>
		<el-input v-model="task_name" @input="isSameName()" size="small" placeholder="任务名称"></el-input>
		<el-input v-model="import_file_path" size="small" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-input v-model="save_path" size="small" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="savePathChoose()"></i>
		</el-input>
		<el-select v-model="option_value" size="small" class="aliasInputClass" @change="option_change">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
	</div>
</template>

<script>
export default {
  name: 'coordinatetransitionbox',
  data(){
    return {
		type:"coordinate",
		task_name:"",
		import_file_path:"",
		save_path:"D:/SuperMap DownLoad",
		option_value:"84坐标系",
		option_label:"PCS_WGS_1984_UTM_49N",
		saveType:"shp",
		isName:false,
		options:[
			{
				value:"84坐标系",
				label:"PCS_WGS_1984_UTM_49N"
			},
			{
				value:"国家大地2000",
				label:"PCS_CHINA_2000_GK_13"
			},
			{
				value:"西安80",
				label:"PCS_XIAN_1980_GK_13"
			},
			{
				value:"北京54",
				label:"PCS_BEIJING_1954_GK_13"
			},
		],
	}
  },
  methods:{
	//初始化
	initCoordinate(){
		this.task_name="";
		this.import_file_path="";
	},
	option_change(name){
		for(let i=0;i<this.options.length;i++){
			if(this.options[i].value === name){
				this.option_label = this.options[i].label;
				break;
			}
		}
	},
	savePathChoose(){
		var $this =this;
		getSavePath();
		async function getSavePath(){
			$this.save_path =await eel.get_save_path()();
		}
	},
	importFileChoose(){
		var $this =this;
		getFilePath();
		async function getFilePath(){
			$this.import_file_path =await eel.get_shape_path()();
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
</style>
