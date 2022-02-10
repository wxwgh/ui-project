<template>
	<div class="tableParent">
		<el-table :cell-class-name="tableCellClassName" :row-style="table_row" @cell-click="tableClick" :data="get_data" border size="mini" :height="tableHeight">
			<template v-for="p in get_header">
				<el-table-column min-width="150" :key="p.id" show-overflow-tooltip :prop="p.name" :label="p.alias" v-if="p.name!=='parentId'">
					<template slot-scope="scope">
						<span v-if="scope.row.index === rowIndex && scope.column.index === columnIndex">
							<el-input v-model="scope.row[p.name]" size="mini" @blur="update_attribute(scope)"></el-input>
						</span>
						<span v-else>{{scope.row[p.name]}}</span>
					</template>
				</el-table-column>
			</template>
		</el-table>
		<div class="attributeButtonParent">
			<span class="attributeSelectClass">
				<i class="el-icon-my-point" v-if="get_type==='marker'"></i>
				<i class="el-icon-my-point" v-else-if="get_type==='point'"></i>
				<i class="el-icon-my-line" v-else-if="get_type==='line'"></i>
				<i class="el-icon-my-polygon" v-else-if="get_type==='region'"></i>
				<el-select :value="get_value" size="mini" @change="attributeSelectChange">
					<el-option v-for="post in get_options" :label="post.label" :value="post.value">
						<i class="el-icon-my-point" v-if="post.type==='marker'"></i>
						<i class="el-icon-my-point" v-else-if="post.type==='point'"></i>
						<i class="el-icon-my-line" v-else-if="post.type==='line'"></i>
						<i class="el-icon-my-polygon" v-else-if="post.type==='region'"></i>
						<span>{{post.label}}</span>
					</el-option>
				</el-select>
			</span>
			<div class="attributeButtonClass">
				<el-button icon="el-icon-plus" circle size="mini" @click="tableAdd()"></el-button>
				<el-button icon="el-icon-delete" circle size="mini" @click="tableDelete()"></el-button>
			</div>
		</div>
	</div>
</template>

<script>
import attributetableaddbox from '@/components/attributetableaddbox.vue';
import attributetabledeletebox from '@/components/attributetabledeletebox.vue';
export default {
  name: 'attributetable',
  components:{
  	attributetableaddbox,
  	attributetabledeletebox,
  },
  data(){
    return {
		rowIndex:"",
		columnIndex:"",
		tableHeight:"100%",
		table_key:1,
	}
  },
  computed:{
	  get_header:function(){
		  return this.$store.state.attributeHeader;
	  },
	  get_data:function(){
		  return this.$store.state.attributeTable;
	  },
	  get_value:function(){
		  return this.$store.state.layerOperationInfo.option_value;
	  },
	  get_options:function(){
		  return this.$store.state.layerOperationInfo.options;
	  },
	  get_type:function(){
		  return this.$store.state.layerOperationInfo.type;
	  },
  },
  mounted:function(){
	var height = parseInt(window.innerHeight)-181;
	$(".tableParent").css("height",height);
  },
  methods:{
	// 行样式回调
	table_row({row, rowIndwx}){
		var style={
			"height":"35px",
			"line-height":"35px"
		};
		return style;
	},
	//更新属性
	update_attribute(data){
		console.log(data);
		//input失去焦点进行属性更新
		//获取当前选中图层
		var layer_name = this.$store.state.layerOperationInfo.option_value;
		var layer_group = this.$store.state.layerGroups[0].children;
		// 获取keys
		var temp_keys = Object.keys(data.row);
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				for(let j=0;j<layer_group[i].children.length;j++){
					if(layer_group[i].children[j].id===data.row.parentId){
						for(let x=0;x<temp_keys.length;x++){
							layer_group[i].children[j].attribute[temp_keys[x]]=data.row[temp_keys[x]];
						}
					}
				}
			}
		}
		this.rowIndex="";
		this.columnIndex="";
	},
	attributeSelectChange(name){
		var $this = this;
		var layerGroup = $this.$store.state.layerGroups[0].children;
		for(let i=0;i<layerGroup.length;i++){
			if(layerGroup[i].label===name){
				//清空表格数据
				$this.myCommon.clearAttributeTable();
				//设置选取图层列表当前选中
				$this.$store.state.layerOperationInfo.option_value=name;
				$this.$store.state.layerOperationInfo.type=layerGroup[i].type;
				// 是否更新过表头
				var flag = false;
				//更新表格数据
				for(let j=0;j<layerGroup[i].children.length;j++){
					if(name === layerGroup[i].label){
						if(layerGroup[i].children[j].isOperation){
							//更新表格数据
							$this.myCommon.setAttributeData(layerGroup[i].children[j].attribute);
							// 更新表头
							if(!flag){
								$this.$store.state.attributeHeader.splice(0,$this.$store.state.attributeHeader.length);
								for(let x=0;x<layerGroup[i].table_header.length;x++){
									$this.$store.state.attributeHeader.push(layerGroup[i].table_header[x]);
								}
								flag=true;
							}
						}
					}
					
				}

			}
		}
	},
	labelHead(h,{column,index}){
		return h('span',{class:'table-head',style:{width:'100%'}},[column.label]);
	},
	tableCellClassName({row, column, rowIndex, columnIndex}){
	    //利用单元格的 className 的回调方法，给行列索引赋值
	    row.index=rowIndex;
	    column.index=columnIndex;
	},
	tableClick(row, column, cell, event){
		this.rowIndex=row.index;
		this.columnIndex=column.index;
	},
	tableAdd(){
		var $this = this;
		$this.$confirm(<attributetableaddbox ref='attributetableaddbox'/>, '添加字段', {
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
					if(!taskRegex.test($this.$refs.attributetableaddbox.field_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '字段名称,格式不正确'
						});
						return false;
					}
					if($this.$refs.attributetableaddbox.isName){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '已有同名字段'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			//添加字段和属性
			$this.add_header_attribute($this.$refs.attributetableaddbox.field_name);
			$this.$refs.attributetableaddbox.field_name="";
		}).catch(() => {
			
		});
	},
	//添加字段和属性
	add_header_attribute(name){
		var $this = this;
		//获取当前选中图层
		var layer_name = this.$store.state.layerOperationInfo.option_value;
		var layer_group = this.$store.state.layerGroups[0].children;
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				var temp={
					id:this.$UUID(),
					alias:name,
					name:name,
				}
				layer_group[i].table_header.push(temp);
				layer_group[i].header_keys.push(name);
				for(let j=0;j<layer_group[i].children.length;j++){
					layer_group[i].children[j].attribute[name]="";
				}
			}
		}
		var flag = false;
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				//清空表格数据
				this.myCommon.clearAttributeTable();
				//更新表格数据
				for(let j=0;j<layer_group[i].children.length;j++){
					if(layer_group[i].children[j].isOperation){
						//更新表格数据
						$this.myCommon.setAttributeData(layer_group[i].children[j].attribute);
						// 更新表头
						if(!flag){
							$this.$store.state.attributeHeader.splice(0,$this.$store.state.attributeHeader.length);
							for(let x=0;x<layer_group[i].table_header.length;x++){
								$this.$store.state.attributeHeader.push(layer_group[i].table_header[x]);
							}
							flag=true;
						}
					}
				}
			}
		}
	},
	//删除字段和属性
	delete_header_attribute(name){
		var $this =this;
		//获取当前选中图层
		var layer_name = this.$store.state.layerOperationInfo.option_value;
		var layer_group = this.$store.state.layerGroups[0].children;
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				for(let j=0;j<layer_group[i].table_header.length;j++){
					if(layer_group[i].table_header[j].name===name){
						layer_group[i].table_header.splice(j,1);
						layer_group[i].header_keys.splice(j,1);
					}
				}
				for(let j=0;j<layer_group[i].children.length;j++){
					delete layer_group[i].children[j].attribute[name];
				}
			}
		}
		//更新表格
		var flag = false;
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				//清空表格数据
				this.myCommon.clearAttributeTable();
				//更新表格数据
				for(let j=0;j<layer_group[i].children.length;j++){
					if(layer_group[i].children[j].isOperation){
						//更新表格数据
						$this.myCommon.setAttributeData(layer_group[i].children[j].attribute);
						// 更新表头
						if(!flag){
							$this.$store.state.attributeHeader.splice(0,$this.$store.state.attributeHeader.length);
							for(let x=0;x<layer_group[i].table_header.length;x++){
								$this.$store.state.attributeHeader.push(layer_group[i].table_header[x]);
							}
							flag=true;
						}
					}
				}
			}
		}
	},
	tableDelete(){
		var $this = this;
		//根据当前选取图层获取字段列表
		var layer_name = this.$store.state.layerOperationInfo.option_value;
		var layer_group = this.$store.state.layerGroups[0].children;
		//清空删除列表
		this.$store.state.layer_delete_options.splice(0,this.$store.state.layer_delete_options.length);
		for(let i=0;i<layer_group.length;i++){
			if(layer_group[i].label===layer_name){
				var temp_keys = layer_group[i].header_keys;
				for(let j=0;j<temp_keys.length;j++){
					if(temp_keys[j]!=="parentId"){
						var temp={
							id:this.$UUID(),
							label:temp_keys[j],
							value:temp_keys[j],
						}
						this.$store.state.layer_delete_options.push(temp);
					}
				}
			}
		}
		$this.$confirm(<attributetabledeletebox ref='attributetabledeletebox'/>, '删除字段', {
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			closeOnClickModal:false,
			beforeClose:function(action, instance, done){
				if(action==="close"){
					$this.$refs.attributetabledeletebox.field_name="";
					done();
				}else if(action==="cancel"){
					$this.$refs.attributetabledeletebox.field_name="";
					done();
				}else if(action==="confirm"){
					var taskRegex = /([0-9]|[a-z]|[\u4e00-\u9fa5])+/;
					if(!taskRegex.test($this.$refs.attributetabledeletebox.field_name)){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '字段名称,格式不正确'
						});
						return false;
					}else{
						done();
					}
				}
			}
		}).then(() => {
			$this.delete_header_attribute($this.$refs.attributetabledeletebox.field_name);
			$this.$refs.attributetabledeletebox.field_name="";
		}).catch(() => {
			$this.$refs.attributetabledeletebox.field_name="";
		});
	},
  },
}
</script>

<style lang="less">
.tableParent{
	width: 100%;
	height:100%;
	display: flex;
	flex-direction: column;
	justify-content:flex-start;
}
.attributeButtonParent{
	display: flex;
	flex-direction: row;
	justify-content:space-between;
	line-height: 39.67px;
	height: 39.67px;
}
.attributeRadioClass{
	margin-left: 10px;
}
.attributeButtonClass{
	margin-right: 10px;
}
.attributeSelectClass{
	margin-left: 5px;
}
.el-tooltip__popper.is-dark{
	background:#fff;
	color:#2c3e50;
	border: 1px solid #303133;
}
</style>
