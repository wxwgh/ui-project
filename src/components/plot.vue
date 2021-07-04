<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in plotPost" :class="{tabMouseOver:post.isShow}" @click="plotClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>标绘</span>
		</div>
	</div>
</template>

<script>
export default {
  name: 'plot',
  data(){
    return {
		plotPost:[
			{
				name:"点",
				url:require('../assets/vectorplot/point.png'),
				isShow:false,
				
			},
			{
				name:"线",
				url:require('../assets/vectorplot/line.png'),
				isShow:false,
				
			},
			{
				name:"面",
				url:require('../assets/vectorplot/duobianxing.png'),
				isShow:false,
				
			},
		],
	}
  },
  methods:{
	//获取当前选中图层 信息
	get_layer_info(){
		var option_value = this.$store.state.layerSelectInfo.option_value;
		//获取父节点图层
		var layer_info = "";
		var temp_layers = this.$store.state.layerGroups[0].children;
		for(let i=0;i<temp_layers.length;i++){
			if(temp_layers[i].label===option_value){
				layer_info = temp_layers[i];
			}
		}
		return layer_info;
	},
	get_attribute(layer_parent,name,layer_id){
		var header_keys = layer_parent.header_keys;
		var attribute = {}
		for(let i=0;i<header_keys.length;i++){
			if(header_keys[i]==="Name"||header_keys[i]==="name"){
				attribute[header_keys[i]]=name;
			}else if(header_keys[i]==="parentId"){
				attribute[header_keys[i]]=layer_id;
			}else{
				attribute[header_keys[i]]="用户自定义矢量标绘";
			}
			
		}
		return attribute;
	},
	plotClick(post){
		var $this = this;
		var map = this.myCommon.getMap();;
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		$this.myCommon.clearOperation();
		//当前图层类型
		var type = this.$store.state.layerSelectInfo.type;
		if(post.name==="点"){
			if(type!=="point"){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '请选择点图层'
				});
				return false;
			}
			//获取当前选中图层信息
			var layer_parent = this.get_layer_info();
			$this.myCommon.switchMouseStyle(true,map);
			map.on("mousedown",function(e){
				if(e.originalEvent.button===0){
					var latlng=e.latlng;
					var layer = L.circle(latlng, {radius: 1,color:'red',weight:1}).addTo(map);
					var features=[[latlng.lat,latlng.lng]];
					var layer_id = $this.$UUID();
					var attribute=$this.get_attribute(layer_parent,"点图层",layer_id);
					var option = {
						id:layer_id,
						parentId:layer_parent.id,
						index:"3",
						label:post.name,
						name:post.name,
						isOperation:false,
						isTip:false,
						isShow:true,
						icon:"fa fa-eye-slash",
						isSelect:true,
						type:"point",
						layer:layer,
						attribute:attribute,
						features:features,
					};
					//创建图层
					$this.myCommon.createLayer(option);
				}
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
			map.on("contextmenu",function(){
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
		}else if(post.name==="线"){
			if(type!=="line"){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '请选择线图层'
				});
				return false;
			}
			//获取当前选中图层信息
			var layer_parent = this.get_layer_info();
			$this.myCommon.switchMouseStyle(true,map);
			var point_first=null;
			var line = null;
			var lines =[];
			var points = [];
			map.on("mousedown",function(e){
				if(e.originalEvent.button===0){
					if(!point_first){
						point_first=e.latlng;
						points.push([e.latlng.lat,e.latlng.lng]);
					}
					if(point_first&&point_first!==e.latlng){
						var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
						lines.push(tempLine);
						points.push([e.latlng.lat,e.latlng.lng]);
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
			})
			map.on("contextmenu",function(e){
				if(line!=null){
					line.remove();
				}
				if(point_first&&point_first!==e.latlng){
					var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]], {color: "red",weight:1}).addTo(map);
					lines.push(tempLine);
					points.push([e.latlng.lat,e.latlng.lng]);
				}
				for(let i=0;i<lines.length;i++){
					lines[i].remove();
				}
				var layerLine = L.polyline(points, {color: "red",weight:1}).addTo(map);
				var layer_id = $this.$UUID();
				var attribute=$this.get_attribute(layer_parent,"线图层",layer_id);
				var option = {
					id:layer_id,
					parentId:layer_parent.id,
					index:"3",
					label:post.name,
					name:post.name,
					isTip:false,
					isOperation:false,
					isShow:true,
					icon:"fa fa-eye-slash",
					isSelect:true,
					type:"line",
					layer:layerLine,
					attribute:attribute,
					features:points,
				};
				//创建图层
				$this.myCommon.createLayer(option);
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
		}else if(post.name==="面"){
			if(type!=="region"){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '请选择面图层'
				});
				return false;
			}
			//获取当前选中图层信息
			var layer_parent = this.get_layer_info();
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
						points.push([point_first.lat,point_first.lng]);
					}
					if(point_first&&point_first!==e.latlng){
						var tempLine=L.polyline([[point_first.lat,point_first.lng],[e.latlng.lat,e.latlng.lng]],{color: "red",weight:1}).addTo(map);
						lines.push(tempLine);
						points.push([e.latlng.lat,e.latlng.lng]);
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
					points.push([e.latlng.lat,e.latlng.lng]);
					for(let i=0;i<lines.length;i++){
						lines[i].remove();
					}
					var layer_id = $this.$UUID();
					var attribute=$this.get_attribute(layer_parent,"面图层",layer_id);
					var layerPolygon = $this.myCommon.createPolygon(points);
					var option = {
						id:layer_id,
						parentId:layer_parent.id,
						index:"3",
						label:post.name,
						name:post.name,
						isTip:false,
						isOperation:false,
						isShow:true,
						icon:"fa fa-eye-slash",
						isSelect:true,
						type:"region",
						layer:layerPolygon,
						attribute:attribute,
						features:points,
					};
					//创建图层
					$this.myCommon.createLayer(option);
				}
				$this.myCommon.unbindMapEvent(map);
				$this.myCommon.switchMouseStyle(false,map);
			})
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
