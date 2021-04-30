<template>
	<div>
		<el-input v-model="task_name" size="small" @input="isSameName()" placeholder="任务名称"></el-input>
		<el-input v-model="save_path" size="small" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="exportFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value2" size="mini" class="aliasInputClass">
			<el-option v-for="post in options2" :labek="post.label" :value="post.value"></el-option>
		</el-select>
		<div></div>
		<el-select v-model="option_value" size="mini" class="aliasInputClass">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'layertreeexportbox',
  data(){
    return {
		type:"export",
		task_name:"",
		save_path:"",
		isName:false,
		option_value:"shp",
		options:[
			{
				value:"shp",
				label:"shp"
			},
			{
				value:"json",
				label:"json"
			},
		],
		option_value2:"84Web墨卡托投影-3857",
		options2:[
			{
				value:"84Web墨卡托投影-3857",
				label:"PCS_WGS_1984_WORLD_MERCATOR"
			},
			{
				value:"84经纬度投影-4326",
				label:"GCS_WGS_1984"
			},
		],
	}
  },
  methods:{
	exportFileChoose(){
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
</style>
