<template>
	<el-tabs v-model="activeName">
	    <el-tab-pane label="影像下载" name="1">
			<el-input id="tileNameId" v-model="tileNameInput" @input="isSameName()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="tileDownInput" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="fileChoose()"></i>
			</el-input>
			<div class="radio_checkbox_parent">
				<el-checkbox v-model="tile_is_clip">边界剪裁</el-checkbox>
				<el-radio v-model="tile_radio" label="原始瓦片">原始瓦片</el-radio>
				<el-radio v-model="tile_radio" label="拼接大图">拼接大图</el-radio>
			</div>
			<el-table border :data="tableDatas" ref="down_table" size="mini" max-width="100%" :max-height="tableHeight">
				<el-table-column type="selection" width="40"></el-table-column>
				<el-table-column prop="level" label="级别" width="50"></el-table-column>
				<el-table-column prop="scale" label="比例尺" min-width="80"></el-table-column>
				<el-table-column prop="dpi" label="DPI" width="50" v-if="false"></el-table-column>
				<el-table-column prop="resolution" label="分辨率" width="100"></el-table-column>
				<el-table-column prop="total" label="瓦片总数" min-width="80"></el-table-column>
				<el-table-column prop="downsize" label="下载大小"></el-table-column>
			</el-table>
		</el-tab-pane>
	    <el-tab-pane label="高程下载" name="2" :disabled="get_dem_able">
			<el-input v-model="demNameInput" @input="isSameName()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="demDownInput" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder"></i>
			</el-input>
			<el-select v-model="demOptionValue" size="mini" class="demSelectClass">
				<el-option v-for="post in demOptions" :labek="post.label" :value="post.value"></el-option>
			</el-select>
		</el-tab-pane>
	    <!-- <el-tab-pane label="POI下载" name="3" :disabled="get_poi_able">
			<el-input v-model="poi_name" @input="isSameName()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="poi_save_path" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="fileChoose()"></i>
			</el-input>
			<el-input v-model="poi_search_name" size="mini" placeholder="搜索关键字" class="poi_input_class"></el-input>
			<div></div>
			<el-select v-model="poi_save_format" size="mini" class="poi_select_class">
				<el-option v-for="post in poi_save_format_options" :labek="post.label" :value="post.value"></el-option>
			</el-select>
		</el-tab-pane> -->
    </el-tabs>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'mapdownloadbox',
  data(){
    return {
		activeName:'1',
		tableHeight:"223",
		isName:false,
		tileNameInput:"",
		tileDownInput:"D:/SuperMap DownLoad",
		tile_is_clip:false,
		tile_radio:"原始瓦片",
		demNameInput:"",
		demDownInput:"D:/SuperMap DownLoad",
		demOptionValue:"img",
		demOptions:[
			{
				value:"img",
				label:"img"
			},
		],
		//poi下载相关变量
		poi_name:"",
		poi_search_name:"",
		poi_save_path:"D:/SuperMap DownLoad",
		poi_save_format:"shp",
		is_poi_name:false,
		poi_save_format_options:[
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
		tableDatas:$store.state.downloadTableDatas,
	}
  },
  computed:{
  	  get_poi_able:function(){
  		  return $store.state.down_load_able.is_poi_able;
  	  },
  	  get_dem_able:function(){
  		  return $store.state.down_load_able.is_dem_able;
  	  },
  },
  methods:{
	//初始化poi下载面板
	init_poi_panel(){
		this.poi_name="";
		this.poi_save_path="D:/SuperMap DownLoad";
		this.poi_save_format="shp";
		this.is_poi_name=false;
		this.poi_search_name="";
	},
	//初始化影像下载面板
	init_tile_panel(){
		this.tileNameInput="";
		this.tileDownInput="D:/SuperMap DownLoad";
		this.tile_is_clip=false;
		this.tileOptionValue="png";
		this.tileOptions=[
			{
				value:"png",
				label:"png"
			}
		];
		this.$refs.down_table.clearSelection();
	},
	//初始化高程下载面板
	init_dem_panel(){
		this.demNameInput="";
		this.demDownInput="D:/SuperMap DownLoad";
		this.demOptionValue="img";
	},
	//文件路径选取
	fileChoose(){
		var $this =this;
		get_export_path();
		async function get_export_path(){
			if($this.activeName==="1"){
				$this.tileDownInput =await eel.get_export_path()();
			}else if($this.activeName==="2"){
				$this.demDownInput =await eel.get_export_path()();
			}else if($this.activeName==="3"){
				$this.poi_save_path =await eel.get_export_path()();
			}
		}
	},
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
	isSameName(){
		var $this =this;
		var path ="";
		if($this.activeName==="1"){
			path = this.tileDownInput+"\\"+this.tileNameInput;
		}else if($this.activeName==="2"){
			path = this.demDownInput+"\\"+this.demNameInput;
		}else if($this.activeName==="3"){
			path = this.poi_save_path+"\\"+this.poi_name;
		}
		is_samename(path);
		async function is_samename(path){
			if($this.activeName==="1"){
				$this.isName =await eel.is_samename(path)();
			}else if($this.activeName==="2"){
				$this.isName =await eel.is_samename(path)();
			}else if($this.activeName==="3"){
				$this.is_poi_name =await eel.is_samename(path)();
			}
		}
	}
  },
}
</script>

<style lang="less">
.radio_checkbox_parent{
	line-height:40px;
	border-top: 1px solid #DCDFE6;
}
.downnameClass{
	margin-top: 15px;
}
.downloadClass{
	margin-top: 10px;
	margin-bottom: 10px;
}
.tileSelectClass{
	margin-left:10px;
	margin-bottom: 10px;
}
.demSelectClass{
	margin-bottom: 233px;
}

//poi下载样式
.poi_select_class{
	margin-top:10px;
	margin-bottom: 195px;
}
.poi_input_class{
	width:30%;
}
</style>
