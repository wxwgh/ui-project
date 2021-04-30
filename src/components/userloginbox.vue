<template>
	<div>
		<!-- <el-input v-model="nameInput" size="small" placeholder="用户名"></el-input> -->
		<el-input v-model="passwordInput" size="small" :show-password="true" placeholder="密码" class="aliasInputClass"></el-input>
	</div>
</template>

<script>
export default {
  name: 'userloginbox',
  data(){
    return {
		// nameInput:"",
		passwordInput:""
	}
  },
  methods:{
	  
  },
}
</script>

<style lang="less">
</style>
