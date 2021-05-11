<template>
	<div class="topButtonsParent">
		<div>
			<div>
				<el-checkbox v-model="sheet_checked">显示图幅</el-checkbox>
				<el-checkbox v-model="lnglat_checked">显示地理经纬度格网</el-checkbox>
			</div>
			<div>
				<el-select size="small" v-model="provincePost.value" :placeholder="provincePost.type" :change="changeSelect(provincePost)">
					<el-option v-for="post in provincePost.option" :key="post.id" :label="post.label" :value="post.value"></el-option>
				</el-select>
			</div>
		</div>
		<div class="description">
			<span>显示分幅设置</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'mapdownload',
  data(){
    return {
		sheet_checked:false,
		lnglat_checked:false,
		option_value:"shp",
		options:[
			{
				value:"shp",
				label:"shp"
			},
			{
				value:"json",
				label:"json"
			},
		],
	}
  },
  methods:{
	  
  },
}
</script>

<style lang="less">
</style>
