<template>
	<el-tree :data="get_data" :props="{label:'name',children:'districts'}" :expand-on-click-node="false"
		@node-click="node_click"></el-tree>
</template>

<script>
	export default {
		name: 'navigationtree',
		data() {
			return {

			}
		},
		computed: {
			get_data: function() {
				return this.$store.state.navigation_tree;
			},
		},
		methods: {
			node_click(data) {
				var $this = this;
				$this.$store.state.loading = true;
				var map = this.myCommon.getMap();;
				this.myCommon.unbindMapEvent(map);
				this.myCommon.switchMouseStyle(false, map);
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
				$this.myCommon.clear_scope_layers();
				var key = this.$store.state.gaodeKey;
				var url = "https://restapi.amap.com/v3/config/district?subdistrict=0&showbiz=false&extensions=all&key=" +
					key + "&s=rsv3&output=json&keywords=" + data.adcode +
					"&callback=jsonp_300354_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4&csid=7C3B60ED-0C39-46A6-891E-A0D28DA8864B&sdkversion=1.4.15";
				this.axios({
					method: 'get',
					url: url
				}).then(function(result) {
					var temp_data = JSON.parse(result.data.substring(result.data.indexOf("(") + 1, result.data
						.length - 1));
					console.log(temp_data)
					var temp = temp_data.districts[0].polyline.split("|");
					var coordinates = [];
					for (let j = 0; j < temp.length; j++) {
						var temp_points = temp[j].split(";");
						var coordinate = [];
						for (let f = 0; f < temp_points.length; f++) {
							// var temp_lnglat = $this.gcj02towgs84(parseFloat(temp_points[f].split(",")[0]),
							// 	parseFloat(temp_points[f].split(",")[1]));
							// var coordinates = L.latLng(temp_lnglat[1],temp_lnglat[0]);
							coordinate.push([parseFloat(temp_points[f].split(",")[0]), parseFloat(temp_points[f].split(",")[1])]);
							// coordinate.push([temp_lnglat[0], temp_lnglat[1]]);
						}
						coordinates.push([coordinate]);
					}
					//判断是否有网格图层
					if ($this.$store.state.show_set.grid_layer.length > 0) {
						//判断是否不想交
						//通过行政区划范围 创建turf多多边型
						var xz_polygon = $this.turf.multiPolygon(coordinates);
						var features = $this.$store.state.show_set.grid_geojson.features;
						var intersect_features = [];
						//遍历网格要素集合
						for (let i = 0; i < features.length; i++) {
							// 根据网格要素创建turf 多边形
							var grid_polygon = $this.turf.polygon(features[i].geometry.coordinates);
							//判断是否不相交 如果为true则不相交
							var flag = $this.turf.booleanDisjoint(xz_polygon, grid_polygon);
							if (!flag) {
								//记录相交网格的要素
								intersect_features.push(features[i]);
							}
						}
						if (intersect_features.length === 0) {
							$this.$message({
								showClose: true,
								type: 'error',
								message: '当前分幅格网与设置范围无相交节点,请重新绘制格网或重新设置范围'
							});
							$this.$store.state.loading = false;
							return false;
						}
						var geojson = {
							type: "FeatureCollection",
							features: intersect_features
						}
						var polygon = L.geoJSON(geojson, {
							style: function(feature) {
								return {
									color: '#0157F0',
									weight: 1,
									fillOpacity: 0.3,
									className: "layerCursor"
								}
							},
							onEachFeature: function(feature, layer) {
								layer.bindTooltip("单击下载", {
									direction: "right",
									sticky: true,
									offset: L.point(5, 0)
								})
								$this.myCommon.update_scope_layers(layer);
							}
						}).addTo(map);
						polygon.on("mousedown", function() {
							if($this.$store.state.map_container.layer_type=="WMS"){
								$this.$message({
									showClose: true,
									type: 'error',
									message: 'WMS类型服务不支持下载'
								});
								//清空范围
								$this.myCommon.clearScope();
								$this.myCommon.clear_scope_layers();
							}else{
								$(".topButton").each(function(){
									if($(this).text()==="地图下载"){
										$(this).trigger("click");
									}
								});
							}
						})
						$this.myCommon.update_scopeInfo(false, "", [polygon], geojson);
						var center = temp_data.districts[0].center;
						map.flyToBounds(polygon.getBounds());
					} else {
						let feature = {
							type: "Feature",
							properties: {
								id: "行政区划面"
							},
							geometry: {
								type: "MultiPolygon",
								coordinates: coordinates
							},
						};
						geojson = {
							type: "FeatureCollection",
							features: [feature]
						}
						var polygon = L.geoJSON(geojson, {
							style: function(feature) {
								return {
									color: '#0157F0',
									weight: 1,
									fillOpacity: 0.3,
									className: "layerCursor"
								}
							},
							onEachFeature: function(feature, layer) {
								layer.bindTooltip("单击下载", {
									direction: "right",
									sticky: true,
									offset: L.point(5, 0)
								})
								$this.myCommon.update_scope_layers(layer);
							}
						}).addTo(map);
						polygon.on("mousedown", function() {
							if($this.$store.state.map_container.layer_type=="WMS"){
								$this.$message({
									showClose: true,
									type: 'error',
									message: 'WMS类型服务不支持下载'
								});
								//清空范围
								$this.myCommon.clearScope();
								$this.myCommon.clear_scope_layers();
							}else{
								$(".topButton").each(function(){
									if($(this).text()==="地图下载"){
										$(this).trigger("click");
									}
								});
							}	
						})
						$this.myCommon.update_scopeInfo(true, temp_data.districts[0].adcode, [polygon], geojson);
						var center = temp_data.districts[0].center;
						map.flyToBounds(polygon.getBounds());
						console.log(polygon.getBounds())
					}
					$this.$store.state.loading = false;
				})
			},
		},
	}
</script>

<style lang="less">
</style>
