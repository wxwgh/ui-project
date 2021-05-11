<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in measurePost" :class="{tabMouseOver:post.isShow}" @click="measureClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>量算相关</span>
		</div>
	</div>
</template>

<script>
import measuresetbox from '@/components/measuresetbox.vue';
export default {
  name: 'measure',
  data(){
    return {
		layers:[],
		measurePost:[
			{
				name:"测距",
				url:require('../assets/maptools/distance.png'),
				isShow:false,
				
			},
			{
				name:"测面",
				url:require('../assets/maptools/area.png'),
				isShow:false,
				
			},
			{
				name:"单位设置",
				url:require('../assets/maptools/unitset.png'),
				isShow:false,
				
			},
			{
				name:"删除结果",
				url:require('../assets/maptools/clear.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
  	measureClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
  		if(post.name==="测距"){
			$this.myCommon.switchMouseStyle(true,map);
			var point_first=null;
			var line = null;
			var total_distance=0;
			//绑定事件
			map.on("mousedown",function(e){
				//判断是否是左键
				if(e.originalEvent.button===0){
					if(point_first===null){
						point_first=e.latlng;
						$this.createMarker(point_first,map);
					}
					if(point_first&&point_first!==e.latlng){
						//计算两点距离
						var first = point_first;
						var end = e.latlng;
						var temp_distance = first.distanceTo(end);
						total_distance+=temp_distance;
						var distance = "";
						var unit = $this.$store.state.measure_unit.old_distance_unit;
						if(unit==="米"){
							distance = temp_distance.toFixed(2)+unit;
						}else if(unit==="千米"){
							distance = (temp_distance/1000).toFixed(2)+unit;
						}else if(unit==="英里"){
							distance = (temp_distance/1609.344).toFixed(2)+unit;
						}else if(unit==="丈"){
							distance = (temp_distance/3.33).toFixed(2)+unit;
						}
						$this.createMarker(e.latlng,map,distance);
						var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
						$this.$data.layers.push(tempLine);
						
						point_first=e.latlng;
					}
				}
				
			});
			map.on("mousemove",function(e){
				if(line!=null){
					line.remove();
				}
				if(point_first){
					line=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
				}
			});
			map.on("contextmenu",function(e){
				if(line!=null){
					line.remove();
					
				}
				if(point_first){
					var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
					$this.$data.layers.push(tempLine);
					var first = point_first;
					var end = e.latlng;
					var temp_distance = first.distanceTo(end);
					total_distance+=temp_distance;
					var unit = $this.$store.state.measure_unit.old_distance_unit;
					if(unit==="米"){
						total_distance = total_distance.toFixed(2)+unit;
					}else if(unit==="千米"){
						total_distance = (total_distance/1000).toFixed(2)+unit;
					}else if(unit==="英里"){
						total_distance = (total_distance/1609.344).toFixed(2)+unit;
					}else if(unit==="丈"){
						total_distance = (total_distance/3.33).toFixed(2)+unit;
					}
					$this.createMarker(e.latlng,map,total_distance);
				}
				$this.myCommon.switchMouseStyle(false,map);
				$this.myCommon.unbindMapEvent(map);
			});
			
		}else if(post.name==="测面"){
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
						
						var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
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
					line=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
				}else if(point_first&&point_end){
					line=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
					line2=L.polyline([[point_end.lat,point_end.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
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
					var temp=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
					var temp2=L.polyline([[point_end.lat,point_end.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
					lines.push(temp);
					lines.push(temp2);
					points.push(e.latlng);
					for(let i=0;i<lines.length;i++){
						lines[i].remove();
					}
					//获取面积
					var coordinates=[];
					for(let i=0;i<points.length;i++){
						var coordinate =[points[i].lng,points[i].lat];
						coordinates.push(coordinate);
						if(i===points.length-1){
							var temp = [points[0].lng,points[0].lat];
							coordinates.push(temp);
						}
					}
					var turfPolygon = $this.turf.polygon([coordinates]);
					var temp_area = $this.turf.area(turfPolygon);
					var unit = $this.$store.state.measure_unit.old_area_unit;
					var area="";
					if(unit==="平方米"){
						area = temp_area.toFixed(2)+unit;
					}else if(unit==="平方千米"){
						area = (temp_area/1000000).toFixed(2)+unit;
					}else if(unit==="亩"){
						area = (temp_area/666.66).toFixed(2)+unit;
					}else if(unit==="公顷"){
						area = (temp_area/10000).toFixed(2)+unit;
					}
					console.log(area);
					
					var polygon  = L.polygon(points,{color: 'red',weight:1,className:"polygonClass"}).addTo(map);
					var popup = L.popup({autoClose:false,closeOnClick:false}).setLatLng(polygon.getCenter()).setContent(area).openOn(map);
					polygon.bindPopup(popup);
					$this.$data.layers.push(polygon);
				}
				$this.myCommon.switchMouseStyle(false,map);
				$this.myCommon.unbindMapEvent(map);
			})
		}else if(post.name==="单位设置"){
			//当前选中赋值为历史选中
			$this.$store.state.measure_unit.distance_unit=$this.$store.state.measure_unit.old_distance_unit;
			$this.$store.state.measure_unit.area_unit=$this.$store.state.measure_unit.old_area_unit;
			$this.$confirm(<measuresetbox ref='measuresetbox'/>, '单位设置', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
			}).then(() => {
				// 历史选中赋值为当前选中
				$this.$store.state.measure_unit.old_distance_unit=$this.$store.state.measure_unit.distance_unit;
				$this.$store.state.measure_unit.old_area_unit=$this.$store.state.measure_unit.area_unit;
			}).catch(() => {
				
			});
		}else if(post.name==="删除结果"){
			if($this.$data.layers.length>0){
				this.$confirm('结果删除后不可恢复, 是否继续?', '删除结果', {
				    confirmButtonText: '确定',
				    cancelButtonText: '取消',
					closeOnClickModal:false,
				    type: 'warning'
				}).then(() => {
					var layers = $this.$data.layers;
					if(layers.length>0){
						for(let i=0;i<layers.length;i++){
							layers[i].remove();
						}
						layers=[];
					}
				}).catch(() => {
				});
			}else{
				$this.$alert('当前没有计算结果', '删除结果', {confirmButtonText: '确定',});
			}
			
		}
  	},
	createMarker(point,map,distance){
		var tempIcon = L.icon({
			iconUrl: require('../assets/marker/marker-icon-green.png'),
			shadowUrl: require('../assets/marker/marker-shadow.png'),
			iconSize: [25, 41],
			iconAnchor: [12, 41],
			popupAnchor: [1, -34],
			shadowSize: [41, 41]
		});
		var tempLayer=null;
		if(distance){
			tempLayer = L.marker(point, {icon: tempIcon}).addTo(map);
			var popup = L.popup({autoClose:false,closeOnClick:false}).setLatLng(point).setContent(distance).openOn(map);
			tempLayer.bindPopup(popup);
		}else{
			tempLayer = L.marker(point, {icon: tempIcon}).addTo(map);
		}
		this.$data.layers.push(tempLayer);
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
.polygonClass{
	cursor:pointer;
}
</style>
