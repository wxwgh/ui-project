<template>
	<el-tabs v-model="activeName">
	    <el-tab-pane label="瓦片下载" name="1">
			<el-input id="tileNameId" v-model="tileNameInput" @input="isSameName()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="tileDownInput" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="fileChoose()"></i>
			</el-input>
			<el-checkbox v-model="tileChecked" @change="isJoin()">拼接大图</el-checkbox>
			<el-select v-model="tileOptionValue" size="mini" class="tileSelectClass">
				<el-option v-for="post in tileOptions" :labek="post.label" :value="post.value"></el-option>
			</el-select>
			<el-table border :data="tableDatas" size="mini" max-width="100%" :max-height="tableHeight" @select-all="tileSelectAll" @select="tileSelect">
				<el-table-column type="selection" width="40"></el-table-column>
				<el-table-column prop="level" label="级别" width="50"></el-table-column>
				<el-table-column prop="scale" label="比例尺" min-width="80"></el-table-column>
				<el-table-column prop="dpi" label="DPI" width="50" v-if="false"></el-table-column>
				<el-table-column prop="resolution" label="分辨率" width="100"></el-table-column>
				<el-table-column prop="total" label="瓦片总数" min-width="80"></el-table-column>
				<el-table-column prop="downsize" label="下载大小"></el-table-column>
			</el-table>
		</el-tab-pane>
	    <el-tab-pane label="高程下载" name="2">
			<el-input v-model="demNameInput" @input="isSameName()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="demDownInput" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder"></i>
			</el-input>
			<el-select v-model="demOptionValue" size="mini" class="demSelectClass">
				<el-option v-for="post in demOptions" :labek="post.label" :value="post.value"></el-option>
			</el-select>
		</el-tab-pane>
	    <el-tab-pane label="矢量下载" name="3">
			<el-input v-model="vectorNameInput" @input="is_vector_same_name()" size="small" placeholder="任务名称" class="downnameClass"></el-input>
			<el-input v-model="vectorDownInput" size="small" placeholder="存储目录" class="downloadClass">
				<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="fileChoose()"></i>
			</el-input>
			<el-select v-model="vectorOptionValue" size="mini" class="vectorSelectClass">
				<el-option v-for="post in vectorOptions" :labek="post.label" :value="post.value"></el-option>
			</el-select>
			<el-table ref="vector_table" border :data="vectorDatas" size="mini" max-width="100%" :max-height="tableHeight" @select-all="vectorSelectAll" @select="vectorSelect">
				<el-table-column type="selection" width="40"></el-table-column>
				<el-table-column prop="layer_type" label="类别" width="80"></el-table-column>
				<el-table-column prop="data_type" label="类型" width="50"></el-table-column>
				<el-table-column prop="describe" label="说明" ></el-table-column>
				<el-table-column prop="data_code" label="数据集名称" v-if="false"></el-table-column>
			</el-table>
		</el-tab-pane>
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
		tileChecked:false,
		tileOptionValue:"png",
		demNameInput:"",
		demDownInput:"D:/SuperMap DownLoad",
		demOptionValue:"img",
		vectorNameInput:"",
		vectorDownInput:"D:/SuperMap DownLoad",
		vectorOptionValue:"shp",
		is_vector_name:false,
		tileOptions:[
			{
				value:"png",
				label:"png"
			}
		],
		demOptions:[
			{
				value:"img",
				label:"img"
			},
		],
		vectorOptions:[
			{
				value:"shp",
				label:"shp"
			}
		],
		tableDatas:$store.state.downloadTableDatas,
		vectorDatas:[
			{
				layer_type:"建筑",
				data_type:"面",
				describe:"商业建筑,宗教建筑,商场,广场",
				data_code:"buildings"
			},
			{
				layer_type:"土地利用",
				data_type:"面",
				describe:"公园,商业用地,住宅,农田,森林,自然保护区,工业区",
				data_code:"landuse"
			},
			{
				layer_type:"自然资源",
				data_type:"面",
				describe:"冰川,海滩,山泉",
				data_code:"naturals"
			},
			{
				layer_type:"绿地",
				data_type:"面",
				describe:"村庄,岛屿,郊区",
				data_code:"places"
			},
			{
				layer_type:"宗教",
				data_type:"面",
				describe:"宗教建筑",
				data_code:"pofw"
			},
			{
				layer_type:"兴趣点",
				data_type:"点",
				describe:"餐饮,宾馆,购物,交通设施",
				data_code:"pois"
			},
			{
				layer_type:"铁路",
				data_type:"线",
				describe:"铁路网",
				data_code:"railways"
			},
			{
				layer_type:"公路",
				data_type:"线",
				describe:"公路网",
				data_code:"roads"
			},
			{
				layer_type:"交通枢纽",
				data_type:"面",
				describe:"码头,停车场",
				data_code:"traffic"
			},
			{
				layer_type:"运输",
				data_type:"面",
				describe:"汽车站,机场",
				data_code:"transport"
			},
			{
				layer_type:"水系",
				data_type:"面",
				describe:"水库,河堤",
				data_code:"water"
			},
		]
	}
  },
  methods:{
	//初始化矢量下载表单
	init_vector(){
		this.$refs.vector_table.clearSelection();
		this.vectorNameInput="";
		this.vectorDownInput="D:/SuperMap DownLoad";
		
	},
	is_vector_same_name(){
		var $this =this;
		var path = this.vectorDownInput+"\\"+this.vectorNameInput;
		is_samename(path);
		async function is_samename(path){
			//python瓦片下载函数
			$this.is_vector_name =await eel.is_samename(path)();
		}
	},
	//文件路径选取
	fileChoose(){
		var $this =this;
		getSavePath();
		async function getSavePath(){
			if($this.activeName==="1"){
				$this.tileDownInput =await eel.get_save_path()();
			}else if($this.activeName==="2"){
				$this.demDownInput =await eel.get_save_path()();
			}else if($this.activeName==="3"){
				$this.vectorDownInput =await eel.get_save_path()();
			}
		}
	},
	isJoin(){
		this.tileOptions=[];
		if(this.tileChecked){
			var temp={
				value:"tif",
				label:"tif"
			}
			this.tileOptions.push(temp);
			this.tileOptionValue="tif";
		}else{
			var temp={
				value:"png",
				label:"png"
			}
			this.tileOptions.push(temp);
			this.tileOptionValue="png";
		}
	},
  	tileSelect(selection,row){
		// console.log(selection)
		//清空zoom数组
		this.myCommon.clearZoomAndResolution();
		//更新zoom
		this.myCommon.updateZoomAndResolution(selection);
		//更新瓦片总数
		this.myCommon.clearTotal();
		this.myCommon.updateTotal(selection);
  	},
	tileSelectAll(selection){
		//清空zoom数组
		this.myCommon.clearZoomAndResolution();
		//更新zoom
		this.myCommon.updateZoomAndResolution(selection);
		this.myCommon.clearTotal();
		this.myCommon.updateTotal(selection);
	},
	vectorSelect(selection,row){
		//清空数据集
		$store.state.downloadInfo.vector_load_info.dataset_names=[];
		//更新数据集数组
		for(let i=0;i<selection.length;i++){
			var temp={
				dataset_name:selection[i].data_code,
				describe:selection[i].layer_type,
				id:this.myCommon.UUID()
			}
			$store.state.downloadInfo.vector_load_info.dataset_names.push(temp);
		}
	},
	vectorSelectAll(selection){
		//清空数据集
		$store.state.downloadInfo.vector_load_info.dataset_names=[];
		//更新数据集数组
		for(let i=0;i<selection.length;i++){
			var temp={
				dataset_name:selection[i].data_code,
				describe:selection[i].layer_type,
				id:this.myCommon.UUID()
			}
			$store.state.downloadInfo.vector_load_info.dataset_names.push(temp);
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
		var path = this.tileDownInput+"\\"+this.tileNameInput;
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
.vectorSelectClass{
	margin-bottom: 10px;
}
.demSelectClass{
	margin-bottom: 233px;
}
</style>
