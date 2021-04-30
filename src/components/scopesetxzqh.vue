<template>
	<div class="scopesetDivParent">
		<div class="scopesetSelectParent">
			<el-select size="small" v-model="provincePost.value" :placeholder="provincePost.type" :change="changeSelect(provincePost)">
				<el-option v-for="post in provincePost.option" :key="post.id" :label="post.label" :value="post.value"></el-option>
			</el-select>
			<el-select size="small" v-model="cityPost.value" :placeholder="cityPost.type" class="selectClass" :change="changeSelect(cityPost)">
				<el-option v-for="post in cityPost.option" :key="post.id" :label="post.label" :value="post.value"></el-option>
			</el-select>
		</div>
		<div class="scopesetSelectParent">
			<el-select size="small" v-model="countyPost.value" :placeholder="countyPost.type" :change="changeSelect(countyPost)">
				<el-option v-for="post in countyPost.option" :key="post.id" :label="post.label" :value="post.value"></el-option>
			</el-select>
			<el-select size="small" v-model="streetPost.value" :placeholder="streetPost.type" class="selectClass" :change="changeSelect(streetPost)">
				<el-option v-for="post in streetPost.option" :key="post.id" :label="post.label" :value="post.value"></el-option>
			</el-select>
		</div>
	</div>
</template>

<script>
import $store from '@/store/index.js';
export default {
  name: 'scopesetxzqh',
  data(){
    return {
		provincePost:{
			value:"",
			oldValue:"",
			type:"省",
			zoom:6,
			option:[],
		},
		cityPost:{
			value:"",
			oldValue:"",
			type:"市",
			zoom:8,
			option:[],
		},
		countyPost:{
			value:"",
			oldValue:"",
			type:"区/县",
			zoom:10,
			option:[],
		},
		streetPost:{
			value:"",
			oldValue:"",
			type:"镇/街道",
			zoom:10,
			option:[],
		},
	}
  },
  mounted:function(){
  	//初始化省下拉菜单
  	this.initSelect("中国",this.provincePost);
  },
  methods:{
	initSelect(keyword,post){
		var $this = this;
		var url = "https://restapi.amap.com/v3/config/district?subdistrict=1&showbiz=false&extensions=base&key="+$store.state.gaodeKey+"&s=rsv3&output=json&keywords="+keyword+"&callback=jsonp_300354_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4&csid=7C3B60ED-0C39-46A6-891E-A0D28DA8864B&sdkversion=1.4.15";
		$this.axios({
		  method: 'get',
		  url: url
		}).then(function (result) {
			var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
			var child = temp.districts[0].districts;
			for(let i=0;i<child.length;i++){
				if(post.type==="镇/街道"){
					var streetOption ={
						id:$this.$UUID(),
						value:child[i].name,
						label:child[i].name,
						center:child[i].center,
						polyline:"",
						adcode:child[i].adcode,
					}
					post.option.push(streetOption);
				}else{
					var url2 = "https://restapi.amap.com/v3/config/district?subdistrict=1&showbiz=false&extensions=all&key="+$store.state.gaodeKey+"&s=rsv3&output=json&level="+child[i].level+"&keywords="+child[i].name+"&callback=jsonp_183447_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4&csid=E8C76FF9-2E7E-42EA-BD68-2FA8E329BEA0&sdkversion=1.4.15";
					$this.axios({
						method:"get",
						url:url2
					}).then(function(result2){
						var tempResult = JSON.parse(result2.data.substring(result2.data.indexOf("(")+1,result2.data.length-1));
						var tempChild = tempResult.districts[0];
						var tempOption={
							id:$this.$UUID(),
							value:tempChild.name,
							label:tempChild.name,
							center:tempChild.center,
							polyline:tempChild.polyline,
							adcode:tempChild.adcode,
						};
						post.option.push(tempOption);
					})
				}
				
				
			}
		})
	},
  	changeSelect(post){
		if(post.value){
			if(post.type==="省"){
				if(post.value!==post.oldValue){
					this.cityPost.option=[];
					this.cityPost.value="";
					this.countyPost.option=[];
					this.countyPost.value="";
					this.streetPost.option=[];
					this.streetPost.value="";
					post.oldValue=post.value;
					this.initSelect(post.value,this.cityPost);
				}
			}else if(post.type==="市"){
				if(post.value!==post.oldValue){
					this.countyPost.option=[];
					this.countyPost.value="";
					this.streetPost.option=[];
					this.streetPost.value="";
					post.oldValue=post.value;
					this.initSelect(post.value,this.countyPost);
				}
			}else if(post.type==="区/县"){
				if(post.value!==post.oldValue){
					this.streetPost.option=[];
					this.streetPost.value="";
					post.oldValue=post.value;
					this.initSelect(post.value,this.streetPost);
				}
			}
			
		}
  	},
	
  },
}
</script>

<style lang="less">
.scopesetDivParent{
	display: flex;
	flex-direction: column;
	justify-content:flex-start;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:space-between;
}
.scopesetSelectParent{
	display: flex;
	flex-direction: row;
	justify-content:space-between;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
	margin-top: 10px;
}
.selectClass{
	margin-left: 10px;
}
</style>
