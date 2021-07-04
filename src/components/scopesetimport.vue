<template>
	<div>
		<el-input v-model="import_file_path" size="small" @input="input_change()" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value" size="mini" class="aliasInputClass" placeholder="源数据坐标系">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
		<div class="csv_parent">
			<div class="title_class"><span>CSV格式设置</span></div>
			<div class="csv_radio">
				<span>对象类型:</span>
				<el-radio v-model="radio" label="面" class="radio">面</el-radio>
			</div>
			<div class="geo_class">
				<span class="geo_span">空间对象:</span>
				<el-input v-model="geometry" size="mini" placeholder="填写列数,如3" class="geo_input"></el-input>
				<span>填写空间对象列</span>
			</div>
			<div class="geo_model" v-if="is_model_show"></div>
		</div>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'scopesetimport',
  data(){
    return {
		import_file_path:"",
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
				value:"Xian 1980",
				label:"4610"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 13",
				label:"2327"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 14",
				label:"2328"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 15",
				label:"2329"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 16",
				label:"2330"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 17",
				label:"2331"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 18",
				label:"2332"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 19",
				label:"2333"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 20",
				label:"2334"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 21",
				label:"2335"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 22",
				label:"2336"
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 23",
				label:"2337"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 25",
				label:"2349"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 26",
				label:"2350"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 27",
				label:"2351"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 28",
				label:"2352"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 29",
				label:"2353"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 30",
				label:"2354"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 31",
				label:"2355"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 32",
				label:"2356"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 33",
				label:"2357"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 34",
				label:"2358"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 35",
				label:"2359"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 36",
				label:"2360"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 37",
				label:"2361"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 38",
				label:"2362"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 39",
				label:"2363"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 40",
				label:"2364"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 41",
				label:"2365"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 42",
				label:"2366"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 43",
				label:"2367"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 44",
				label:"2368"
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 45",
				label:"2369"
			},
			{
				value:"China Geodetic Coordinate System 2000",
				label:"4490"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 13",
				label:"4491"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 14",
				label:"4492"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 15",
				label:"4493"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 16",
				label:"4494"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 17",
				label:"4495"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 18",
				label:"4496"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 19",
				label:"4497"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 20",
				label:"4498"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 21",
				label:"4499"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 22",
				label:"4500"
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 23",
				label:"4501"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 25",
				label:"4513"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 26",
				label:"4514"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 27",
				label:"4515"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 28",
				label:"4516"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 29",
				label:"4517"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 30",
				label:"4518"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 31",
				label:"4519"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 32",
				label:"4520"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 33",
				label:"4521"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 34",
				label:"4522"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 35",
				label:"4523"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 36",
				label:"4524"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 37",
				label:"4525"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 38",
				label:"4526"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 39",
				label:"4527"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 40",
				label:"4528"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 41",
				label:"4529"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 42",
				label:"4530"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 43",
				label:"4531"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 44",
				label:"4532"
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 45",
				label:"4533"
			},
		],
		is_model_show:true,
		radio:"面",
		geometry:"",
		//导入类型
		import_format:"",
		//矢量类型
		feature_type:"region",
		//文件是否存在
		is_exists:true,
	}
  },
  methods:{
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
						if(temp_coordinate===$this.options[i].value){
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
		this.import_file_path="";
		this.geometry="";
		this.is_model_show=true;
		this.import_format="";
		this.is_exists=true;
	},
	init_csv_panel(){
		this.geometry="";
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
					if(temp_coordinate===$this.options[i].value){
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
