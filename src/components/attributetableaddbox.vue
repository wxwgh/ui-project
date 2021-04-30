<template>
	<div>
		<el-input v-model="field_name" size="small" placeholder="字段名称" @input="isSameName()"></el-input>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'attributetableaddbox',
  data(){
    return {
		field_name:"",
		isName:false
	}
  },
  methods:{
	isSameName(){
		this.isName=false;
		//获取当前图层名称
		var layer_name = $store.state.layerOperationInfo.option_value;
		var temp_child = $store.state.layerGroups[0].children;
		for(let i=0;i<temp_child.length;i++){
			if(temp_child[i].label===layer_name){
				var flag=temp_child[i].header_keys.indexOf(this.field_name);
				if(flag===-1){
					this.isName=false;
				}else{
					this.isName=true;
				}
			}
		}
	}
  },
}
</script>

<style lang="less">
</style>