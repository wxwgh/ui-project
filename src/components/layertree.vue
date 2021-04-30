<template>
	<div>
		<el-tree :data="treeDatas" default-expand-all :expand-on-click-node="false" @node-contextmenu="rightClick">
			<span class="custom-tree-node" slot-scope="{node,data}"  @click.stop="layerClick(data)">
				<el-tooltip :content="data.name" placement="right-end" effect="light" v-if="data.isTip">
					<span>
						<i class="el-icon-my-point" v-if="data.type==='marker'"></i>
						<i class="el-icon-my-point" v-else-if="data.type==='Point'"></i>
						<i class="el-icon-my-line" v-else-if="data.type==='Line'"></i>
						<i class="el-icon-my-polygon" v-else-if="data.type==='Region'"></i>
						<span>{{node.label}}</span>
					</span>
				</el-tooltip>
				<span v-else>
					<i class="el-icon-my-point" v-if="data.type==='marker'"></i>
					<i class="el-icon-my-point" v-else-if="data.type==='Point'"></i>
					<i class="el-icon-my-line" v-else-if="data.type==='Line'"></i>
					<i class="el-icon-my-polygon" v-else-if="data.type==='Region'"></i>
					<span>{{node.label}}</span>
				</span>
				<span v-if="data.index==='1'">
					<i class="el-icon-my-point" v-if="get_type==='marker'"></i>
					<i class="el-icon-my-point" v-else-if="get_type==='Point'"></i>
					<i class="el-icon-my-line" v-else-if="get_type==='Line'"></i>
					<i class="el-icon-my-polygon" v-else-if="get_type==='Region'"></i>
					<el-select :value="get_value" size="mini" class="layerSelectClass" @change="layerSelectChange">
						<el-option v-for="post in get_options" :labek="post.label" :value="post.value" >
							<i class="el-icon-my-point" v-if="post.type==='marker'"></i>
							<i class="el-icon-my-point" v-else-if="post.type==='Point'"></i>
							<i class="el-icon-my-line" v-else-if="post.type==='Line'"></i>
							<i class="el-icon-my-polygon" v-else-if="post.type==='Region'"></i>
							<span>{{post.label}}</span>
						</el-option>
					</el-select>
					<el-button size="mini" type="text" icon="el-icon-folder-add"  @click.stop="importClick(data)"></el-button>
					<el-button size="mini" type="text" icon="el-icon-plus" @click.stop="addClick(data)"></el-button>
				</span>
				<span v-else>
					<el-button size="mini" type="text" :icon="data.icon" @click.stop="selectClick(node,data)"></el-button>
					<el-button size="mini" type="text" icon="el-icon-minus" @click.stop="deleteClick(node,data)"></el-button>
				</span>
			</span>
		</el-tree>
		<div v-show="isShow" class="menuParent">
			<el-menu active-text-color="#303133">
				<el-menu-item index="1" class="menuItem" @click="exportClick()">
					<span slot="title">导出</span>
				</el-menu-item>
				<el-menu-item index="2" class="menuItem" @click="attributeClick()">
					<span slot="title">属性表</span>
				</el-menu-item>
				<el-menu-item index="3" class="menuItem" @click="renameClick()">
					<span slot="title">重命名</span>
				</el-menu-item>
			</el-menu>
		</div>
	</div>
</template>

<script>
import layertreeexportbox from '@/components/layertreeexportbox.vue';
import layertreeimportbox from '@/components/layertreeimportbox.vue';
import layeraddbox from '@/components/layeraddbox.vue';
import renamebox from '@/components/renamebox.vue';
export default {
  name: 'layertree',
  data(){
    return {
		id:this.$UUID(),
		isShow:false,
		treeDatas:this.$store.state.layerGroups,
	}
  },
  computed:{
  	  get_value:function(){
  		  return this.$store.state.layerSelectInfo.option_value;
  	  },
  	  get_options:function(){
  		  return this.$store.state.layerSelectInfo.options;
  	  },
  	  get_type:function(){
  		  return this.$store.state.layerSelectInfo.type;
  	  }
  },
  methods:{
	layerSelectChange(name){
		var options = this.$store.state.layerSelectInfo.options
		for(let i=0;i<options.length;i++){
			if(options[i].label===name){
				// 更新选中图层
				this.myCommon.update_select_layer(options[i]);
			}
		}
	},
	importClick(data){
		var $this =this;
		var map = this.myCommon.getMap();;
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		$this.myCommon.clearOperation();
		$this.$confirm(<layertreeimportbox ref='layertreeimportbox'/>, '矢量导入', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					done();
				}else if(action==="cancel"){
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					var importRegex = /\.shp/;
					if(!taskRegex.test($this.$refs.layertreeimportbox.layer_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '图层名称,格式不正确'
						});
						return false;
					}
					if(!importRegex.test($this.$refs.layertreeimportbox.import_file_path)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '不支持当前文件格式'
						});
						return false;
					}
					if($this.$refs.layertreeimportbox.isName){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '已有同名图层'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			//导入文件路径
			var temp_info={
				url:$this.$refs.layertreeimportbox.import_file_path
			}
			getFeatures(temp_info);
			async function getFeatures(temp_info){
				var datas = await eel.get_features(temp_info)();
				console.log(datas);
				var header_json = JSON.parse(datas.features[0].geojson);
				var table_header=[];
				var attribute = datas.features[0].attribute;
				attribute["id"]=header_json.id
				var temp_keys = Object.keys(attribute);
				// 将keys排序
				for(let i=0;i<temp_keys.length;i++){
					if(temp_keys[i]==="id"){
						var temp =temp_keys[0];
						temp_keys[0]=temp_keys[i];
						temp_keys[i]=temp;
						break;
					}
				}
				temp_keys.push("parentId");
				for(let i=0;i<temp_keys.length;i++){
					temp={
						id:$this.$UUID(),
						alias:temp_keys[i],
						name:temp_keys[i],
					};
					table_header.push(temp);
				};
				//创建图层父节点 类似数据集结构
				var layer_option = {
					id:$this.$UUID(),
					index:"2",
					label:$this.$refs.layertreeimportbox.layer_name,
					isTip:false,
					isPlot:true,
					isShow:true,
					type:datas.type,
					table_header:table_header,
					header_keys:temp_keys,
					icon:"fa fa-eye-slash",
					isSelect:true,
					children:[]
				}
				//创建图层
				$this.myCommon.createLayer(layer_option);
				//添加至图层选中列表
				$this.myCommon.add_select_layer(layer_option);
				//更新header
				$this.myCommon.update_attribute_header();
				// 清除选取图层列表
				$this.myCommon.clear_operation_list();
				//更新当前选取图层列表
				$this.myCommon.update_operation_list([temp]);
				//重置输入框
				$this.$refs.layertreeimportbox.layer_name="";
				
				//创建图层子节点
				for(let i=0;i<datas.features.length;i++){
					var name="";
					if(datas.features[i].attribute.Name){
						name=datas.features[i].attribute.Name;
					}else if(datas.type==="Point"){
						name="点";
					}else if(datas.type==="Line"){
						name="线";
					}else if(datas.type==="Region"){
						name="面";
					}
					var label="";
					var isTip="";
					if(name.length>12){
						label = name.substring(0,12)+"...";
						isTip=true;
					}else{
						label=name;
						isTip=false;
					}
					var icon="";
					var isSelect="";
					if(i>9){
						icon ="fa fa-eye"
						isSelect=false;
					}else{
						icon ="fa fa-eye-slash"
						isSelect=true;
					}
					var points=[];
					var layer="";
					var temp_attribute = datas.features[i].attribute;
					var temp_json = JSON.parse(datas.features[i].geojson);
					console.log(temp_json);
					temp_attribute["id"]=temp_json.id
					if(datas.type==="Point"){
						var geometry = temp_json.Point;
						var latlng = L.latLng(geometry[1],geometry[0]);
						points.push(latlng);
						if(i<=9){
							//创建地图点图层
							layer = L.circle(latlng, {radius: 1,color:'red',weight:1}).addTo(map);
						}else{
							layer=null;
						}
						
					}else if(datas.type==="Line"){
						var geometry = temp_json.Line;
						for(let j=0;j<geometry.length;j++){
							var temp=[];
							for(let x=0;x<geometry[j].length;x++){
								var latlng = L.latLng(geometry[j][x][1],geometry[j][x][0]);
								temp.push(latlng);
							}
							points.push(temp);
						}
						if(i<=9){
							layer = L.polyline(points, {color: "red",weight:1}).addTo(map);
						}else{
							layer=null;
						}
						
					}else if(datas.type==="Region"){
						var geometry = temp_json.Region;
						for(let j=0;j<geometry.length;j++){
							var temp=[];
							for(let x=0;x<geometry[j].length;x++){
								var latlng = L.latLng(geometry[j][x][1],geometry[j][x][0]);
								temp.push(latlng);
							}
							points.push(temp);
						}
						if(i<=9){
							layer = L.polygon(points,{color:'red',weight:1}).addTo(map);
						}else{
							layer=null;
						}
						
					}
					var layer_id = $this.$UUID();
					temp_attribute["parentId"]=layer_id;
					//创建图层子节点
					var option = {
						id:layer_id,
						parentId:layer_option.id,
						index:"3",
						label:label,
						name:name,
						isOperation:false,
						isTip:isTip,
						isShow:true,
						icon:icon,
						isSelect:isSelect,
						type:datas.type,
						layer:layer,
						geojson:datas.features[i].geojson,
						attribute:temp_attribute,
						points:points,
					};
					//创建图层
					$this.myCommon.createLayer(option);
					
				}
			}
		}).catch(() => {
			
		});
	},
	//判断图层是否为空
	is_layer_empty(){
		var flag=false;
		var layer_name = this.$store.state.layerSelectInfo.option_value;
		var temp_data = this.$store.state.layerGroups[0].children;
		for(let i=0;i<temp_data.length;i++){
			if(temp_data[i].label===layer_name){
				if(temp_data[i].children.length>0){
					flag=true;
				}else{
					flag=false;
				}
			}
		}
		return flag;
	},
	// 矢量导出
	exportClick(){
		var $this =this;
		var flag = this.is_layer_empty();
		if(!flag){
			this.$message({
			    showClose: true,
				type: 'error',
			    message: '此图层为空白图层'
			});
			return false;
		}
		$this.$confirm(<layertreeexportbox ref='layertreeexportbox'/>, '矢量导出', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					done();
				}else if(action==="cancel"){
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					var pathRegex = /[a-zA-Z]:\//;
					if(!taskRegex.test($this.$refs.layertreeexportbox.task_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '任务名称,格式不正确'
						});
						return false;
					}
					if(!pathRegex.test($this.$refs.layertreeexportbox.save_path)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '存储地址,格式不正确'
						});
						return false;
					}
					if($this.$refs.layertreeexportbox.isName){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '该路径下已存在同名文件'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			//更新下载信息
			$this.myCommon.updateDownLoadInfo($this.$refs.layertreeexportbox);
			var data = $this.$store.state.downloadInfo;
			//更新下载任务表
			$this.myCommon.updateTaskTableDatas(data);
			$this.myCommon.openTaskTable();
			// 获取features
			var temp_data = $this.$store.state.layerGroups[0].children;
			var option_value = $this.$store.state.layerSelectInfo.option_value;
			var type = $this.$store.state.layerSelectInfo.type;
			for(let i=0;i<temp_data.length;i++){
				if(temp_data[i].label===option_value){
					for(let j=0;j<temp_data[i].children.length;j++){
						var temp={};
						temp.attribute={};
						for(var key in temp_data[i].children[j].attribute){
							if(key!=="index"&&key!=="parentId"){
								temp.attribute[key] = temp_data[i].children[j].attribute[key];
							}
						}
						temp.geojson = temp_data[i].children[j].geojson;
						console.log(temp)
						data.geometrys.push(temp);
					}
				}
			}
			//调用后端函数
			exportShape(data);
			async function exportShape(data){
				await eel.export_shape(data)();
			}
			var index_down = setInterval(function(){
				for(let i=0;i<window.progress.length;i++){
					if(data.id===window.progress[i].id){
						$this.myCommon.updateProgress(data.id,window.progress[i].progress);
						$this.myCommon.updateExportProgress(data.id,window.progress[i].exportProgress);
						if(window.progress[i].progress===100&&window.progress[i].exportProgress===100){
							$this.myCommon.updateTaskIndexedDB(data);
							clearInterval(index_down);
						}
					}
				}
			},1000);
		}).catch(() => {
			
		});
	},
	rightClick(event, data, value, element){
		var $this = this;
		var map = this.myCommon.getMap();;
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		if(data.index==="1"||data.index==="3"){
			this.isShow=false;
			return false;
		}
		if(data.index==="2"){
			//清除选中
			this.myCommon.clearOperation();
			//清空表数据
			this.myCommon.clearAttributeTable();
			//清空选取图层列表
			this.myCommon.clear_operation_list();
			//更新表头
			this.myCommon.update_attribute_header();
			// 更新选取图层
			this.myCommon.update_operation_list([data]);
			//更新当前选中图层
			this.myCommon.update_select_layer(data);
			//设置全部选中(当前图层节点)
			this.myCommon.setOperation(data.label);
			//设置表数据
			this.myCommon.setAllAttributeData(data.label);
			$(".menuParent").css("left",event.clientX+"px");
			$(".menuParent").css("top",parseInt(event.clientY-141)+"px");
			this.isShow=true;
		}
		$(document).on("click",function(e){
			$this.isShow=false;
		})
	},
	attributeClick(){
		this.myCommon.openAttributeTable();
	},
	renameClick(){
		var $this=this;
		//清除选中
		this.myCommon.clearOperation();
		$this.$confirm(<renamebox ref='renamebox'/>, '重命名图层', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					done();
				}else if(action==="cancel"){
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					if(!taskRegex.test($this.$refs.renamebox.layer_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '任务名称,格式不正确'
						});
						return false;
					}
					if($this.$refs.renamebox.isName){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '已有同名图层'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			$this.myCommon.updateLayerName($this.$refs.renamebox.layer_name);
			//更新选中图层列表
			var option_value = $this.$store.state.layerSelectInfo.option_value;
			var options = $this.$store.state.layerSelectInfo.options;
			var type = $this.$store.state.layerSelectInfo.type;
			for(let i=0;i<options.length;i++){
				if(options[i].label===option_value){
					options[i].label=$this.$refs.renamebox.layer_name
					options[i].value=$this.$refs.renamebox.layer_name
					$this.myCommon.update_select_layer(options[i]);
					$this.myCommon.clear_operation_list();
					$this.myCommon.update_operation_list([options[i]]);
					break;
				}
			}
		}).catch(() => {
			
		});
		
	},
	addClick(){
		var $this=this;
		var map = this.myCommon.getMap();;
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		//清除选中
		this.myCommon.clearOperation();
		$this.$confirm(<layeraddbox ref='layeraddbox'/>, '创建图层', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					done();
				}else if(action==="cancel"){
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					if(!taskRegex.test($this.$refs.layeraddbox.layer_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '任务名称,格式不正确'
						});
						return false;
					}
					if($this.$refs.layeraddbox.isName){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '已有同名图层'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			var type = "";
			var temp_list =["id","Name","parentId"];
			if($this.$refs.layeraddbox.option_value==="点"){
				type="Point";
			}else if($this.$refs.layeraddbox.option_value==="线"){
				type="Line";
			}else if($this.$refs.layeraddbox.option_value==="面"){
				type="Region";
			}
			var table_header=[];
			for(let i=0;i<temp_list.length;i++){
				var temp={
					id:$this.$UUID(),
					alias:temp_list[i],
					name:temp_list[i],
				}
				table_header.push(temp);
			}
			//图层参数
			var option = {
				id:$this.$UUID(),
				index:"2",
				label:$this.$refs.layeraddbox.layer_name,
				isTip:false,
				isPlot:true,
				type:type,
				isShow:true,
				icon:"fa fa-eye-slash",
				table_header:table_header,
				header_keys:temp_list,
				isSelect:true,
				children:[]
			}
			//创建图层
			$this.myCommon.createLayer(option);
			var temp={
				label:$this.$refs.layeraddbox.layer_name,
				type:type
			}
			//添加至图层选中列表
			$this.myCommon.add_select_layer(temp);
			//更新header
			$this.myCommon.update_attribute_header();
			// 清除选取图层列表
			$this.myCommon.clear_operation_list();
			//更新当前选取图层列表
			$this.myCommon.update_operation_list([temp]);
			//重置输入框
			$this.$refs.layeraddbox.layer_name="";
		}).catch(() => {
			
		});
	},
	deleteClick(node,data){
		var $this=this;
		var map = this.myCommon.getMap();;
		$this.myCommon.unbindMapEvent(map);
		$this.myCommon.switchMouseStyle(false,map);
		//清除选中
		this.myCommon.clearOperation();
		if(data.index==="2"){
			//更新当前选中图层
			this.myCommon.update_select_layer(data);
			this.$confirm('图层删除后不可恢复, 是否继续?', '删除图层', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
			    type: 'warning'
			}).then(() => {
				//删除图层
				$this.myCommon.deleteLayer(data);
				var options = $this.$store.state.layerSelectInfo.options;
				if(options.length>0){
					//设置当前选中图层
					$this.myCommon.update_select_layer(options[0]);
				}else{
					$this.myCommon.clear_select_layer();
				}
			}).catch(() => {
			});
		}else if(data.index==="3"){
			var layerGroup=this.$store.state.layerGroups[0].children;
			for(let i=0;i<layerGroup.length;i++){
				if(layerGroup[i].id===data.parentId){
					//更新选中图层
					this.myCommon.update_select_layer(layerGroup[i]);
				}
			}
			this.$confirm('矢量删除后不可恢复, 是否继续?', '删除矢量', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
			    type: 'warning'
			}).then(() => {
				//删除矢量
				$this.myCommon.deleteLayer(data);
			}).catch(() => {
			});
		}
	},
	layerClick(data){
		var $this = this;
		var map = this.myCommon.getMap();;
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		if(data.index==="1"){
			return false;
		}
		//清除选中
		this.myCommon.clearOperation();
		//清空表数据
		this.myCommon.clearAttributeTable();
		//清空选取图层列表
		this.myCommon.clear_operation_list();
		//更新表头
		this.myCommon.update_attribute_header();
		
		if(data.index==="3"){
			//设置单个选中
			data.isOperation=true;
			var layerGroup=this.$store.state.layerGroups[0].children;
			for(let i=0;i<layerGroup.length;i++){
				if(layerGroup[i].id===data.parentId){
					//更新选中图层
					this.myCommon.update_select_layer(layerGroup[i]);
					// 更新选取图层
					this.myCommon.update_operation_list([layerGroup[i]]);
					for(let j=0;j<layerGroup[i].children.length;j++){
						if(layerGroup[i].children[j].id===data.id){
							
							if(!layerGroup[i].children[j].isSelect){
								layerGroup[i].children[j].isSelect=true;
								layerGroup[i].children[j].icon="fa fa-eye-slash";
								var layer =null;
								if(layerGroup[i].children[j].type==="Point"){
									layer = this.myCommon.createPoint(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="Line"){
									layer = this.myCommon.createLine(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="Region"){
									layer = this.myCommon.createPolygon(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="marker"){
									layer = this.myCommon.createMarker(layerGroup[i].children[j].points[0],layerGroup[i].children[j].name);
								}
								layerGroup[i].children[j].layer=layer;
							}
							
						}
					}
				}
			}
			if(data.type==="marker"){
				map.setView(data.layer.getLatLng(),map.getZoom());
				data.layer.openPopup();
				var myIcon = L.icon({
				    iconUrl: require('../assets/marker/marker-icon-blue.png'),
				    shadowUrl: require('../assets/marker/marker-shadow.png'),
					iconSize: [25, 41],
					iconAnchor: [12, 41],
					popupAnchor: [1, -34],
					shadowSize: [41, 41],
				});
				data.layer.setIcon(myIcon);
			}else if(data.type==="Point"){
				map.setView(data.layer.getLatLng(),map.getZoom());
				data.layer.setStyle({radius: 1,color:'blue',weight:1});
			}else if(data.type==="Line"||data.type==="Region"){
				map.setView(data.layer.getCenter(),map.getZoom());
				data.layer.setStyle({color:'blue',weight:1});
			}
			this.myCommon.setAttributeData(data.attribute);
		}else if(data.index==="2"){
			//更新当前选中图层
			$this.myCommon.update_select_layer(data);
			//设置全部选中(当前图层节点)
			$this.myCommon.setOperation(data.label);
			//设置表数据
			$this.myCommon.setAllAttributeData(data.label);
			// 更新选取图层
			$this.myCommon.update_operation_list([data]);
		}
	},
	selectClick(node,data){
		var map = this.myCommon.getMap();;
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		//清除选中
		this.myCommon.clearOperation();
		if(data.index==="2"){
			//更新当前选中图层
			this.myCommon.update_select_layer(data);
			var layerGroup=this.$store.state.layerGroups[0].children;
			for(let i=0;i<layerGroup.length;i++){
				if(layerGroup[i].id===data.id){
					if(data.isSelect){
						layerGroup[i].isSelect=false;
						layerGroup[i].icon="fa fa-eye";
						for(let j=0;j<layerGroup[i].children.length;j++){
							if(layerGroup[i].children[j].isSelect){
								layerGroup[i].children[j].isSelect=false;
								layerGroup[i].children[j].icon="fa fa-eye";
								if(layerGroup[i].children[j].layer){
									layerGroup[i].children[j].layer.remove();
								}
							}
						}
					}else{
						layerGroup[i].isSelect=true;
						layerGroup[i].icon="fa fa-eye-slash";
						for(let j=0;j<layerGroup[i].children.length;j++){
							if(j<10){
								if(!layerGroup[i].children[j].isSelect){
									layerGroup[i].children[j].isSelect=true;
									layerGroup[i].children[j].icon="fa fa-eye-slash";
									var layer =null;
									if(layerGroup[i].children[j].type==="Point"){
										layer = this.myCommon.createPoint(layerGroup[i].children[j].points);
									}else if(layerGroup[i].children[j].type==="Line"){
										layer = this.myCommon.createLine(layerGroup[i].children[j].points);
									}else if(layerGroup[i].children[j].type==="Region"){
										layer = this.myCommon.createPolygon(layerGroup[i].children[j].points);
									}else if(layerGroup[i].children[j].type==="marker"){
										layer = this.myCommon.createMarker(layerGroup[i].children[j].points[0],layerGroup[i].children[j].name);
									}
									layerGroup[i].children[j].layer=layer;
								}
							}
						}
					}
					
				}
			}
		}else if(data.index==="3"){
			var layerGroup=this.$store.state.layerGroups[0].children;
			for(let i=0;i<layerGroup.length;i++){
				if(layerGroup[i].id===data.parentId){
					//更新选中图层
					this.myCommon.update_select_layer(layerGroup[i]);
					for(let j=0;j<layerGroup[i].children.length;j++){
						if(layerGroup[i].children[j].id===data.id){
							if(layerGroup[i].children[j].isSelect){
								layerGroup[i].children[j].isSelect=false;
								layerGroup[i].children[j].icon="fa fa-eye";
								layerGroup[i].children[j].layer.remove();
							}else{
								layerGroup[i].children[j].isSelect=true;
								layerGroup[i].children[j].icon="fa fa-eye-slash";
								var layer =null;
								if(layerGroup[i].children[j].type==="Point"){
									layer = this.myCommon.createPoint(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="Line"){
									layer = this.myCommon.createLine(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="Region"){
									layer = this.myCommon.createPolygon(layerGroup[i].children[j].points);
								}else if(layerGroup[i].children[j].type==="marker"){
									layer = this.myCommon.createMarker(layerGroup[i].children[j].points[0],layerGroup[i].children[j].name);
								}
								layerGroup[i].children[j].layer=layer;
							}
							
						}
					}
				}
			}
			for(let i=0;i<layerGroup.length;i++){
				var flag = false;
				for(let j=0;j<layerGroup[i].children.length;j++){
					if(layerGroup[i].children[j].isSelect){
						flag=true;
					}
				}
				if(!flag){
					layerGroup[i].isSelect=false;
					layerGroup[i].icon="fa fa-eye";
				}else{
					layerGroup[i].isSelect=true;
					layerGroup[i].icon="fa fa-eye-slash";
				}
			}
		}
	}
  },
}
</script>

<style lang="less">
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
	color: #303133;
    padding-right: 8px;
}
.menuParent{
	position: absolute;
	left:0;
	top:0;
	width: 100px;
	z-index:3;
	border:1px solid #E4E7ED;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.menuItem{
	height: 30px;
	line-height: 30px;
	font-size: 13px;
}

.el-icon-my-point{
    background: url('../assets/vectorplot/layerpoint.png') center no-repeat;
	margin-right: 5px;
   /* background-size: cover;*/
}
// .el-icon-my-point:before{
//     content: "替";
//     font-size: 12px;
//     visibility: hidden;
// }
.el-icon-my-point{
    font-size: 12px;
}
.el-icon-my-point:before{
    content: "\e611";
}

.el-icon-my-line{
    background: url('../assets/vectorplot/layerline.png') center no-repeat;
	margin-right: 5px;
   /* background-size: cover;*/
}
.el-icon-my-line:before{
    content: "替";
    font-size: 12px;
    visibility: hidden;
}
.el-icon-my-line{
    font-size: 12px;
}
.el-icon-my-line:before{
    content: "\e611";
}

.el-icon-my-polygon{
    background: url('../assets/vectorplot/layerpolygon.png') center no-repeat;
	margin-right: 5px;
   /* background-size: cover;*/
}
.el-icon-my-polygon:before{
    content: "替";
    font-size: 12px;
    visibility: hidden;
}
.el-icon-my-polygon{
    font-size: 12px;
}
.el-icon-my-polygon:before{
    content: "\e611";
}

.layerSelectClass{
	width:100px;
	margin-right: 10px;
}
.layerSelectClass>div>.el-input__inner{
	height:20px;
	line-height: 20px;
}
.layerSelectClass>.el-input--mini .el-input__icon{
	line-height: 20px;
	font-size: 12px;
}
</style>
