<template>
	<div class="topButtonsParent">
		<div class="show_set_parent">
			<el-checkbox v-model="checked" class="show_set_checkbox" @change="check_change(checked)">显示图幅及编号</el-checkbox>
			<el-select v-model="option_value" size="mini" class="show_set_select" @change ="select_change(option_value)">
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
  data(){
    return {
		checked:false,
		option_value:"未选择",
		options:[
			{
				value:"1:100万",
				label:"1000000"
			},
			{
				value:"1:50万",
				label:"500000"
			},
			{
				value:"1:25万",
				label:"250000"
			},
			{
				value:"1:10万",
				label:"100000"
			},
			{
				value:"1:5万",
				label:"50000"
			},
			{
				value:"1:2.5万",
				label:"25000"
			},
			{
				value:"1:1万",
				label:"10000"
			},
			{
				value:"1:5000",
				label:"5000"
			},
		],
	}
  },
  methods:{
	// 多选框点击事件
	check_change(value){
		
		console.log(value)
	},
  	select_change(value){
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		
		var bounds = map.getBounds();
		var west = bounds.getWest();
		var south = bounds.getSouth();
		var east = bounds.getEast();
		var north = bounds.getNorth();
		// 生成格网json
		let lngDiff = 0;
		let latDiff = 0;
		let scaleCode = '';
		var features=this.$store.state.show_set.grid_geojson.features;
		var text_features = this.$store.state.show_set.text_geojson.features;
		// 获取比例尺
		var scale = ""
		for(let i=0;i<this.options.length;i++){
			if(this.options[i].value === value){
				scale = parseInt(this.options[i].label);
			}
		}
		switch (scale) {
			case 1000000:
				lngDiff = 6;
				latDiff = 4;
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
		const GridX0 = -180;
		const GridX1 = 180;
		const GridY0 = -88;
		const GridY1 = 88;
		let x0 = Math.max(GridX0, west);
		let y0 = Math.max(GridY0, south);
		let x1 = Math.min(GridX1, east);
		let y1 = Math.min(GridY1, north);
		if (((x1 - x0) < lngDiff) || ((y1 - y0) < latDiff)) {
			return null;
		}
		
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
				var text_center = L.polygon(coordinates).getBounds().getCenter();
				var text_coordinates=[text_center.lat,text_center.lng];
				millionCol = (millionCol<10)?('0'+millionCol):millionCol;
				let gridID = Hemisphere + millionRowCode[millionRow] + millionCol;
				if(scaleCode != '') {
					// 计算当前分幅在 1:100万 分幅内的行列号
					// 注意，这里行列号从左向右，从北向南，从1开始编号
					let colID = parseInt((fractional((gcx -GridX0)/6)*6)/lngDiff) + 1;
					let rowID = parseInt((fractional((GridY1 - gcy)/4)*4)/latDiff) + 1;
					gridID += scaleCode + formatInt(rowID,3)  + formatInt(colID,3);
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
				let text_feature = {
					type: "Feature",
					geometry: {
						type: "Point",
						coordinates: text_coordinates
					},
					properties: {
						id: gridID,
						fanwei:'西:'+gx0+' 东:' + gx1 + ' 南:'+gy0+' 北:'+gy1
					}
				};
				features.push(feature);
				text_features.push(text_feature);
			}
		}
		// 获取小数部分
		function fractional(x) {
		   x = Math.abs(x);
		   return x - Math.floor(x);
		}
		function formatInt(x, len) {
		    let result = '' + x;
		    len = len - result.length;
		    while(len > 0) {
		        result = '0'+result;
		        len--;
		    }
		    return result;
		}
		var grid_layer = L.geoJSON(this.$store.state.show_set.grid_geojson, {
			style: function (feature) {
				return {
					color: 'red',
					weight:0.5,
					fillOpacity:0
				};
			},
		}).addTo(map);
		//生成编号 json
		for(let i=0;i<text_features.length;i++){
			var icon = L.divIcon({
				html:text_features[i].properties.id,
				iconSize:100,
				className:"marker_class",
			})
			var marker = L.marker([text_features[i].geometry.coordinates[1],text_features[i].geometry.coordinates[0]], { icon: icon }).addTo(map);
			this.$store.state.show_set.text_layers.push(marker);
		}
  	},
	
  },
}
</script>

<style lang="less">
.show_set_parent{
	display: flex;
	flex-direction: column;
	flex-wrap:nowrap;
	justify-content:space-around;
	height:64px;
}
.show_set_checkbox{
	width:80%;
}
.show_set_select{
	width:90%;
	margin-left:5%;
}
.marker_class{
	font-size:14px;
}
</style>
