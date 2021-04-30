<template>
	<div>
		<el-input v-model="import_file_path" size="small" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
	</div>
</template>

<script>
export default {
  name: 'updatelicence',
  data(){
    return {
		import_file_path:"",
	}
  },
  methods:{
	importFileChoose(){
		var $this =this;
		get_licence_path();
		async function get_licence_path(){
			$this.import_file_path =await eel.get_licence_path()();
		}
	},
  },
}
</script>

<style lang="less">
</style>
