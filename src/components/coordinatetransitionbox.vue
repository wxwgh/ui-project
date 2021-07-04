<template>
	<div>
		<el-input v-model="task_name" @input="isSameName()" size="small" placeholder="任务名称"></el-input>
		<el-input v-model="import_file_path" size="small" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-select v-model="option_value" size="small" class="aliasInputClass" placeholder="源数据坐标系">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
		<el-input v-model="save_path" size="small" @input="save_change()" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="savePathChoose()"></i>
		</el-input>
		<el-select v-model="option_value2" size="small" class="aliasInputClass"  placeholder="目标坐标系">
			<el-option v-for="post in options2" :labek="post.label" :value="post.value"></el-option>
		</el-select>
<!-- 		<div class="seven_title"><span :class="{'on_need':on_need,'off_need':off_need}">七参数设置</span></div>
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
		<el-input v-model="seven.k" :disabled="off_need" class="seven_class" size="small" placeholder="k缩放"></el-input> -->
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
		isName:false,
		//导入类型
		import_format:"",
		//导出类型
		export_format:"tif",
		//源坐标系
		option_value:"",
		options:[
			{
				value:"WGS 84",
				label:"4326",
				disabled:false
			},
			{
				value:"WGS 84 / Pseudo-Mercator",
				label:"3857",
				disabled:false
			},
			{
				value:"Beijing 1954",
				label:"4214",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 13",
				label:"21413",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 14",
				label:"21414",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 15",
				label:"21415",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 16",
				label:"21416",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 17",
				label:"21417",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 18",
				label:"21418",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 19",
				label:"21419",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 20",
				label:"21420",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 21",
				label:"21421",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 22",
				label:"21422",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 23",
				label:"21423",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2401",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 26",
				label:"2402",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 27",
				label:"2403",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 28",
				label:"2404",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 29",
				label:"2405",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 30",
				label:"2406",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2407",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 31",
				label:"2408",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 32",
				label:"2409",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 33",
				label:"2410",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 34",
				label:"2411",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 35",
				label:"2401",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 36",
				label:"2412",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 37",
				label:"2413",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 38",
				label:"2414",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 39",
				label:"2415",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 40",
				label:"2416",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 41",
				label:"2417",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 42",
				label:"2418",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 43",
				label:"2419",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 44",
				label:"2420",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 45",
				label:"2421",
				disabled:false
			},
			{
				value:"Xian 1980",
				label:"4610",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 13",
				label:"2327",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 14",
				label:"2328",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 15",
				label:"2329",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 16",
				label:"2330",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 17",
				label:"2331",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 18",
				label:"2332",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 19",
				label:"2333",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 20",
				label:"2334",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 21",
				label:"2335",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 22",
				label:"2336",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 23",
				label:"2337",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 25",
				label:"2349",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 26",
				label:"2350",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 27",
				label:"2351",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 28",
				label:"2352",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 29",
				label:"2353",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 30",
				label:"2354",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 31",
				label:"2355",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 32",
				label:"2356",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 33",
				label:"2357",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 34",
				label:"2358",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 35",
				label:"2359",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 36",
				label:"2360",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 37",
				label:"2361",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 38",
				label:"2362",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 39",
				label:"2363",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 40",
				label:"2364",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 41",
				label:"2365",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 42",
				label:"2366",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 43",
				label:"2367",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 44",
				label:"2368",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 45",
				label:"2369",
				disabled:false
			},
			{
				value:"China Geodetic Coordinate System 2000",
				label:"4490",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 13",
				label:"4491",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 14",
				label:"4492",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 15",
				label:"4493",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 16",
				label:"4494",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 17",
				label:"4495",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 18",
				label:"4496",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 19",
				label:"4497",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 20",
				label:"4498",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 21",
				label:"4499",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 22",
				label:"4500",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 23",
				label:"4501",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 25",
				label:"4513",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 26",
				label:"4514",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 27",
				label:"4515",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 28",
				label:"4516",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 29",
				label:"4517",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 30",
				label:"4518",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 31",
				label:"4519",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 32",
				label:"4520",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 33",
				label:"4521",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 34",
				label:"4522",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 35",
				label:"4523",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 36",
				label:"4524",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 37",
				label:"4525",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 38",
				label:"4526",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 39",
				label:"4527",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 40",
				label:"4528",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 41",
				label:"4529",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 42",
				label:"4530",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 43",
				label:"4531",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 44",
				label:"4532",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 45",
				label:"4533",
				disabled:false
			},
		],
		//目标坐标系
		option_value2:"",
		options2:[
			{
				value:"WGS 84",
				label:"4326",
				disabled:false
			},
			{
				value:"WGS 84 / Pseudo-Mercator",
				label:"3857",
				disabled:false
			},
			{
				value:"Beijing 1954",
				label:"4214",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 13",
				label:"21413",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 14",
				label:"21414",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 15",
				label:"21415",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 16",
				label:"21416",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 17",
				label:"21417",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 18",
				label:"21418",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 19",
				label:"21419",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 20",
				label:"21420",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 21",
				label:"21421",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 22",
				label:"21422",
				disabled:false
			},
			{
				value:"Beijing 1954 / Gauss-Kruger zone 23",
				label:"21423",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2401",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 26",
				label:"2402",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 27",
				label:"2403",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 28",
				label:"2404",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 29",
				label:"2405",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 30",
				label:"2406",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 25",
				label:"2407",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 31",
				label:"2408",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 32",
				label:"2409",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 33",
				label:"2410",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 34",
				label:"2411",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 35",
				label:"2401",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 36",
				label:"2412",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 37",
				label:"2413",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 38",
				label:"2414",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 39",
				label:"2415",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 40",
				label:"2416",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 41",
				label:"2417",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 42",
				label:"2418",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 43",
				label:"2419",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 44",
				label:"2420",
				disabled:false
			},
			{
				value:"Beijing 1954 / 3-degree Gauss-Kruger zone 45",
				label:"2421",
				disabled:false
			},
			{
				value:"Xian 1980",
				label:"4610",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 13",
				label:"2327",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 14",
				label:"2328",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 15",
				label:"2329",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 16",
				label:"2330",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 17",
				label:"2331",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 18",
				label:"2332",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 19",
				label:"2333",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 20",
				label:"2334",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 21",
				label:"2335",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 22",
				label:"2336",
				disabled:false
			},
			{
				value:"Xian 1980 / Gauss-Kruger zone 23",
				label:"2337",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 25",
				label:"2349",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 26",
				label:"2350",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 27",
				label:"2351",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 28",
				label:"2352",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 29",
				label:"2353",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 30",
				label:"2354",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 31",
				label:"2355",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 32",
				label:"2356",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 33",
				label:"2357",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 34",
				label:"2358",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 35",
				label:"2359",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 36",
				label:"2360",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 37",
				label:"2361",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 38",
				label:"2362",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 39",
				label:"2363",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 40",
				label:"2364",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 41",
				label:"2365",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 42",
				label:"2366",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 43",
				label:"2367",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 44",
				label:"2368",
				disabled:false
			},
			{
				value:"Xian 1980 / 3-degree Gauss-Kruger zone 45",
				label:"2369",
				disabled:false
			},
			{
				value:"China Geodetic Coordinate System 2000",
				label:"4490",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 13",
				label:"4491",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 14",
				label:"4492",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 15",
				label:"4493",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 16",
				label:"4494",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 17",
				label:"4495",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 18",
				label:"4496",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 19",
				label:"4497",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 20",
				label:"4498",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 21",
				label:"4499",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 22",
				label:"4500",
				disabled:false
			},
			{
				value:"CGCS2000 / Gauss-Kruger zone 23",
				label:"4501",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 25",
				label:"4513",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 26",
				label:"4514",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 27",
				label:"4515",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 28",
				label:"4516",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 29",
				label:"4517",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 30",
				label:"4518",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 31",
				label:"4519",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 32",
				label:"4520",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 33",
				label:"4521",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 34",
				label:"4522",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 35",
				label:"4523",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 36",
				label:"4524",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 37",
				label:"4525",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 38",
				label:"4526",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 39",
				label:"4527",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 40",
				label:"4528",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 41",
				label:"4529",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 42",
				label:"4530",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 43",
				label:"4531",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 44",
				label:"4532",
				disabled:false
			},
			{
				value:"CGCS2000 / 3-degree Gauss-Kruger zone 45",
				label:"4533",
				disabled:false
			},
		],
	}
  },
  methods:{
	//初始化
	initCoordinate(){
		this.task_name="";
		this.import_file_path="";
		this.save_path="D:/SuperMap DownLoad";
		this.isName=false;
		//导入类型
		this.import_format="";
		//导出类型
		this.export_format="tif";
		//源坐标系
		this.option_value="";
		this.option_value2="";
	},
	savePathChoose(){
		var $this =this;
		get_export_path();
		async function get_export_path(){
			$this.save_path =await eel.get_export_path()();
		}
	},
	importFileChoose(){
		var $this =this;
		get_tif_path();
		async function get_tif_path(){
			$this.import_file_path =await eel.get_tif_path()();
			$this.import_format = $this.import_file_path.split(".")[1];
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
	save_change(){
		this.isSameName();
	},
	// 判断是否需要七参数
	is_need_seven(){
		var $this = this;
		// 源坐标系
		var source_coordinate = "";
		for(let i = 0;i<this.options.length;i++){
			if(this.option_value === this.options[i].value){
				source_coordinate = this.options[i].label;
			}
		}
		//目标坐标系
		var target_coordinate = "";
		for(let i = 0;i<this.options2.length;i++){
			if(this.option_value2 === this.options2[i].value){
				target_coordinate = this.options2[i].label;
			}
		}
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
</style>
