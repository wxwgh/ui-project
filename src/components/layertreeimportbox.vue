<template>
	<div>
		<el-input v-model="layer_name" size="small" @input="isSameName()" placeholder="图层名称"></el-input>
		<el-input v-model="import_file_path" size="small" @input="input_change()" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value" size="mini" class="aliasInputClass" placeholder="源数据坐标系">
			<el-option v-for="post in options" :label="post.label" :value="post.value"></el-option>
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
				label:"WGS 84",
				value:"4326"
			},
			{
				label:"WGS 84 / Pseudo-Mercator",
				value:"3857"
			},
			{
				label:"Beijing 1954",
				value:"4214"
			},
			{
				label:"Beijing 1954 / Gauss-Kruger zone 15",
				value:"21415"
			},
			{
				label:"Xian 1980",
				value:"4610"
			},
			{
				label:"Xian 1980 / Gauss-Kruger zone 15",
				value:"2329",
			},
			{
				label:"China Geodetic Coordinate System 2000",
				value:"4490"
			},
			{
				label:"CGCS2000 / Gauss-Kruger zone 15",
				value:"4493",
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
	input_change(){
		console.log(this.options)
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
						if(temp_coordinate==$this.options[i].label){
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
