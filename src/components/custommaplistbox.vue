<template>
	<div>
		<el-input v-model="map_name" size="small" @input="isSameName()" placeholder="服务名称" class="aliasInputClass"></el-input>
		<el-input v-model="map_url" size="small" placeholder="服务地址" class="aliasInputClass"></el-input>
		<el-input v-model="layer_name" size="small" placeholder="图层名称" class="aliasInputClass"></el-input>
		<el-input v-model="tile_matrix" :disabled="map_type_flag" size="small" placeholder="比例尺集合" class="aliasInputClass"></el-input>
		<div class="radio_checkbox_parent">
			<el-radio v-model="type_radio" label="WMS" @change="radio_change()">WMS</el-radio>
			<el-radio v-model="type_radio" label="WMTS" @change="radio_change()">WMTS</el-radio>
		</div>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'custommaplistbox',
  data(){
    return {
		type_radio:"WMS",
		tile_matrix:"",
		map_name:"",
		map_url:"",
		layer_name:"",
		isName:false,
		map_type_flag:true,
	}
  },
  methods:{
	//地图类型更改事件
	radio_change(){
		if(this.type_radio==="WMS"){
			this.map_type_flag=true;
			this.map_name="";
			this.map_url="";
			this.layer_name="";
			this.tile_matrix="";
			this.isName=false;
		}else{
			this.map_type_flag=false;
			this.map_name="";
			this.map_url="";
			this.layer_name="satImage";
			this.tile_matrix="satImage";
			this.isName=false;
		}
	},
	init_custommaplistbox(){
		this.map_name="";
		this.map_url="";
		this.layer_name="";
		this.type_radio="WMS";
		this.tile_matrix="";
		this.isName=false;
		this.map_type_flag=true;
	},
	isSameName(){
		var map_list = $store.state.custom_map_list[0].children;
		for(let i=0;i<map_list.length;i++){
			if(map_list[i].label === "自定义-"+this.map_name){
				this.isName = true;
				break;
			}else{
				this.isName = false;
			}
		}
	}
  },
}
</script>

<style lang="less">
</style>
