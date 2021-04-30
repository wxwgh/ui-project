<template>
	<div class="userinfoParentClass">
		<div class="userinfoClass">类型:{{get_info.name}}</div>
		<div class="userinfoClass">描述:{{get_info.describe}}</div>
		<div class="userinfoClass">许可:{{get_info.time}}</div>
	</div>
</template>

<script>
export default {
  name: 'userinfo',
  data(){
    return {
	}
  },
  computed:{
  	get_info:function(){
  		return this.$store.state.administratorInfo;
  	},
  },
  methods:{
  	
  },
}
</script>

<style lang="less">
.userinfoParentClass{
	border-right:1px solid #E4E7ED;
	height: 100%;
	display: flex;
	flex-direction: column;
	flex-wrap:nowrap;
	justify-content:space-around;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
}
.userinfoClass{
	margin-left: 10px;
	margin-right: 10px;
}
</style>
