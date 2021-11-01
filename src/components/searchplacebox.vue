<template>
	<div>
		<el-input v-model="place_name" size="small" @input="isSameName()" placeholder="请输入地名关键字"></el-input>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'searchplacebox',
  data(){
    return {
		place_name:"学校",
		isName:false,
	}
  },
  methods:{
	isSameName(){
		this.isName=false;
		var temp_child = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_child.length;i++){
			if(temp_child[i].label===this.place_name){
				this.isName=true;
			}
		}
	}
  },
}
</script>

<style lang="less">
</style>
