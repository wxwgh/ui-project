<template>
	<div>
		<el-input v-model="task_name" size="small" @input="isSameName()" placeholder="任务名称"></el-input>
		<el-input v-model="save_path" size="small" @input="save_change()" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="exportFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value2" @change="is_need_seven(option_value2)" size="mini" class="aliasInputClass">
			<el-option v-for="post in options2" :label="post.label" :value="post.value" :disabled="post.disabled"></el-option>
		</el-select>
		<div class="seven_title"><span :class="{'on_need':on_need,'off_need':off_need}">七参数设置</span></div>
		<div class="seven_parent">
			<el-input v-model="seven.x" :disabled="off_need" class="seven_class" size="small" placeholder="△x平移"></el-input>
			<el-input v-model="seven.y" :disabled="off_need" class="seven_class" size="small" placeholder="△y平移"></el-input>
			<el-input v-model="seven.z" :disabled="off_need" class="seven_class" size="small" placeholder="△z平移"></el-input>
		</div>
		<div class="seven_parent">
			<el-input v-model="seven.alpha" :disabled="off_need" class="seven_class" size="small" placeholder="△α旋转"></el-input>
			<el-input v-model="seven.beta" :disabled="off_need" class="seven_class" size="small" placeholder="△β旋转"></el-input>
			<el-input v-model="seven.gamma" :disabled="off_need" class="seven_class" size="small" placeholder="△γ旋转"></el-input>
		</div>
		<el-input v-model="seven.k" :disabled="off_need" class="seven_class" size="small" placeholder="k缩放"></el-input>
		<div></div>
		<el-select v-model="option_value" size="mini" class="aliasInputClass" @change="select_change()">
			<el-option v-for="post in options" :label="post.label" :value="post.value"></el-option>
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
		seven:{
			x:"",
			y:"",
			z:"",
			alpha:"",
			beta:"",
			gamma:"",
			k:"",
		},
		on_need:false,
		off_need:true,
		task_name:"",
		save_path:"C:/MapDownLoad",
		isName:false,
		option_value:"shp",
		options:[
			{
				value:"shp",
				label:"shp"
			},
			{
				value:"kml",
				label:"kml"
			},
			{
				value:"csv",
				label:"csv"
			},
		],
		option_value2:"",
		options2:[
			{
				label:"WGS 84",
				value:"4326",
				disabled:false
			},
			{
				label:"WGS 84 / Pseudo-Mercator",
				value:"3857",
				disabled:false
			},
			{
				label:"Beijing 1954",
				value:"4214",
				disabled:false
			},
			{
				label:"Beijing 1954 / Gauss-Kruger zone 15",
				value:"21415",
				disabled:false
			},
			{
				label:"Xian 1980",
				value:"4610",
				disabled:false
			},
			{
				label:"Xian 1980 / Gauss-Kruger zone 15",
				value:"2329",
				disabled:false
			},
			{
				label:"China Geodetic Coordinate System 2000",
				value:"4490",
				disabled:false
			},
			{
				label:"CGCS2000 / Gauss-Kruger zone 15",
				value:"4493",
				disabled:false
			},
		],
	}
  },
  methods:{
	// 初始化导出界面
	init_export(){
		this.option_value2 = "";
		this.option_value = "shp";
		this.task_name = "";
		this.save_path = "C:/MapDownLoad";
		this.isName = false;
		this.on_need = false;
		this.off_need = true;
		this.seven={
			x:"",
			y:"",
			z:"",
			alpha:"",
			beta:"",
			gamma:"",
			k:"",
		}
		for(let i=0;i<this.options2.length;i++){
			this.options2[i].disabled = false;
		}
	},
	// 根据保存格式 限制坐标系类型
	select_change(){
		var $this = this;
		if(this.option_value === "kml"){
			this.option_value2 = "4326";
			for(let i=0;i<this.options2.length;i++){
				if(this.options2[i].value !== "4326"){
					this.options2[i].disabled = true;
				}
			}
		}else{
			for(let i=0;i<this.options2.length;i++){
				this.options2[i].disabled = false;
			}
		}
	},
	// 判断是否需要七参数
	is_need_seven(value){
		var $this = this;
		// 源坐标系
		var source_coordinate = $store.state.layerSelectInfo.coordinate;
		//目标坐标系
		var target_coordinate = "";
		for(let i = 0;i<this.options2.length;i++){
			if(value === this.options2[i].value){
				target_coordinate = this.options2[i].value;
			}
		}
		console.log(source_coordinate);
		console.log(target_coordinate);
		//判断是否是 相同基准坐标系
		is_same_geo(source_coordinate,target_coordinate);
		async function is_same_geo(source_coordinate,target_coordinate){
			var is_same = await eel.is_same_geo(source_coordinate ,target_coordinate)();
			if(is_same == 0){
				$this.on_need = true;
				$this.off_need = false;
			}else{
				$this.on_need = false;
				$this.off_need = true;
			}
		}
	},
	exportFileChoose(){
		var $this =this;
		get_export_path();
		async function get_export_path(){
			$this.save_path =await eel.get_export_path()();
		}
	},
	save_change(){
		this.isSameName();
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
.seven_title{
	margin-top: 5px;
}
.seven_class{
	margin-top: 5px;
	width: 33%;
}
.seven_parent{
	display: flex;
	flex-direction: row;
	flex-wrap:nowrap;
	justify-content:space-between;
	overflow: hidden;
}
.on_need{
	color:#409EFF;
}
.off_need{
	color:#C0C4CC;
}

</style>
