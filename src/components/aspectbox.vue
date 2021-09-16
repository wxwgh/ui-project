<template>
	<div>
		<el-input v-model="task_name" size="small" @input="isSameName()" placeholder="任务名称"></el-input>
		<el-input v-model="import_file_path" size="small" placeholder="导入文件路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="importFileChoose()"></i>
		</el-input>
		<el-input v-model="save_path" size="small" placeholder="文件保存路径" class="aliasInputClass">
			<i slot="suffix" class="el-input__icon el-icon-folder layerCursor" @click="savePathChoose()"></i>
		</el-input>
		<el-select v-model="option_value" size="mini" class="aliasInputClass">
			<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
		</el-select>
	</div>
</template>

<script>
	export default {
		name: 'aspectbox',
		data() {
			return {
				type: "aspectbox",
				task_name: "",
				isName:false,
				import_file_path: "",
				save_path: "",
				option_value: "tif",
				options: [{
						value: "tif",
						label: "tif"
					}
				],
			}
		},
		methods: {
			init_panel(){
				this.import_file_path="";
				this.save_path="";
				this.task_name="";
				this.option_value="shp";
				this.isName=false;
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
