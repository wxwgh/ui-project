<template>
	<div>
		<el-input v-model="task_name" size="small" placeholder="任务名称"></el-input>
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
				import_file_path: "",
				save_path: "",
				option_value: "tif",
				options: [{
						value: "tif",
						label: "tif"
					},
					{
						value: "img",
						label: "img"
					},
				],
			}
		},
		methods: {
			savePathChoose() {
				var $this = this;
				getSavePath();
				async function getSavePath() {
					$this.save_path = await eel.get_save_path()();
				}
			},
			importFileChoose() {
				var $this = this;
				getFilePath();
				async function getFilePath() {
					$this.import_file_path = await eel.get_grid_path()();
				}
			},
		},
	}
</script>

<style lang="less">
</style>
