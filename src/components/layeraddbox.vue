<template>
	<div>
		<el-input v-model="layer_name" size="small" @input="isSameName()" placeholder="请输入图层名称"></el-input>
		<el-select v-model="option_value" size="mini" class="aliasInputClass">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'layeraddbox',
  data(){
    return {
		layer_name:"",
		isName:false,
		option_value:"点",
		options:[
			{
				value:"点",
				label:"点"
			},
			{
				value:"线",
				label:"线"
			},
			{
				value:"面",
				label:"面"
			},
		],
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
