<template>
	<div>
		<div class="unitclass">
			<span>距离单位:</span>
			<el-radio v-model="get_distance_radio" label="米" class="radio">米</el-radio>
			<el-radio v-model="get_distance_radio" label="千米" class="radio">千米</el-radio>
			<el-radio v-model="get_distance_radio" label="英里" class="radio">英里</el-radio>
			<el-radio v-model="get_distance_radio" label="丈" class="radio">丈</el-radio>
		</div>
		<div class="unitclass">
			<span>面积单位:</span>
			<el-radio v-model="get_area_radio" label="平方米" class="radio">平方米</el-radio>
			<el-radio v-model="get_area_radio" label="平方千米" class="radio">平方千米</el-radio>
			<el-radio v-model="get_area_radio" label="亩" class="radio">亩</el-radio>
			<el-radio v-model="get_area_radio" label="公顷" class="radio">公顷</el-radio>
		</div>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'measuresetbox',
  data(){
    return {
	}
  },
  computed:{
  	get_distance_radio:{
		get(){
			return $store.state.measure_unit.distance_unit;
		},
		set(val){
			$store.state.measure_unit.distance_unit=val;
		}
	},
	get_area_radio:{
		get(){
			return $store.state.measure_unit.area_unit;
		},
		set(val){
			$store.state.measure_unit.area_unit=val;
		}
	},
  },
  methods:{
	  
  },
}
</script>

<style lang="less">
.unitclass{
	display: flex;
	flex-direction: row;
	justify-content:start;
	margin-top: 10px;
	line-height: 40px;
}
.unitclass .radio{
	line-height: 40px;
}
.unitclass>span{
	margin-right: 4px;
}
</style>
