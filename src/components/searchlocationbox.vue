<template>
	<div>
		<el-input v-model="location_value" size="small" placeholder="请输入经纬度坐标"></el-input>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'searchlocationbox',
  data(){
    return {
		location_value:"116.72,39.62",
	}
  },
  methods:{
  },
}
</script>

<style lang="less">
</style>
