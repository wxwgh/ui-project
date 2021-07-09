<template>
  <div id="app" v-loading.fullscreen.lock="get_loading" element-loading-text="请稍等" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.5)">
	<el-row type="flex" >
	  <el-col :span="24">
		  <el-tabs v-model="activeName" type="card" :before-leave="tabBeforeClick">
		      <el-tab-pane label="地图下载" name="first">
		  		<div class="tabContent">
		  			<!-- 在线地图 -->
		  			<onlinemap></onlinemap>
		  			<!-- 范围设置 -->
		  			<scopeset></scopeset>
					<!-- 分幅设置 -->
					<showset></showset>
		  			<!-- 下载相关 -->
		  			<mapdownload></mapdownload>
		  		</div>
		  	</el-tab-pane>
		      <el-tab-pane label="矢量标绘" name="second">
		  		<div class="tabContent">
		  			<!-- 标绘 -->
		  			<plot></plot>
		  			<!-- 对象操作 -->
		  			<plotoperation></plotoperation>
		  			<!-- poi搜索 -->
		  			<search></search>
		  		</div>
		  	</el-tab-pane>
		      <el-tab-pane label="实用工具" name="third">
		  		<div class="tabContent">
		  			<!-- 量测 -->
		  			<measure />
		  			<!-- 地形分析 -->
		  			<analyze />
		  			<!-- 坐标转换 -->
		  			<coordinate></coordinate>
		  		</div>
		  	</el-tab-pane>
		      <el-tab-pane label="许可中心" name="fourth">
		  		<div class="tabContent">
		  			<userpermission></userpermission>
		  			<userinfo></userinfo>
		  		</div>
		  	</el-tab-pane>
		  </el-tabs>
	  </el-col>
	</el-row>
	<el-row type="flex" style="flex-grow: 1;">
		<el-col :span="4" style="min-width: 250px">
			<!-- 侧边栏控制台 -->
			<myaside></myaside>
		</el-col>
		<el-col :span="20" >
			<!-- 地图窗口 表格面板 -->
			<el-tabs v-model="tabActionName" type="card" :before-leave="tabBeforeClick" >
				<el-tab-pane label="二维视图" name="1">
					<router-view v-if="is_router_show"></router-view>
					<zoomslider></zoomslider>
				</el-tab-pane>
				<el-tab-pane label="三维视图" name="2" >
					<mapcesium></mapcesium>
				</el-tab-pane>
				<el-tab-pane label="下载任务" name="3" >
					<downloadattribute></downloadattribute>
				</el-tab-pane>
				<el-tab-pane label="属性表" name="4" >
					<attributetable></attributetable>
				</el-tab-pane>
			</el-tabs>
			
		</el-col>
	</el-row>
  </div>
</template>
<script>
  import measure from '@/components/measure.vue';
  import coordinate from '@/components/coordinate.vue';
  import analyze from '@/components/analyze.vue';
  import scopeset from '@/components/scopeset.vue';
  import search from '@/components/search.vue';
  import plot from '@/components/plot.vue';
  import plotoperation from '@/components/plotoperation.vue';
  import attributetable from '@/components/attributetable.vue';
  import onlinemap from '@/components/onlinemap.vue';
  import myaside from '@/components/aside.vue';
  import mapdownload from '@/components/mapdownload.vue';
  import userpermission from '@/components/userpermission.vue';
  import showset from '@/components/showset.vue';
  import downloadattribute from '@/components/downloadattribute.vue';
  import mapcesium from '@/components/mapcesium.vue';
  import userinfo from '@/components/userinfo.vue';
  import zoomslider from '@/components/zoomslider.vue';
  export default {
	components:{
	    measure,
		coordinate,
		analyze,
		scopeset,
		search,
		plot,
		plotoperation,
		attributetable,
		onlinemap,
		myaside,
		mapdownload,
		userpermission,
		showset,
		downloadattribute,
		mapcesium,
		userinfo,
		zoomslider,
	},
    data() {
      return {
		//顶部选项卡标识
        activeName: 'first',
		//地图窗口选项卡 标识
		tabActionName:this.$store.state.tabActionName,
		is_router_show:true,
      };
    },
	provide(){
		return {
			reload:this.reload
		}
	},
	mounted:function(){
		//初始化indexedDB
		this.initIndexedDB();
		//初始化用户
		this.initUser();
		//初始化下载任务 表格数据
		this.initDownLoadTableDatas();
		//初始化地图名和下载地址
		this.myCommon.updateNameAndUrl();
		//初始化快速导航树
		this.initNavigationTree();
		//进度条更新方法 挂载到windows对象上
		this.initProgress();
		// 初始化自定义图层列表
		this.init_map_list();
		//页面刷新返回首页
		// this.return_home();
	},
	// 页面创建时
	created:function(){
		$("body").css("height",window.innerHeight);
	},
	computed:{
		  get_loading:function(){
			  return this.$store.state.loading;
		  }
	},
    methods: {
		reload(){
			this.is_router_show = false;
			this.$nextTick(() => {
			    this.is_router_show = true;
				//清空范围
				this.myCommon.clearScope();
				//清空测量结果
				this.myCommon.clear_measure();
		    })
		},
		initProgress(){
			var $this = this;
			window["updateProgress"] =function(id,progress){
				$this.myCommon.updateProgress(id,progress);
			}
			window["updateExportProgress"] =function(id,exportProgress){
				$this.myCommon.updateExportProgress(id,exportProgress);
			}
			window["updateTaskIndexedDB"] =function(data){
				$this.myCommon.updateTaskIndexedDB(data);
			}
		},
		initNavigationTree(){
			var $this =this;
			var key = this.$store.state.gaodeKey;
			var url = "https://restapi.amap.com/v3/config/district?subdistrict=3&showbiz=false&extensions=base&key="+key+"&s=rsv3&output=json&keywords=中国&callback=jsonp_300354_&platform=JS&logversion=2.0&appname=https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4&csid=7C3B60ED-0C39-46A6-891E-A0D28DA8864B&sdkversion=1.4.15";
			this.axios({
				method: 'get',
				url: url
			}).then(function(result){
				var temp = JSON.parse(result.data.substring(result.data.indexOf("(")+1,result.data.length-1));
				var temp_data = temp.districts;
				$this.$store.state.navigation_tree=temp_data;
			})
		},
		tabBeforeClick(activeName, oldActiveName){
			if(activeName==="3"||activeName==="4"||activeName==="second"||activeName==="third"){
				var data = this.myCommon.isLoginAndTime();
				if(!data.flag){
					this.$message(data.options);
					return data.flag
				}
			}
			this.$store.state.tabActionName = activeName;
			if(this.$store.state.is_init_map&&activeName==="1"){
				this.reload();
			}
		},
		//数据库及表初始化函数
		initIndexedDB(){
			let id = this.$store.state.downLoadTableId;
			let user_id = this.$store.state.user_table_id;
			let custom_id = this.$store.state.custom_map_list_id;
			// indexedDB.deleteDatabase("download");
			var request = indexedDB.open("download",1);
			//成功回调函数
			request.onsuccess = function(e) {
				//数据库表初始化成功
				// console.log("数据库及表初始化成功");
			};
			//数据库版本升级事件函数
			request.onupgradeneeded =function(e){
				var db = e.target.result;
				//创建对象仓库 即 表
				if(!db.objectStoreNames.contains(id)){
					//新增一张表 主键是id
					db.createObjectStore(id,{autoIncrement:true});
				}
				//创建用户表
				if(!db.objectStoreNames.contains(user_id)){
					//新增一张表 主键是id
					db.createObjectStore(user_id,{autoIncrement:true});
				}
				//创建自定义服务表
				if(!db.objectStoreNames.contains(custom_id)){
					//新增一张表 主键是id
					db.createObjectStore(custom_id,{autoIncrement:true});
				}
			};
		},
		//初始化用户
		initUser(){
			var $this = this;
			var id = this.$store.state.user_table_id;
			//打开一个数据库 并指定名称
			var request = indexedDB.open("download",1);
			//成功回调函数
			request.onsuccess = function(e) {
				var db = e.target.result;
				//创建一个事务对象 指定表名 和操作模式
				var trans = db.transaction(id,"readwrite");
				//获取表格对象
				var objStore = trans.objectStore(id);
				//判断表格是否为空
				var countRequest = objStore.count();
				countRequest.onsuccess = function() {
				  if(countRequest.result===0){
				  	//添加管理员和限时用户信息
				  	var userInfo={
						id:$this.$UUID(),
				  		name:"限时用户",
				  		describe:"无需登录,更新许可即可使用本应用",
				  		time:"2022/6/10",
				  		isAdmin:false
				  	};
				  	var administratorInfo={
						id:$this.$UUID(),
						user_id:userInfo.id,
				  		name:"管理员",
				  		password:"supermap@123",
				  		describe:"生成许可",
				  		time:"2121/3/17",
						limitTime:"",
						error_count:0,
				  		isAdmin:true
				  	};
				  	objStore.add(userInfo);
				  	objStore.add(administratorInfo);
					$this.$store.state.administratorInfo.id=administratorInfo.id;
					$this.$store.state.administratorInfo.user_id=administratorInfo.user_id;
				  }else{
				  	//获取游标对象
				  	var cursor = objStore.openCursor();
				  	cursor.onsuccess=function(e){
				  		var result = e.target.result;
				  		//查询数据
				  		if(result){
				  			if(result.value.name==="管理员"){
				  				$this.$store.state.administratorInfo.password=result.value.password;
				  				$this.$store.state.administratorInfo.id=result.value.id;
				  				$this.$store.state.administratorInfo.limitTime=result.value.limitTime;
				  				$this.$store.state.administratorInfo.error_count=result.value.error_count;
				  			}else if(result.value.name==="限时用户"){
				  				$this.$store.state.administratorInfo.name=result.value.name;
								$this.$store.state.administratorInfo.user_id = result.value.id;
				  				$this.$store.state.administratorInfo.describe=result.value.describe;
				  				$this.$store.state.administratorInfo.time=result.value.time;
				  				$this.$store.state.administratorInfo.isAdmin=result.value.isAdmin;
				  			}
							result.continue();
				  		}
				  	}
				  }
				}
				db.close();
			};
		},
		//初始化下载任务 表格数据
		initDownLoadTableDatas(){
			var $this = this;
			var id = this.$store.state.downLoadTableId;
			//打开一个数据库 并指定名称
			var request = indexedDB.open("download",1);
			//成功回调函数
			request.onsuccess = function(e) {
				var db = e.target.result;
				//创建一个事务对象 指定表名 和操作模式
				var trans = db.transaction(id,"readwrite");
				//获取表格对象
				var objStore = trans.objectStore(id);
				//获取游标对象
				var cursor = objStore.openCursor();
				cursor.onsuccess=function(e){
					var result = e.target.result;
					//查询数据
					if(result){
						var tempData={
							id:result.value.id,
							taskName:result.value.taskName,
							mapName:result.value.mapName,
							downType:result.value.downType,
							time:result.value.time,
							savePath:result.value.savePath,
							progress:result.value.progress,
							exportProgress:result.value.exportProgress,
						};
						$this.$store.state.taskTableDatas.push(tempData);
						//将游标按它的方向移动到下一个位置，到其健与可选健参数匹配的项
						result.continue();
					}
				}
				db.close();
			};
			
		},
		init_map_list(){
			var $this = this;
			var id = this.$store.state.custom_map_list_id;
			//打开一个数据库 并指定名称
			var request = indexedDB.open("download",1);
			//成功回调函数
			request.onsuccess = function(e) {
				var db = e.target.result;
				//创建一个事务对象 指定表名 和操作模式
				var trans = db.transaction(id,"readwrite");
				//获取表格对象
				var objStore = trans.objectStore(id);
				//获取游标对象
				var cursor = objStore.openCursor();
				cursor.onsuccess=function(e){
					var result = e.target.result;
					//查询数据
					if(result){
						var temp = {
							id:result.value.id,
							label:result.value.label,
							index:result.value.index,
							type:result.value.type,
							center:result.value.center,
							dpi:result.value.dpi,
							scale:result.value.scale,
							isActive:result.value.isActive,
							isShow:result.value.isShow,
							minZoom: result.value.minZoom,
							maxZoom: result.value.maxZoom,
							image:result.value.image,
							url:result.value.url,
							realUrl:result.value.realUrl,
							imageProvider:result.value.imageProvider,
						};
						$this.$store.state.custom_map_list[0].children.push(temp);
						$this.$store.state.custom_map_list[0].count = $this.$store.state.custom_map_list[0].children.length;
						// if(temp.type === "wmts"){
						// 	//添加至provider对象
						// 	L.TileLayer.ChinaProvider.providers.CusTom.Normal[temp.label] = temp.realUrl.split(":")[1];
						// 	L.TileLayer.ChinaProvider.providers.CusTom["Subdomains"]=[];
						// }
						//将游标按它的方向移动到下一个位置，到其健与可选健参数匹配的项
						result.continue();
					}
				}
				db.close();
			};
		},
		initWebSocket(){
			var $this = this;
			//打开一个web socket
			var ws = new WebSocket("ws://127.0.0.1:5001");
			//连接建立后的回调
			ws.onopen=function(){
				console.log("连接已建立");
				ws.send("你好");
			}
			ws.onmessage = function(e){
				var data = e.data;
				console.log(data);
			}
		    ws.onclose = function(){ 
			  // 关闭 websocket
			  alert("连接已关闭..."); 
		    };
		},
    }
  };
</script>
<style lang="less">
/* 初始化环境 */
html,body{
  height:100%;
  width:100%;
  overflow:hidden;
  -webkit-user-select:none;
  font-size: 16px;
  color: #2c3e50;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}
body{margin:0;padding:0;background:#fff;}
body img{border:none;margin:0;padding:0;}
div, h1, h2, h3, h4, p, form, label, input, textarea, img, span{margin:0;padding:0;word-break:break-all;word-wrap:break-word;}
ul{margin:0;padding:0;list-style-type:none;word-break:break-all;word-wrap:break-word;}
dl,dt,dd{margin:0;padding:0;border:0;}
a{color:#5f6477;text-decoration:none;}
a:hover{color:#5f6477;text-decoration:none;}
:focus{outline:0;}
input,select{font-family:"微软雅黑";}
/* 设置滚动条的样式 */
::-webkit-scrollbar{
	width:5px;
	height:5px;
}
/* 滚动槽 */
::-webkit-scrollbar-track {
	box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
	border-radius:10px;
	background-color: #ddd;
	
}
/* 滚动条滑块 */
::-webkit-scrollbar-thumb {
	border-radius:10px;
	height:5px;
	background:#777;
}

#app{
	height:100%;
	width: 100%;
	display: flex;
	flex-direction: column;
	flex-wrap:nowrap;
	justify-content:flex-start;
	overflow: hidden;
}
.el-tabs--card>.el-tabs__header .el-tabs__nav{
	border-top:0;
	border-radius: 0;
}
// 选项卡默认外间距清除
.el-tabs__header{
	margin:0;
}
.tabContent{
	height: 100px;
	width: 100%;
	border-bottom: 1px solid #E4E7ED;
	text-align: center;
	font-size: 14px;
	display: flex;
	flex-direction: row;
	flex-wrap:nowrap;
	justify-content:flex-start;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
	overflow: auto;
}
.tabImage{
	width: 32px;
	height:32px;
	margin-top:5px;
}
.topButton{
	width: 64px;
	height: 64px;
	cursor:pointer;
}
.topButtons{
	margin-left: 5px;
	margin-right: 5px;
	display: flex;
	flex-direction: row;
	flex-wrap:nowrap;
	justify-content:flex-start;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
}
.description{
	width: 100%;
}
.topButtonsParent{
	border-right:1px solid #E4E7ED;
	height: 100%;
	display: flex;
	flex-direction: column;
	flex-wrap:nowrap;
	justify-content:space-around;
	/* 定义子元素在 纵轴方向的对齐方式  此处为居中*/
	align-items:flex-start;
}
.el-loading-spinner .el-loading-text{
	color:#fff
}
.el-loading-spinner i{
	color:#fff
}
</style>
