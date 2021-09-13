<template>
	<div>
		<el-tree :data="treeDatas" default-expand-all :expand-on-click-node="false" @node-contextmenu="rightClick">
			<span class="custom-tree-node" slot-scope="{node,data}"  @click.stop="layerClick(data)">
				<el-tooltip :content="data.name" placement="right-end" effect="light" v-if="data.isTip">
					<span>
						<i class="el-icon-my-point" v-if="data.type==='marker'"></i>
						<i class="el-icon-my-point" v-else-if="data.type==='point'"></i>
						<i class="el-icon-my-line" v-else-if="data.type==='line'"></i>
						<i class="el-icon-my-polygon" v-else-if="data.type==='region'"></i>
						<span>{{node.label}}</span>
					</span>
				</el-tooltip>
				<span v-else>
					<i class="el-icon-my-point" v-if="data.type==='marker'"></i>
					<i class="el-icon-my-point" v-else-if="data.type==='point'"></i>
					<i class="el-icon-my-line" v-else-if="data.type==='line'"></i>
					<i class="el-icon-my-polygon" v-else-if="data.type==='region'"></i>
					<span>{{node.label}}</span>
				</span>
				<span v-if="data.index==='1'">
					<i class="el-icon-my-point" v-if="get_type==='marker'"></i>
					<i class="el-icon-my-point" v-else-if="get_type==='point'"></i>
					<i class="el-icon-my-line" v-else-if="get_type==='line'"></i>
					<i class="el-icon-my-polygon" v-else-if="get_type==='region'"></i>
					<el-select :value="get_value" size="mini" class="layerSelectClass" @change="layerSelectChange">
						<el-option v-for="post in get_options" :labek="post.label" :value="post.value" >
							<i class="el-icon-my-point" v-if="post.type==='marker'"></i>
							<i class="el-icon-my-point" v-else-if="post.type==='point'"></i>
							<i class="el-icon-my-line" v-else-if="post.type==='line'"></i>
							<i class="el-icon-my-polygon" v-else-if="post.type==='region'"></i>
							<span>{{post.label}}</span>
						</el-option>
					</el-select>
					<el-button size="mini" type="text" icon="el-icon-folder-add"  @click.stop="importClick(data)"></el-button>
					<el-button size="mini" type="text" icon="el-icon-plus" @click.stop="addClick(data)"></el-button>
				</span>
				<span v-else>
					<el-button size="mini" type="text">{{data.count}}</el-button>
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
  	  },
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
					$this.$refs.layertreeimportbox.init_panel();
					done();
				}else if(action==="cancel"){
					$this.$refs.layertreeimportbox.init_panel();
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					var importRegex = /(\.shp)|(\.csv)|(\.kml)/;
					var indexRegex = /[0-9]+/;
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
					if(!$this.$refs.layertreeimportbox.is_exists){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '文件不存在或坐标系不支持'
						});
						return false;
					}
					if($this.$refs.layertreeimportbox.import_format==="csv"&&$this.$refs.layertreeimportbox.radio === "点"){
						if(!indexRegex.test($this.$refs.layertreeimportbox.lng)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '经度不能为空'
							});
							return false;
						}
						if(!indexRegex.test($this.$refs.layertreeimportbox.lat)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '纬度不能为空'
							});
							return false;
						}
					}else if($this.$refs.layertreeimportbox.import_format==="csv"&&$this.$refs.layertreeimportbox.radio !== "点"){
						if(!indexRegex.test($this.$refs.layertreeimportbox.geometry)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '空间对象不能为空'
							});
							return false;
						}
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
			var coordinate="";
			for(let i=0;i<$this.$refs.layertreeimportbox.options.length;i++){
				if($this.$refs.layertreeimportbox.option_value===$this.$refs.layertreeimportbox.options[i].value){
					coordinate = $this.$refs.layertreeimportbox.options[i].label;
				}
			}
			var temp_info={
				file_path:$this.$refs.layertreeimportbox.import_file_path,
				import_format:$this.$refs.layertreeimportbox.import_format,
				coordinate:coordinate,
			}
			if($this.$refs.layertreeimportbox.import_format==="csv"&&$this.$refs.layertreeimportbox.feature_type==="point"){
				temp_info.x = $this.$refs.layertreeimportbox.lng-1;
				temp_info.y = $this.$refs.layertreeimportbox.lat-1;
				temp_info.feature_type=$this.$refs.layertreeimportbox.feature_type;
			}else if($this.$refs.layertreeimportbox.import_format==="csv"&&$this.$refs.layertreeimportbox.feature_type==="line"){
				temp_info.geometry = $this.$refs.layertreeimportbox.geometry-1;
				temp_info.feature_type=$this.$refs.layertreeimportbox.feature_type;
			}else if($this.$refs.layertreeimportbox.import_format==="csv"&&$this.$refs.layertreeimportbox.feature_type==="region"){
				temp_info.geometry = $this.$refs.layertreeimportbox.geometry-1;
				temp_info.feature_type=$this.$refs.layertreeimportbox.feature_type;
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
					$this.$refs.layertreeimportbox.init_panel();
					//关闭loading
					$this.$store.state.loading=false;
					return false;
				}else{
					var attribute = result.data[0].attributes;
					var temp_keys = Object.keys(attribute);
					var table_header = [];
					for(let i=0;i<temp_keys.length;i++){
						var temp={
							id:$this.$UUID(),
							alias:temp_keys[i],
							name:temp_keys[i],
						};
						table_header.push(temp);
					}
					var temp_coordinate = "";
					for(let i=0;i<$this.$refs.layertreeimportbox.options.length;i++){
						if(result.coordinate===$this.$refs.layertreeimportbox.options[i].value){
							temp_coordinate = $this.$refs.layertreeimportbox.options[i].label;
						}
					}
					console.log(temp_coordinate);
					//创建图层父节点 类似数据集结构
					var layer_option = {
						id:$this.$UUID(),
						index:"2",
						count:0,
						label:$this.$refs.layertreeimportbox.layer_name,
						isTip:false,
						isPlot:true,
						isShow:true,
						type:result.type,
						table_header:table_header,
						header_keys:temp_keys,
						icon:"fa fa-eye-slash",
						coordinate:temp_coordinate,
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
					var operation_list={
						label:$this.$refs.layertreeimportbox.layer_name,
						type:result.type
					}
					//更新当前选取图层列表
					$this.myCommon.update_operation_list([operation_list]);
					
					//创建图层子节点
					for(let i=0;i<result.data.length;i++){
						var name="";
						if(result.data[i].attributes.Name||result.data[i].attributes.name){
							name=result.data[i].attributes.Name||result.data[i].attributes.name;
						}else if(result.type==="point"){
							name="点";
						}else if(result.type==="line"){
							name="线";
						}else if(result.type==="region"){
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
						var layer="";
						if(result.type==="point"){
							if(i<=9){
								//创建地图点图层
								layer = L.circleMarker(result.data[i].features[0], {radius: 5,color:'red',weight:1}).addTo(map);
							}else{
								layer=null;
							}
							
						}else if(result.type==="line"){
							if(i<=9){
								layer = L.polyline(result.data[i].features, {color: "red",weight:1}).addTo(map);
							}else{
								layer=null;
							}
							
						}else if(result.type==="region"){
							if(i<=9){
								layer = L.polygon(result.data[i].features,{color:'red',weight:1}).addTo(map);
							}else{
								layer=null;
							}
							
						}
						var layer_id = $this.$UUID();
						var temp_attribute = result.data[i].attributes;
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
							type:result.type,
							layer:layer,
							features:result.data[i].features,
							attribute:temp_attribute,
						};
						//创建图层
						$this.myCommon.createLayer(option);
						
					}
					$this.$refs.layertreeimportbox.init_panel();
					//关闭loading
					$this.$store.state.loading=false;
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
					$this.$refs.layertreeexportbox.init_export();
					done();
				}else if(action==="cancel"){
					$this.$refs.layertreeexportbox.init_export();
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
					if($this.$refs.layertreeexportbox.option_value2 === ""){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '目标坐标系不能为空'
						});
						return false;
					}
					if($this.$refs.layertreeexportbox.on_need){
						var flag = false;
						for(var key in $this.$refs.layertreeexportbox.seven){
							if($this.$refs.layertreeexportbox.seven[key] != ""){
								flag = true;
								break;
							}
						}
						if(!flag){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '不同基准坐标系转换,需要设置七参数'
							});
							return false;
						}
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
			var target_coordinate="";
			for(let i=0;i<$this.$refs.layertreeexportbox.options2.length;i++){
				if($this.$refs.layertreeexportbox.option_value2===$this.$refs.layertreeexportbox.options2[i].label){
					target_coordinate = $this.$refs.layertreeexportbox.options2[i].label;
				}
			}
			var features = [];
			var attributes = [];
			for(let i=0;i<$this.$store.state.layerGroups[0].children.length;i++){
				if($this.$store.state.layerSelectInfo.option_value === $this.$store.state.layerGroups[0].children[i].label){
					for(let j=0;j<$this.$store.state.layerGroups[0].children[i].children.length;j++){
						features.push($this.$store.state.layerGroups[0].children[i].children[j].features);
						attributes.push($this.$store.state.layerGroups[0].children[i].children[j].attribute);
					}
				}
			}
			// 源坐标系
			var source_coordinate = $this.$store.state.layerSelectInfo.coordinate;
			var temp_info={
				id:$this.$UUID(),
				downType:"导出矢量",
				taskName:$this.$refs.layertreeexportbox.task_name,
				savePath:$this.$refs.layertreeexportbox.save_path,
				saveType:$this.$refs.layertreeexportbox.option_value,
				type:$this.$store.state.layerSelectInfo.type,
				source:source_coordinate,
				target:target_coordinate,
				seven:$this.$refs.layertreeexportbox.seven,
				time:$this.getDate(),
				features:features,
				attributes:attributes,
			}
			console.log(temp_info)
			//更新下载任务表
			$this.myCommon.updateTaskTableDatas(temp_info);
			$this.myCommon.openTaskTable();
			//导出数据
			export_features(temp_info);
			async function export_features(temp_info){
				await eel.export_features(temp_info)();
			}
			$this.$refs.layertreeexportbox.init_export();
		}).catch(() => {
			$this.$refs.layertreeexportbox.init_export();
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
			var temp_list =["name","parentId","mydescribe"];
			if($this.$refs.layeraddbox.option_value==="点"){
				type="point";
			}else if($this.$refs.layeraddbox.option_value==="线"){
				type="line";
			}else if($this.$refs.layeraddbox.option_value==="面"){
				type="region";
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
				count:0,
				label:$this.$refs.layeraddbox.layer_name,
				isTip:false,
				isPlot:true,
				type:type,
				isShow:true,
				icon:"fa fa-eye-slash",
				table_header:table_header,
				header_keys:temp_list,
				coordinate:"4326",
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
								if(layerGroup[i].children[j].type==="point"){
									layer = L.circleMarker(layerGroup[i].children[j].features[0], {radius: 5,color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="line"){
									layer = L.polyline(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="region"){
									layer = L.polygon(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="marker"){
									layer = this.myCommon.createMarker(layerGroup[i].children[j].features[0],layerGroup[i].children[j].name);
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
			}else if(data.type==="point"){
				map.setView(data.layer.getLatLng(),map.getZoom());
				data.layer.setStyle({radius: 5,color:'blue',weight:1});
			}else if(data.type==="line"||data.type==="region"){
				map.setView(data.layer.getCenter(),map.getZoom());
				data.layer.setStyle({color:'blue',weight:1});
			}
			this.myCommon.setAttributeData(data.attribute);
			//更新表头
			this.myCommon.update_attribute_header();
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
		var map = this.myCommon.getMap();
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
									if(layerGroup[i].children[j].type==="point"){
										layer = L.circleMarker(layerGroup[i].children[j].features[0], {radius:5,color:'red',weight:1}).addTo(map);
									}else if(layerGroup[i].children[j].type==="line"){
										layer = L.polyline(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
									}else if(layerGroup[i].children[j].type==="region"){
										layer = L.polygon(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
									}else if(layerGroup[i].children[j].type==="marker"){
										layer = this.myCommon.createMarker(layerGroup[i].children[j].features[0],layerGroup[i].children[j].name);
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
								if(layerGroup[i].children[j].type==="point"){
									layer = L.circleMarker(layerGroup[i].children[j].features[0], {radius: 5,color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="line"){
									layer = L.polyline(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="region"){
									layer = L.polygon(layerGroup[i].children[j].features,{color:'red',weight:1}).addTo(map);
								}else if(layerGroup[i].children[j].type==="marker"){
									layer = this.myCommon.createMarker(layerGroup[i].children[j].features[0],layerGroup[i].children[j].name);
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
	flex-direction: row;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
	color: #303133;
    padding-right: 8px;
}
.custom-tree-node>span:nth-child(1){
	flex:1;
	width:0;
	overflow: hidden;
	text-overflow: ellipsis;
}
.custom-tree-node>span:nth-child(1)>span{
	// width:100%;
	// max-width: 150px;
	// overflow: hidden;
	// text-overflow: ellipsis;
	// display: block;
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
}

.el-icon-my-point{
    font-size: 12px;
}
.el-icon-my-point:before{
    content: "\e611";
}

.el-icon-my-line{
    background: url('../assets/vectorplot/layerline.png') center no-repeat;
	margin-right: 5px;
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
