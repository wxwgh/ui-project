<template>
	<ul class="mapListUlClass">
		<li v-for="p in get_post" :id="p.id" :class="{textActive:p.isActive,mapListOver:p.isShow}" @click="main_click(p)" @mouseleave="mouseLeave(p)" @mouseover="mouseOver(p)">
			<div class="map_list_main_parent">
				<div>
					<el-image class="mapListMainImage" :src="p.image" fit='fill'></el-image>
					<span>{{p.name}}</span>
				</div>
				<el-button size="mini" type="text" icon="el-icon-minus" @click.stop="main_delete(p)" class="custom_main_button"></el-button>
			</div>
		</li>
	</ul>
</template>

<script>
export default {
  name: 'custommaplist',
  data(){
    return {
		 
	}
  },
  computed:{
  	  get_post:function(){
  		  return this.$store.state.custom_map_list;
  	  },
  },
  methods:{
	main_delete(post){
		var $this =this;
		this.$confirm('服务删除后不可恢复, 是否继续?', '删除服务', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			type: 'warning'
		}).then(() => {
			//删除全局对象
			var temp_data = $this.$store.state.custom_map_list;
			for(let i=0;i<temp_data.length;i++){
				if(temp_data[i].id===post.id){
					temp_data.splice(i,1);
					break;
				}
			}
			//删除indexed
			var id = $this.$store.state.custom_map_list_id;
			$this.myCommon.deleteIndexedDB(id,post);
		}).catch(() => {
		});
	},
	main_click(post){
		var temp_data = this.$store.state.custom_map_list;
		//清空地图列表选中状态
		var temp_map_list = this.$store.state.mapList;
		for(let i=0;i<temp_map_list.length;i++){
			for(let j=0;j<temp_map_list[i].urls.length;j++){
				temp_map_list[i].urls[j].isActive=false;
			}
		}
		//切换地图容器 首先判断是否需要切换
		if(!this.$store.state.mapContainer[0].isShow){
			//跳转页面
			this.$router.push('/CommonMap');
			//更新地图类型
			this.myCommon.updateMapType("CommonMap");
		}
		//获取map
		var map = this.myCommon.getMap();
		var layer = this.myCommon.getLayer();
		if(layer){
			//删除图层
			layer.remove();
		}
		//清空三维图层
		this.$store.state.viewer.imageryLayers.removeAll();
		for(let i=0;i<temp_data.length;i++){
			if(temp_data[i].id===post.id){
				temp_data[i].isActive=true;
				//叠加三维场景图层
				this.$store.state.viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider(temp_data[i].imageProvider));
				//叠加二维图层
				var layer = L.tileLayer.chinaProvider(temp_data[i].url).addTo(map);
				this.myCommon.updateLayer(layer);
			}else{
				temp_data[i].isActive=false;
			}
		}
	},
	mouseOver(post){
		this.myCommon.mouseOver(post);
	},
	mouseLeave(post){
		this.myCommon.mouseLeave(post);
	},
  },
}
</script>

<style lang="less">
.map_list_main_parent{
	display: flex;
	flex-direction: row;
	flex-wrap:nowrap;
	justify-content:space-between;
	
}
.map_list_main_parent>div:nth-child(1)>span{
	line-height: 38px;
	vertical-align: middle;
}
.custom_main_button{
	margin-right: 10px;
}
</style>
