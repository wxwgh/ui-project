<template>
	<div class="topButtonsParent">
		<div class="show_set_parent">
			<el-checkbox v-model="checked" class="show_set_checkbox" @change="check_change(checked)">显示图幅及编号
			</el-checkbox>
			<el-select v-model="option_value" size="mini" class="show_set_select" @change="select_change(option_value)">
				<el-option v-for="post in options" :labek="post.label" :value="post.value"></el-option>
			</el-select>
		</div>
		<div class="description">
			<span>分幅设置</span>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'showset',
		data() {
			return {
				checked: true,
				option_value: "未选择",
				options: [
					{
						value: "未选择",
						label: "未选择",
						zoom: 3,
					},
					{
						value: "1:100万",
						label: 1000000,
						zoom: 3,
					},
					{
						value: "1:50万",
						label: 500000,
						zoom: 4,
					},
					{
						value: "1:25万",
						label: 250000,
						zoom: 5,
					},
					{
						value: "1:10万",
						label: 100000,
						zoom: 6,
					},
					{
						value: "1:5万",
						label: 50000,
						zoom: 7,
					},
					{
						value: "1:2.5万",
						label: 25000,
						zoom: 9,
					},
					{
						value: "1:1万",
						label: 10000,
						zoom: 10,
					},
					{
						value: "1:5000",
						label: 5000,
						zoom: 11,
					},
				],
			}
		},
		methods: {
			// 多选框点击事件
			check_change(value){
				var map = this.myCommon.getMap();
				// 如果为真表示选中 显示图幅和编号
				if (value&&this.option_value!=="未选择") {
					this.$store.state.show_set.grid_layer[0].addTo(map);
				//隐藏图幅和编号
				}else if(!value&&this.option_value!=="未选择"){
					this.$store.state.show_set.grid_layer[0].remove();
				}
			},
			//js生成geojson文件 以浏览器下载的方式保存至本地
			test_check_change(value) {
				var temp_list=[
					"5000-11.json"
				];
				for(let i=0;i<temp_list.length;i++){
					var scale = temp_list[i].split("-")[0];
					var data = this.get_geojson(parseInt(scale));
					this.save_json(data,temp_list[i]);
				}
			},
			//下拉框改变事件
			select_change(value) {
				var $this =this;
				if(value==="未选择"){
					// 清除分幅Layer
					this.myCommon.clear_show_set_layer();
					return false;
				}
				var map = this.myCommon.getMap();
				// 清除分幅Layer
				this.myCommon.clear_show_set_layer();
				var scale = "";
				var zoom = "";
				for(let i=0;i<this.options.length;i++){
					if(value === this.options[i].value){
						scale = this.options[i].label;
						zoom = this.options[i].zoom;
					}
				}
				// if(value!=="1:100万"&&value!=="1:50万"){
				// 	var temp_zoom = map.getZoom();
				// 	if(temp_zoom<zoom){
				// 		$this.$message({
				// 		    showClose: true,
				// 			type: 'error',
				// 		    message: '当前比例尺级别过小,请放大地图重试'
				// 		});
				// 		$this.option_value = "未选择";
				// 		return false;
				// 	}
				// }
				$this.get_layer(scale,zoom);
				
			},
			get_layer(scale,zoom){
				var $this = this;
				var map = this.myCommon.getMap();
				var bounds = map.getBounds();
				//获取geojson和layer
				var grid_geojson = $this.get_geojson(scale,bounds);
				var grid_layer = L.geoJSON(grid_geojson, {
					style: function(feature) {
						return {
							color: 'red',
							weight: 0.5,
							fillOpacity: 0
						};
					},
					onEachFeature: function(feature, layer) {
						layer.bindTooltip(feature.properties.id);
					}
				})
				// 赋值全局对象
				$this.$store.state.show_set.grid_geojson = grid_geojson;
				$this.$store.state.show_set.grid_layer.push(grid_layer);
				$this.$store.state.show_set.zoom=zoom;
				if($this.checked){
					$this.$store.state.show_set.grid_layer[0].addTo(map);
				}
			},
			get_geojson(scale,bounds){
				let lngDiff = 0;
				let latDiff = 0;
				let scaleCode = '';
				switch (scale) {
					case 1000000:
						lngDiff = 6;
						latDiff = 4;
						scaleCode = '';
						break;
					case 500000:
						lngDiff = 3;
						latDiff = 2;
						scaleCode = 'B';
						break;
					case 250000:
						lngDiff = 1.5;
						latDiff = 1;
						scaleCode = 'C';
						break;
					case 100000:
						lngDiff = 0.5;
						latDiff = 1 / 3;
						scaleCode = 'D';
						break;
					case 50000:
						lngDiff = 0.25;
						latDiff = 1 / 6;
						scaleCode = 'E';
						break;
					case 25000:
						lngDiff = 0.125;
						latDiff = 1 / 12;
						scaleCode = 'F';
						break;
					case 10000:
						lngDiff = 0.0625;
						latDiff = 1 / 24;
						scaleCode = 'G';
						break;
					case 5000:
						lngDiff = 0.03125;
						latDiff = 1 / 48;
						scaleCode = 'H';
						break;
					default:
						return null;
				}
				var west = bounds.getWest();
				var south = bounds.getSouth();
				var east = bounds.getEast();
				var north = bounds.getNorth();
				const GridX0 = -180;
				const GridX1 = 180;
				const GridY0 = -88;
				const GridY1 = 88;
				let x0 = Math.max(GridX0, west);
				let y0 = Math.max(GridY0, south);
				let x1 = Math.min(GridX1, east);
				let y1 = Math.min(GridY1, north);
				// if (((x1 - x0) < lngDiff) || ((y1 - y0) < latDiff)) {
				// 	return null;
				// }
				let features = [];
				// 计算标准分幅网格行列范围
				const col0 = parseInt((x0 - GridX0) / lngDiff);
				const col1 = parseInt((x1 - GridX0) / lngDiff);
				const row0 = parseInt((y0 - GridY0) / latDiff);
				const row1 = parseInt((y1 - GridY0) / latDiff);
				const millionRowCode = 'ABCDEFGHIJKLMNOPQRSTUV';
				for (let row = row0; row <= row1; row++) {
					let gy0 = GridY0 + row * latDiff;
					let gy1 = gy0 + latDiff;
					let gcy = (gy0+gy1)*0.5;    // 分幅中心点 y 坐标
					let millionRow = parseInt((gy0 - 0)/4); // 1:100分幅行号
					let Hemisphere = '';   // 南北半球标志
					if(millionRow < 0){
						millionRow = -1-millionRow;
						Hemisphere = 'S';
					}
					for (let col = col0; col <= col1; col++) {
						let gx0 = GridX0 + col * lngDiff;
						let gx1 = gx0 + lngDiff;
						let gcx = (gx0+gx1)*0.5;    // 分幅中心点 x 坐标
						let millionCol = parseInt((gcx-GridX0)/6)+1;  // 1:100分幅列号(从1开始)
						var coordinates = [[
							[gx0, gy0],
							[gx1, gy0],
							[gx1, gy1],
							[gx0, gy1],
							[gx0, gy0]
						]];
						millionCol = (millionCol<10)?('0'+millionCol):millionCol;
						let gridID = Hemisphere + millionRowCode[millionRow] + millionCol;
						if(scaleCode != '') {
							// 计算当前分幅在 1:100万 分幅内的行列号
							// 注意，这里行列号从左向右，从北向南，从1开始编号
							let colID = parseInt((this.fractional((gcx -GridX0)/6)*6)/lngDiff) + 1;
							let rowID = parseInt((this.fractional((GridY1 - gcy)/4)*4)/latDiff) + 1;
							gridID += scaleCode + this.formatInt(rowID,3)  + this.formatInt(colID,3);
						}
						let feature = {
							type: "Feature",
							geometry: {
								type: "Polygon",
								coordinates: coordinates
							},
							properties: {
								id: gridID,
								fanwei:'西:'+gx0+' 东:' + gx1 + ' 南:'+gy0+' 北:'+gy1
							}
						};
						features.push(feature);
					}
				}
				return {
					type: "FeatureCollection",
					features: features
				};
			},
			save_json(data, filename){
				var temp_data=JSON.stringify(data)
				var blob = new Blob([temp_data], {type: 'text/json'}),
				e = document.createEvent('MouseEvents'),
				a = document.createElement('a')
				a.download = filename
				a.href = window.URL.createObjectURL(blob)
				a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
				e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
				a.dispatchEvent(e)
			},
			// 获取小数部分
			fractional(x){
			   x = Math.abs(x);
			   return x - Math.floor(x);
			},
			formatInt(x, len){
			    let result = '' + x;
			    len = len - result.length;
			    while(len > 0) {
			        result = '0'+result;
			        len--;
			    }
			    return result;
			}
		},
	}
</script>

<style lang="less">
	.show_set_parent {
		display: flex;
		flex-direction: column;
		flex-wrap: nowrap;
		justify-content: space-around;
		height: 64px;
	}

	.show_set_checkbox {
		width: 80%;
	}

	.show_set_select {
		width: 90%;
		margin-left: 5%;
	}

	.marker_class {
		font-size: 14px;
	}
</style>
