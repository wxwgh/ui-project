<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in operationPost" :class="{tabMouseOver:post.isShow}" @click="operationClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>对象操作</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'plot',
  data(){
    return {
		operationPost:[
			{
				name:"选择",
				url:require('../assets/vectorplot/choose.png'),
				isShow:false,
				
			},
			// {
			// 	name:"平移",
			// 	url:require('../assets/vectorplot/translation.png'),
			// 	isShow:false,
				
			// },
			{
				name:"删除对象",
				url:require('../assets/vectorplot/clear.png'),
				isShow:false,
				
			},
			{
				name:"属性表",
				url:require('../assets/vectorplot/table.png'),
				isShow:false,
				
			},
			// {
			// 	name:"矢量编辑",
			// 	url:require('../assets/vectorplot/editor.png'),
			// 	isShow:false,
				
			// },
		],
	}
  },
  methods:{
	operationClick(post){
		var $this = this;
		var map = this.myCommon.getMap();
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		if(post.name==="选择"){
			$this.myCommon.switchMouseStyle(true,map);
			//清除选中
			$this.myCommon.clearOperation();
			//清空选取图层
			$this.myCommon.clear_operation_list();
			//清空表数据
			$this.myCommon.clearAttributeTable();
			var point_first=null;
			var rectangle = null;
			var points = [];
			map.on("mousedown",function(e){
				if(e.originalEvent.button===0){
					if(!point_first){
						point_first=e.latlng;
						points.push(e.latlng);
					}
					if(point_first&&point_first!==e.latlng){
						if(rectangle!=null){
							rectangle.remove();
						}
						points.push(e.latlng);
						var tempRectangle = L.rectangle(points, {color:'#0157F0',weight:1});
						var bounds = tempRectangle.getBounds();
						//西北角点 左上
						var northWest = bounds.getNorthWest();
						//西南角点 左下
						var southWest = bounds.getSouthWest();
						//东南角点 右下
						var southEast = bounds.getSouthEast();
						//东北角点 右上
						var northEast = bounds.getNorthEast();
						var tempBounds = [];
						tempBounds.push(northWest);
						tempBounds.push(southWest);
						tempBounds.push(southEast);
						tempBounds.push(northEast);
						var coordinates =[];
						for(let i=0;i<tempBounds.length;i++){
							var coordinate = [tempBounds[i].lng,tempBounds[i].lat];
							coordinates.push(coordinate);
							if(i===tempBounds.length-1){
								var temp = [tempBounds[0].lng,tempBounds[0].lat];
								coordinates.push(temp);
							}
						}
						var layer = $this.turf.polygon([coordinates]);
						//判断是否包含
						var layerGroup = $this.$store.state.layerGroups[0].children;
						var index = 0;
						for(let i=0;i<layerGroup.length;i++){
							for(let j=0;j<layerGroup[i].children.length;j++){
								if(layerGroup[i].children[j].isSelect){
									if(layerGroup[i].children[j].type==="Point"){
										var tempPoints = layerGroup[i].children[j].points;
										var point = $this.turf.point([tempPoints[0].lng, tempPoints[0].lat]);
										var flag = $this.turf.booleanContains(layer, point);
										if(flag){
											layerGroup[i].children[j].isOperation=true;
											layerGroup[i].children[j].layer.setStyle({color:"blue"});
											index++;
										}
									}else if(layerGroup[i].children[j].type==="marker"){
										var tempPoints = layerGroup[i].children[j].points;
										var point = $this.turf.point([tempPoints[0].lng, tempPoints[0].lat]);
										var flag = $this.turf.booleanContains(layer, point);
										if(flag){
											layerGroup[i].children[j].isOperation=true;
											var myIcon = L.icon({
											    iconUrl: require('../assets/marker/marker-icon-blue.png'),
											    shadowUrl: require('../assets/marker/marker-shadow.png'),
												iconSize: [25, 41],
												iconAnchor: [12, 41],
												popupAnchor: [1, -34],
												shadowSize: [41, 41],
											});
											layerGroup[i].children[j].layer.setIcon(myIcon);
											index++;
										}
										
									}else if(layerGroup[i].children[j].type==="Line"){
										var tempPoints = layerGroup[i].children[j].points;
										var tempCoordinates =[];
										for(let s=0;s<tempPoints.length;s++){
											var tempCoordinate = [tempPoints[s].lng,tempPoints[s].lat];
											tempCoordinates.push(tempCoordinate);
										}
										var line = $this.turf.lineString(tempCoordinates);
										var flag = $this.turf.booleanWithin(line, layer);
										if(flag){
											layerGroup[i].children[j].isOperation=true;
											layerGroup[i].children[j].layer.setStyle({color:"blue"});
											index++;
										}
									}else if(layerGroup[i].children[j].type==="Region"){
										var tempPoints = layerGroup[i].children[j].points;
										var tempCoordinates =[];
										for(let s=0;s<tempPoints.length;s++){
											var tempCoordinate = [tempPoints[s].lng,tempPoints[s].lat];
											tempCoordinates.push(tempCoordinate);
											if(s===tempPoints.length-1&&tempPoints[0].lng!==tempPoints[tempPoints.length-1].lng){
												var temp = [tempPoints[0].lng,tempPoints[0].lat];
												tempCoordinates.push(temp);
											}
										}
										var polygon = $this.turf.polygon([tempCoordinates]);
										var flag = $this.turf.booleanWithin(polygon, layer);
										if(flag){
											layerGroup[i].children[j].isOperation=true;
											layerGroup[i].children[j].layer.setStyle({color:"blue"});
											index++;
										}
									}
								}
							}
						}
						//根据选中对象获取 选取图层列表
						var layer_list=[];
						for(let i=0;i<layerGroup.length;i++){
							for(let j=0;j<layerGroup[i].children.length;j++){
								if(layerGroup[i].children[j].isOperation){
									var temp={
										label:layerGroup[i].label,
										type:layerGroup[i].type
									}
									layer_list.push(temp);
									break;
								}
							}
						}
						// 根据图层列表 更新表格数据
						for(let i=0;i<layerGroup.length;i++){
							if(layerGroup[i].label===layer_list[0].label){
								//更新表头
								$this.$store.state.attributeHeader = layerGroup[i].table_header;
								for(let j=0;j<layerGroup[i].children.length;j++){
									if(layerGroup[i].children[j].isOperation){
										//更新表格数据
										$this.myCommon.setAttributeData(layerGroup[i].children[j].attribute);
									}
								}
							}
							
						}
						//更新选取图层列表
						$this.myCommon.update_operation_list(layer_list);
						
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
					rectangle=L.rectangle([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color:'#0157F0',weight:1}).addTo(map);
				}
			})
			map.on("contextmenu",function(e){
				if(rectangle!=null){
					rectangle.remove();
				}
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
		}else if(post.name==="平移"){
			var flag = $this.myCommon.isOperationSelect();
			if(!flag){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前无选择对象'
				});
				return false;
			}
			map.on("contextmenu",function(){
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			});
		}else if(post.name==="删除对象"){
			var flag = $this.myCommon.isOperationSelect();
			if(!flag){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前无选择对象'
				});
				return false;
			}
			$this.$confirm('矢量删除后不可恢复, 是否继续?', '删除矢量', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
			    type: 'warning'
			}).then(() => {
				//删除选中对象
				var layerGroup = $this.$store.state.layerGroups[0].children;
				for(let i=0;i<layerGroup.length;i++){
					for(let j=0;j<layerGroup[i].children.length;j++){
						if(layerGroup[i].children[j].isOperation){
							layerGroup[i].children[j].layer.remove();
							layerGroup[i].children.splice(j,1);
							j--;
						}
					}
				}
			}).catch(() => {
			});
		}else if(post.name==="属性表"){
			var flag = $this.myCommon.isOperationSelect();
			if(!flag){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '当前无选择对象'
				});
				return false;
				// $this.$alert('当前选择对象为空,请选择对象', '提示', {confirmButtonText: '确定',}).catch(() => {});
			}
			$this.myCommon.openAttributeTable();
			
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
</style>
