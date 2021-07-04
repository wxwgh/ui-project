<template>
	<div>
		<el-input v-model="layer_name" size="small" @input="isSameName()" placeholder="图层名称"></el-input>
		<el-input v-model="import_file_path" size="small" @input="input_change()" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value" @change="testChange(option_value)" size="mini" class="aliasInputClass" placeholder="源数据坐标系">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
		<div class="csv_parent">
			<div class="title_class"><span>CSV格式设置</span></div>
			<div class="csv_radio">
				<span>对象类型:</span>
				<el-radio v-model="radio" label="点" class="radio" @change="radio_change">点</el-radio>
				<el-radio v-model="radio" label="线" class="radio" @change="radio_change">线</el-radio>
				<el-radio v-model="radio" label="面" class="radio" @change="radio_change">面</el-radio>
			</div>
			<div class="geo_class">
				<span class="geo_span">经度:</span>
				<el-input v-model="lng" :disabled="is_point" size="mini" placeholder="填写列数,如1" class="geo_input"></el-input>
				<span>横坐标所在列</span>
			</div>
			<div class="geo_class">
				<span class="geo_span">纬度:</span>
				<el-input v-model="lat" :disabled="is_point" size="mini" placeholder="填写列数,如2" class="geo_input"></el-input>
				<span>纵坐标所在列</span>
			</div>
			<div class="geo_class">
				<span class="geo_span">空间对象:</span>
				<el-input v-model="geometry" :disabled="is_line_region" size="mini" placeholder="填写列数,如3" class="geo_input"></el-input>
				<span>线面对象填写空间对象列</span>
			</div>
			<div class="geo_model" v-if="is_model_show"></div>
		</div>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'layertreeimportbox',
  data(){
    return {
		layer_name:"",
		import_file_path:"",
		isName:false,
		option_value:"",
		options:[
			{
				value:"WGS 84",
				label:"4326"
			},
			{
				value:"WGS 84 / Pseudo-Mercator",
				label:"3857"
			},
			{
				value:"Beijing 1954",
				label:"4214"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 13",
				label:"21413"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 14",
				label:"21414"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 15",
				label:"21415"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 16",
				label:"21416"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 17",
				label:"21417"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 18",
				label:"21418"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 19",
				label:"21419"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 20",
				label:"21420"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 21",
				label:"21421"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 22",
				label:"21422"
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 23",
				label:"21423"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2401"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 26",
				label:"2402"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 27",
				label:"2403"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 28",
				label:"2404"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 29",
				label:"2405"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 30",
				label:"2406"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2407"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 31",
				label:"2408"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 32",
				label:"2409"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 33",
				label:"2410"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 34",
				label:"2411"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 35",
				label:"2401"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 36",
				label:"2412"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 37",
				label:"2413"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 38",
				label:"2414"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 39",
				label:"2415"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 40",
				label:"2416"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 41",
				label:"2417"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 42",
				label:"2418"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 43",
				label:"2419"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 44",
				label:"2420"
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 45",
				label:"2421"
			},
			{
				value:"北京54坐标系高斯投影",
				label:"Beijing 1954 高斯投影",
				label:{
					degree3:{
						75:"2401",
						78:"2402",
						81:"2403",
						84:"2404",
						87:"2405",
						90:"2406",
						93:"2407",
						96:"2408",
						99:"2409",
						102:"2410",
						105:"2411",
						108:"2412",
						111:"2413",
						114:"2414",
						117:"2415",
						120:"2416",
						123:"2417",
						126:"2418",
						129:"2419",
						132:"2420",
						135:"2421",
					},
					degree6:{
						75:"21413",
						81:"21414",
						87:"21415",
						93:"21416",
						99:"21417",
						105:"21418",
						111:"21419",
						117:"21420",
						123:"21421",
						129:"21422",
						135:"21423",
					}
				}
			},
			{
				value:"西安80坐标系经纬度投影",
				label:"Xian 1980"
			},
			{
				value:"西安80坐标系高斯投影",
				label:"Xian 1980 高斯投影"
				// label:{
				// 	degree3:{
				// 		75:"2349",
				// 		78:"2350",
				// 		81:"2351",
				// 		84:"2352",
				// 		87:"2353",
				// 		90:"2354",
				// 		93:"2355",
				// 		96:"2356",
				// 		99:"2357",
				// 		102:"2358",
				// 		105:"2359",
				// 		108:"2360",
				// 		111:"2361",
				// 		114:"2362",
				// 		117:"2363",
				// 		120:"2364",
				// 		123:"2365",
				// 		126:"2366",
				// 		129:"2367",
				// 		132:"2368",
				// 		135:"2369",
				// 	},
				// 	degree6:{
				// 		75:"2327",
				// 		81:"2328",
				// 		87:"2329",
				// 		93:"2330",
				// 		99:"2331",
				// 		105:"2332",
				// 		111:"2333",
				// 		117:"2334",
				// 		123:"2335",
				// 		129:"2336",
				// 		135:"2337",
				// 	}
				// }
			},
			{
				value:"国家2000坐标系经纬度投影",
				label:"China Geodetic Coordinate System 2000"
			},
			{
				value:"国家2000坐标系高斯投影",
				label:"CGCS2000 高斯投影"
				// label:{
				// 	degree3:{
				// 		75:"4513",
				// 		78:"4514",
				// 		81:"4515",
				// 		84:"4516",
				// 		87:"4517",
				// 		90:"4518",
				// 		93:"4519",
				// 		96:"4520",
				// 		99:"4521",
				// 		102:"4522",
				// 		105:"4523",
				// 		108:"4524",
				// 		111:"4525",
				// 		114:"4526",
				// 		117:"4527",
				// 		120:"4528",
				// 		123:"4529",
				// 		126:"4530",
				// 		129:"4531",
				// 		132:"4532",
				// 		135:"4533",
				// 	},
				// 	degree6:{
				// 		75:"4491",
				// 		81:"4492",
				// 		87:"4493",
				// 		93:"4494",
				// 		99:"4495",
				// 		105:"4496",
				// 		111:"4497",
				// 		117:"4498",
				// 		123:"4499",
				// 		129:"4500",
				// 		135:"4501",
				// 	}
				// }
			},
		],
		is_model_show:true,
		radio:"点",
		lng:"",
		lat:"",
		geometry:"",
		is_point:false,
		is_line_region:true,
		//导入类型
		import_format:"",
		//矢量类型
		feature_type:"点",
		is_exists:true,
	}
  },
  methods:{
	testChange(value){
		debugger
		for(let i=0;i<this.options.length;i++){
			if(value === this.options[i].value){
				console.log(this.options[i].label)
			}
		}
	},
	input_change(){
		var $this=this;
		this.import_format = this.import_file_path.split(".")[1];
		if(this.import_format === "csv"){
			this.is_model_show=false;
		}else if(this.import_format === "kml"){
			this.is_model_show=true;
		}else if(this.import_format === "shp"){
			this.is_model_show=true;
		}else{
			this.is_model_show=true;
			this.init_csv_panel();
			return false;
		}
		//格式化csv设置面板
		this.init_csv_panel();
		//判断文件是否存在
		get_file_exists(this.import_file_path);
		async function get_file_exists(data){
			var result =await eel.get_file_exists(data)();
			console.log(result)
			if(result){
				var data={
					file_path:$this.import_file_path,
					file_format:$this.import_format
				};
				get_import_coordinate(data);
				async function get_import_coordinate(data){
					var temp_coordinate =await eel.get_import_coordinate(data)();
					var flag = false;
					for(let i=0;i<$this.options.length;i++){
						if(temp_coordinate===$this.options[i].label){
							$this.option_value = $this.options[i].value;
							flag=true;
							break;
						}
					}
					if(!flag){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: "暂不支持"+temp_coordinate+"坐标系"
						});
						$this.is_exists=false;
					}else{
						$this.is_exists=true;
					}
				}
			}else{
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: "文件不存在,请确认文件地址是否正确"
				});
				$this.is_exists=false;
			}
		}
		
	},
	init_panel(){
		this.option_value="";
		this.layer_name="";
		this.import_file_path="";
		this.lng="";
		this.lat="";
		this.geometry="";
		this.radio="点";
		this.is_model_show=true;
		this.is_point=false;
		this.is_line_region=true;
		this.import_format="";
		this.feature_type="点";
		this.is_exists=true;
	},
	init_csv_panel(){
		this.radio="点";
		this.feature_type = "point";
		this.is_point=false;
		this.lng="";
		this.lat="";
		this.geometry="";
		this.is_line_region=true;
	},
	radio_change(label){
		if(label==="点"){
			this.feature_type = "point";
			this.is_point=false;
			this.geometry="";
			this.is_line_region=true;
		}else if(label ==="线"){
			this.feature_type = "line";
			this.is_point=true;
			this.lng="";
			this.lat="";
			this.geometry="";
			this.is_line_region=false;
		}else if(label ==="面"){
			this.feature_type = "region";
			this.is_point=true;
			this.lng="";
			this.lat="";
			this.geometry="";
			this.is_line_region=false;
		}
	},
	importFileChoose(){
		var $this =this;
		get_import_path();
		async function get_import_path(){
			$this.import_file_path=await eel.get_import_path()();
			$this.import_format = $this.import_file_path.split(".")[1];
			if($this.import_format === "csv"){
				$this.is_model_show=false;
			}else if($this.import_format === "kml"){
				$this.is_model_show=true;
			}else if($this.import_format === "shp"){
				$this.is_model_show=true;
			}else{
				$this.is_model_show=true;
				$this.init_csv_panel();
				return false;
			}
			//格式化csv设置面板
			$this.init_csv_panel();
			var data={
				file_path:$this.import_file_path,
				file_format:$this.import_format
			};
			get_import_coordinate(data);
			async function get_import_coordinate(data){
				var temp_coordinate =await eel.get_import_coordinate(data)();
				var flag = false;
				for(let i=0;i<$this.options.length;i++){
					if(temp_coordinate===$this.options[i].label){
						$this.option_value = $this.options[i].value;
						flag=true;
						break;
					}
				}
				if(!flag){
					$this.$message({
					    showClose: true,
						type: 'error',
					    message: "暂不支持"+temp_coordinate+"坐标系"
					});
					$this.is_exists = false;
				}else{
					$this.is_exists = true;
				}
			}
		}
	},
	isSameName(){
		this.isName=false;
		var temp_child = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_child.length;i++){
			if(temp_child[i].label===this.layer_name){
				this.isName=true;
			}
		}
	},
  },
}
</script>

<style lang="less">
.csv_parent{
	position: relative;
	margin-top: 10px;
	border: 1px solid #DCDFE6;
}
.title_class{
	margin-left: 5px;
	line-height: 30px;
}
.csv_radio{
	display: flex;
	flex-direction: row;
	justify-content:start;
	line-height: 40px;
	margin-left: 5px;
}
.csv_radio .radio{
	line-height: 40px;
}
.csv_radio>span{
	margin-right: 16px;
}
.geo_class{
	display: flex;
	flex-direction: row;
	justify-content:start;
	line-height: 40px;
	margin-left: 5px;
	white-space:nowrap;
}
.geo_span{
	width: 70px;
}
.geo_input{
	width: 100px;
	margin-left: 5px;
	margin-right: 10px;
}
.geo_model{
	position: absolute;
	width: 100%;
	height: 100%;
	top:0;
	left: 0;
	z-index:10;
	background: #000000;
	opacity: 0.1;
}
</style>
