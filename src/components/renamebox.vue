<template>
	<div>
		<el-input v-model="layer_name" size="small" @input="isSameName()" placeholder="请输入图层名称"></el-input>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'renamebox',
  data(){
    return {
		layer_name:"",
		isName:false,
	}
  },
  methods:{
	isSameName(){
		this.isName=false;
		var temp_child = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_child.length;i++){
			if(temp_child[i].label===this.layer_name){
				this.isName=true;
			}
		}
	}
  },
}
</script>

<style lang="less">
</style>
