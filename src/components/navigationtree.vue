<template>
	<el-tree :data="get_data" :props="{label:'name',children:'districts'}" :expand-on-click-node="false" @node-click="node_click"></el-tree>
</template>

<script>
export default {
  name: 'navigationtree',
  data(){
    return {
		
	}
  },
  computed:{
  	  get_data:function(){
  		  return this.$store.state.navigation_tree;
  	  },
  },
  methods:{
  	node_click(data){
		console.log(data);
		var $this = this;
		var map = this.myCommon.getMap();;
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		//清除选中
		this.myCommon.clearOperation();
		//清空表数据
		this.myCommon.clearAttributeTable();
		//清空选取图层列表
		this.myCommon.clear_operation_list();
		//更新表头
		this.myCommon.update_attribute_header();
		//清空范围
		$this.myCommon.clearScope();
		var key = this.$store.state.gaodeKey;
		var url = "https://restapi.amap.com/v3/config/district?subdistrict=0&showbiz=false&extensions=all&key="+key+"&s=rsv3&output=json&keywords="+data.adcode+"&callback=jsonp_300354_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4&csid=7C3B60ED-0C39-46A6-891E-A0D28DA8864B&sdkversion=1.4.15";
		this.axios({
			method: 'get',
			url: url
		}).then(function(result){
			var temp_data = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
			var temp = temp_data.districts[0].polyline.split("|");
			var temp_latlngs =[];
			for(let j=0;j<temp.length;j++){
				var temp_points=temp[j].split(";");
				var latlngs =[];
				for(let f=0;f<temp_points.length;f++){
					var temp_lnglat=$this.gcj02towgs84(parseFloat(temp_points[f].split(",")[0]),parseFloat(temp_points[f].split(",")[1]));
					var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
					latlngs.push(latlng);
				}
				temp_latlngs.push(latlngs);
			}
			let polygon = L.polygon(temp_latlngs,{
				color:'#0157F0',
				weight:1,
				fillOpacity:0.3,
				className:"layerCursor"
			}).addTo(map);
			polygon.bindTooltip("单击下载",{
				direction:"right",
				sticky:true,
				offset:L.point(5,0)
			});
			polygon.on("mousedown",function(){
				$(".topButton").each(function(){
					if($(this).text()==="地图下载"){
						$(this).trigger("click");
					}
				});
			})
			var geojson = $this.myCommon.get_geojson(polygon);
			$this.myCommon.update_scopeInfo(true,temp_data.districts[0].adcode,polygon,geojson);
			var center = temp_data.districts[0].center;
			map.setView(L.latLng(center.split(",")[1],center.split(",")[0]),data.zoom);
		})
  	},
  },
}
</script>

<style lang="less">
</style>
