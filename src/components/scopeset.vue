<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in scopeSetPost" @click="scopeClick(post)" :class="{tabMouseOver:post.isShow}" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>范围设置</span>
		</div>
	</div>
</template>

<script>
import scopesetxzqh from '@/components/scopesetxzqh.vue';
export default {
  name: 'scopeset',
  components:{
  	scopesetxzqh,
  },
  data(){
    return {
		index:null,
		rectAngleOptions:{
			color:'#0157F0',
			weight:1,
			fillOpacity:0.3,
			className:"layerCursor"
		},
		tipOptions:{
			direction:"right",
			sticky:true,
			offset:L.point(5,0)
		},
		lineOptions:{
			color:'#0157F0',
			weight:1,
		},
		scopeSetPost:[
			{
				name:"矩形",
				url:require('../assets/mapdownload/juxing.png'),
				isShow:false,
				
			},
			{
				name:"多边形",
				url:require('../assets/mapdownload/duobianxing.png'),
				isShow:false,
				
			},
			{
				name:"行政区划",
				url:require('../assets/mapdownload/xzqh.png'),
				isShow:false,
				
			},
			{
				name:"删除范围",
				url:require('../assets/mapdownload/clear.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
  	scopeClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		var temp_data = this.myCommon.isLoginAndTime();
		if(!temp_data.flag){
			this.$message(temp_data.options);
			return temp_data.flag
		}
		if(post.name==="矩形"){
			$this.myCommon.clearScope();
			$this.myCommon.switchMouseStyle(true,map);
			var point_first=null;
			var rectangle = null;
			var points = [];
			map.on("mousedown",function(e){
				//判断是否是左键
				if(e.originalEvent.button===0){
					if(point_first===null){
						point_first=e.latlng;
						points.push(e.latlng);
					}
					if(point_first&&point_first!==e.latlng){
						if(rectangle!=null){
							rectangle.remove();
						}
						points.push(e.latlng);
						var tempRectangle = L.rectangle(points, $this.$data.rectAngleOptions).addTo(map);
						tempRectangle.bindTooltip("单击下载",$this.$data.tipOptions);
						$this.bindEvent(tempRectangle);
						var geojson = $this.myCommon.get_geojson(tempRectangle);
						$this.myCommon.update_scopeInfo(false,"",tempRectangle,geojson);
						$this.myCommon.updateDownLoadTable();
						$this.myCommon.unbindMapEvent(map);
						$this.myCommon.switchMouseStyle(false,map);
					}	
				}
				
			})
			map.on("mousemove",function(e){
				if(rectangle!=null){
					rectangle.remove();
				}
				if(point_first){
					rectangle=L.rectangle([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.rectAngleOptions).addTo(map);
				}
			})
			map.on("contextmenu",function(e){
				if(rectangle!=null){
					rectangle.remove();
				}
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
		}else if(post.name==="多边形"){
			$this.myCommon.clearScope();
			$this.myCommon.switchMouseStyle(true,map);
			var point_first=null;
			var point_end = null;
			var line = null;
			var line2 = null;
			var lines=[];
			var points = [];
			map.on("mousedown",function(e){
				//判断是否是左键
				if(e.originalEvent.button===0){
					if(point_first===null&&point_end===null){
						point_first=e.latlng;
						point_end=e.latlng
						points.push(point_first);
					}
					if(point_first&&point_first!==e.latlng){
						var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]],$this.$data.lineOptions).addTo(map);
						lines.push(tempLine);
						points.push(e.latlng);
						point_first=e.latlng;
					}
				}
			})
			map.on("mousemove",function(e){
				if(line!=null){
					line.remove();
					
				}
				if(line2!=null){
					line2.remove();
				}
				if(point_first&&point_end===null){
					line=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.lineOptions).addTo(map);
				}else if(point_first&&point_end){
					line=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.lineOptions).addTo(map);
					line2=L.polyline([[point_end.lat,point_end.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.lineOptions).addTo(map);
				}
			})
			map.on("contextmenu",function(e){
				if(line!=null){
					line.remove();
					
				}
				if(line2!=null){
					line2.remove();
				}
				if(point_first&&point_end){
					var temp=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.lineOptions).addTo(map);
					var temp2=L.polyline([[point_end.lat,point_end.lng],[e.latlng.lat,e.latlng.lng]], $this.$data.lineOptions).addTo(map);
					lines.push(temp);
					lines.push(temp2);
					points.push(e.latlng);
					for(let i=0;i<lines.length;i++){
						lines[i].remove();
					}
					var polygon  = L.polygon(points,$this.$data.rectAngleOptions).addTo(map);
					polygon.bindTooltip("单击下载",$this.$data.tipOptions);
					$this.bindEvent(polygon);
					var geojson = $this.myCommon.get_geojson(polygon);
					$this.myCommon.update_scopeInfo(false,"",polygon,geojson);
					$this.myCommon.updateDownLoadTable();
				}
				$this.myCommon.switchMouseStyle(false,map);
				$this.myCommon.unbindMapEvent(map);
			})
		}else if(post.name==="行政区划"){
			$this.$confirm(<scopesetxzqh ref='scopesetxzqh'/>, '行政区划选取', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
			}).then(() => {
				if($this.$refs.scopesetxzqh.provincePost.option.length===0){
					return false;
				}else if(!$this.$refs.scopesetxzqh.cityPost.value){
					$this.myCommon.clearScope();
					setPolygon($this.$refs.scopesetxzqh.provincePost,$this.$refs.scopesetxzqh.provincePost.option);
				}else if(!$this.$refs.scopesetxzqh.countyPost.value){
					$this.myCommon.clearScope();
					setPolygon($this.$refs.scopesetxzqh.cityPost,$this.$refs.scopesetxzqh.cityPost.option);
				}else if(!$this.$refs.scopesetxzqh.streetPost.value){
					$this.myCommon.clearScope();
					setPolygon($this.$refs.scopesetxzqh.countyPost,$this.$refs.scopesetxzqh.countyPost.option);
				}else if($this.$refs.scopesetxzqh.streetPost.value){
					for(let i=0;i<$this.$refs.scopesetxzqh.streetPost.option.length;i++){
						if($this.$refs.scopesetxzqh.streetPost.value===$this.$refs.scopesetxzqh.streetPost.option[i].label){
							var center = $this.$refs.scopesetxzqh.streetPost.option[i].center;
							map.setView(L.latLng(center.split(",")[1],center.split(",")[0]),$this.$refs.scopesetxzqh.streetPost.zoom);
						}
					}
				}
				function setPolygon(data,option){
					for(let i=0;i<option.length;i++){
						if(data.value===option[i].label){
							var temp = option[i].polyline.split("|");
							var temp_latlngs =[];
							for(let j=0;j<temp.length;j++){
								var tempPoints=temp[j].split(";");
								var latlngs =[];
								for(let f=0;f<tempPoints.length;f++){
									var temp_lnglat=$this.gcj02towgs84(parseFloat(tempPoints[f].split(",")[0]),parseFloat(tempPoints[f].split(",")[1]));
									var latlng = L.latLng(temp_lnglat[1],temp_lnglat[0]);
									latlngs.push(latlng);
								}
								temp_latlngs.push(latlngs);
							}
							let polygon = L.polygon(temp_latlngs,$this.$data.rectAngleOptions).addTo(map);
							polygon.bindTooltip("单击下载",$this.$data.tipOptions);
							$this.bindEvent(polygon);
							var geojson = $this.myCommon.get_geojson(polygon);
							$this.myCommon.update_scopeInfo(true,option[i].adcode,polygon,geojson);
							var center = option[i].center;
							map.setView(L.latLng(center.split(",")[1],center.split(",")[0]),data.zoom);
						}
					}
				}
			}).catch(() => {
				
			});
		}else if(post.name==="删除范围"){
			if($this.$store.state.scopeInfo.scopeLayer.length!==0){
				$this.$confirm('范围删除后不可恢复, 是否继续?', '删除范围', {
				    confirmButtonText: '确定',
				    cancelButtonText: '取消',
					closeOnClickModal:false,
				    type: 'warning'
				}).then(() => {
					$this.myCommon.clearScope();
				}).catch(() => {
				});
			}else{
				$this.$alert('当前没有范围', '提示', {confirmButtonText: '确定',});
			}
		}
  	},
	bindEvent(polygon){
		var $this = this;
		polygon.on("mousedown",function(){
			$(".topButton").each(function(){
				if($(this).text()==="地图下载"){
					$(this).trigger("click");
				}
			});
		})
		
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
</style>