<template>
	<div>
		<el-select v-model="field_name" size="small" placeholder="选择字段" style="width:100%" >
			<el-option v-for="post in get_options" :key="post.id" :label="post.label" :value="post.value"></el-option>
		</el-select>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'attributetabledeletebox',
  data(){
    return {
		field_name:"",
	}
  },
  computed:{
  	get_options:function(){
  		return $store.state.layer_delete_options;
  	},
  },
  methods:{
  },
}
</script>

<style lang="less">
</style>
