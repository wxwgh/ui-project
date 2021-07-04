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
import scopesetimport from '@/components/scopesetimport.vue';
export default {
  name: 'scopeset',
  components:{
  	scopesetxzqh,
	scopesetimport,
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
				name:"导入范围",
				url:require('../assets/mapdownload/importscope.png'),
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
						tempRectangle.bindTooltip("单击下载",$this.tipOptions);
						$this.bindEvent(tempRectangle);
						
						$this.myCommon.update_scopeInfo(false,"",[tempRectangle]);
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
					var polygon  = L.polygon(points,$this.rectAngleOptions).addTo(map);
					polygon.bindTooltip("单击下载",$this.tipOptions);
					$this.bindEvent(polygon);
					$this.myCommon.update_scopeInfo(false,"",[polygon]);
					$this.myCommon.updateDownLoadTable();
				}
				$this.myCommon.switchMouseStyle(false,map);
				$this.myCommon.unbindMapEvent(map);
			})
		}else if(post.name==="行政区划"){
			$(".mapListBottom span").each(function(){
				if($(this).text()==="快速导航"){
					$(this).trigger("click");
				}
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
		}else if(post.name==="导入范围"){
			$this.$confirm(<scopesetimport ref='scopesetimport'/>, '导入范围', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						$this.$refs.scopesetimport.init_panel();
						done();
					}else if(action==="cancel"){
						$this.$refs.scopesetimport.init_panel();
						done();
					}else if(action==="confirm"){
						var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
						var importRegex = /(\.shp)|(\.csv)|(\.kml)/;
						var indexRegex = /[0-9]+/;
						if(!taskRegex.test($this.$refs.scopesetimport.layer_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '图层名称,格式不正确'
							});
							return false;
						}
						if(!importRegex.test($this.$refs.scopesetimport.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不支持当前文件格式'
							});
							return false;
						}
						if($this.$refs.scopesetimport.import_format==="csv"&&$this.$refs.scopesetimport.radio === "面"){
							if(!indexRegex.test($this.$refs.scopesetimport.geometry)){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '空间对象不能为空'
								});
								return false;
							}
						}
						if(!$this.$refs.scopesetimport.is_exists){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '文件不存在或坐标系不支持'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var coordinate="";
				for(let i=0;i<$this.$refs.scopesetimport.options.length;i++){
					if($this.$refs.scopesetimport.option_value===$this.$refs.scopesetimport.options[i].value){
						coordinate = $this.$refs.scopesetimport.options[i].label;
					}
				}
				var temp_info={
					file_path:$this.$refs.scopesetimport.import_file_path,
					import_format:$this.$refs.scopesetimport.import_format,
					coordinate:coordinate,
				}
				if($this.$refs.scopesetimport.import_format==="csv"&&$this.$refs.scopesetimport.feature_type==="region"){
					temp_info.geometry = $this.$refs.scopesetimport.geometry-1;
					temp_info.feature_type=$this.$refs.scopesetimport.feature_type;
				}
				//开启loading
				$this.$store.state.loading=true;
				get_import_features(temp_info);
				async function get_import_features(temp_info){
					var result = await eel.get_import_features(temp_info)();
					console.log(result);
					if(result.code===204){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '导入失败,请检查数据是否正确'
						});
						$this.$refs.scopesetimport.init_panel();
						//关闭loading
						$this.$store.state.loading=false;
						return false;
					}else{
						$this.myCommon.clearScope();
						var polygons =[];
						for(let i=0;i<result.data.length;i++){
							var polygon = L.polygon(result.data[i].features,$this.rectAngleOptions).addTo(map);
							polygon.bindTooltip("单击下载",$this.tipOptions);
							$this.bindEvent(polygon);
							polygons.push(polygon);
						}
						$this.myCommon.update_scopeInfo(false,"",polygons);
						$this.myCommon.updateDownLoadTable();
						$this.$refs.scopesetimport.init_panel();
						//关闭loading
						$this.$store.state.loading=false;
					}
				}
			}).catch(() => {
				
			});
		}
  	},
	bindEvent(polygon){
		var $this = this;
		polygon.on("mousedown",function(){
			if($this.$store.state.peration_rectangle!==""){
				$this.$store.state.peration_rectangle.remove();
			}
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