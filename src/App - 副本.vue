<template>
  <div id="app">
	<el-row>
	  <el-col :span="24">
		  <el-tabs v-model="activeName" type="card" id="navigationTabList" :before-leave="tabBeforeClick">
		      <el-tab-pane label="地图下载" name="first">
		  		<div class="tabContent">
		  			<!-- 在线地图 -->
		  			<onlinemap></onlinemap>
		  			<!-- 范围设置 -->
		  			<scopeset></scopeset>
		  			<!-- 下载相关 -->
		  			<mapdownload></mapdownload>
		  			<!-- 显示设置 -->
		  			<!-- <showset></showset> -->
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
		      <el-tab-pane label="权限控制" name="fourth">
		  		<div class="tabContent">
		  			<userpermission></userpermission>
		  			<userinfo></userinfo>
		  		</div>
		  	</el-tab-pane>
		  </el-tabs>
	  </el-col>
	</el-row>
    <el-container class="container">
		<el-container>
			<el-tabs v-model="activeName" type="card" id="navigationTabList" :before-leave="tabBeforeClick">
			    <el-tab-pane label="地图下载" name="first">
					<div class="tabContent">
						<!-- 在线地图 -->
						<onlinemap></onlinemap>
						<!-- 范围设置 -->
						<scopeset></scopeset>
						<!-- 下载相关 -->
						<mapdownload></mapdownload>
						<!-- 显示设置 -->
						<!-- <showset></showset> -->
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
			    <el-tab-pane label="权限控制" name="fourth">
					<div class="tabContent">
						<userpermission></userpermission>
						<userinfo></userinfo>
					</div>
				</el-tab-pane>
			</el-tabs>
		</el-container>
		<el-container class="container"	>
			<el-aside>
				<!-- 侧边栏控制台 -->
				<myaside></myaside>
			</el-aside>
			<el-main class="mainClass">
				<el-tabs v-model="tabActionName" type="card" :before-leave="tabBeforeClick" >
					<el-tab-pane label="二维视图" name="1" >
						<!-- 路由匹配的组件将在此处显示 -->
						<router-view></router-view>
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
			</el-main>
		</el-container>
	</el-container>
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
		userinfo
	},
    data() {
      return {
		//顶部选项卡标识
        activeName: 'first',
		//地图窗口选项卡 标识
		tabActionName:"1",
      };
    },
	mounted:function(){
		//初始化indexedDB
		this.initIndexedDB();
		this.initDownLoadTableDatas();
		this.myCommon.updateNameAndUrl();
		//开启websocket
		// this.initWebSocket();
		
	},
    methods: {
		tabBeforeClick(activeName, oldActiveName){
			if(activeName==="3"||activeName==="4"||activeName==="second"||activeName==="third"){
				var data = this.myCommon.isLoginAndTime();
				if(!data.flag){
					this.$message(data.options);
					return data.flag
				}
			}
		},
		//数据库及表初始化函数
		initIndexedDB(){
			let id = this.$store.state.downLoadTableId;
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

// #app{
// 	height:100%;
// 	width:100%;
// }
	// .container{
	// 	height:100%;
	//     width:100%;
	// }
// #mapTabList .is-top{
// 	height: 35px;
// 	line-height: 35px;
// }
// #navigationTabList .is-top{
// 	height: 35px;
// 	line-height: 35px;
// }
// .el-tabs--card>.el-tabs__header .el-tabs__nav{
// 	border-top:0;
// 	border-radius: 0;
// }
// .el-tabs__header{
// 	margin:0;
// }
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
.el-aside{
	border-right:1px solid #E4E7ED;
}
/**
 * 地图窗口相关样式
 */
.el-main{
	padding: 0;
	// width: 100%;
	// height: 100%;
	overflow: hidden;
}
// #mapTabList{
// 	width: 100%;
// }
// #mapTabList .el-tabs__nav div{
// 	height: 30px;
// 	line-height: 30px;
// }
// #mapTabList .el-tabs__content{
// 	width: 100%;
// 	height: 100%;
// }
// #mapTabList .el-tabs__content .el-tab-pane{
// 	width: 100%;
// 	height: 100%;
// }
</style>
