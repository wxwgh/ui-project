<template>
	<div>
		<el-input v-model="map_name" size="small" @input="isSameName()" placeholder="服务名称" class="aliasInputClass"></el-input>
		<el-input v-model="map_url" size="small" placeholder="服务地址 格式如下:http://xx.com?经度={x}纬度={y}级别={z}" class="aliasInputClass"></el-input>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'custommaplistbox',
  data(){
    return {
		map_name:"",
		map_url:"",
		isName:false,
	}
  },
  methods:{
	init_custommaplistbox(){
		this.map_name="";
		this.map_url="";
	},
	isSameName(){
		var map_list = $store.state.custom_map_list;
		for(let i=0;i<map_list.length;i++){
			if(map_list[i].name === this.map_name){
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
