<template>
	<div>
		<el-input v-model="layer_name" size="small" @input="isSameName()" placeholder="图层名称"></el-input>
		<el-input v-model="import_file_path" size="small" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
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
	}
  },
  methods:{
	importFileChoose(){
		var $this =this;
		getFilePath();
		async function getFilePath(){
			$this.import_file_path =await eel.get_shape_path()();
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
	}
  },
}
</script>

<style lang="less">
</style>
