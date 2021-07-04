<template>
	<div class="topButtonsParent">
		<div class="topButtons">
			<div class="topButton" v-for="post in userPost" :class="{tabMouseOver:post.isShow}" @click="loginClick(post)" @mouseleave="mouseLeave(post)" @mouseover="mouseOver(post)">
				<el-image class="tabImage" :src="post.url" fit='fill'></el-image>
				<div class="description">
					<span>{{post.name}}</span>
				</div>
			</div>
		</div>
		<div class="description">
			<span>用户相关</span>
		</div>
	</div>
</template>

<script>
import userloginbox from '@/components/userloginbox.vue';
import getlicence from '@/components/getlicence.vue';
import updatelicence from '@/components/updatelicence.vue';
export default {
  name: 'userpermission',
  data(){
    return {
		userPost:[
			{
				name:"登录",
				url:require('../assets/user/user.png'),
				isShow:false,
			},
			{
				name:"生成许可",
				url:require('../assets/user/DownLoadManager.png'),
				isShow:false,
			},
			{
				name:"更新许可",
				url:require('../assets/user/DownLoadManager.png'),
				isShow:false,
			},
		],
	}
  },
  methods:{
  	loginClick(post){
		var $this =this;
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		this.myCommon.clearOperation();
		if(post.name==="登录"){
			$this.$confirm(<userloginbox ref='userloginbox'/>, '管理员登录', {
				confirmButtonText: '登录',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						if($this.$store.state.administratorInfo.limitTime){
							if(new Date().getTime()<=$this.$store.state.administratorInfo.limitTime){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '账号已锁定,请5分钟后尝试'
								});
								return false;
							}else{
								$this.$store.state.administratorInfo.limitTime="";
								$this.$store.state.administratorInfo.error_count=0;
							}
							
						}
						if($this.$refs.userloginbox.passwordInput!==$this.$store.state.administratorInfo.password){
							if(++$this.$store.state.administratorInfo.error_count<=3){
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '密码不正确 连续输错3次将锁定5分钟 已输错'+$this.$store.state.administratorInfo.error_count+'次'
								});
								//更新输错次数
								var id=$this.$store.state.user_table_id;
								var data ={
									id:$this.$store.state.administratorInfo.id,
									user_id:$this.$store.state.administratorInfo.user_id,
									name:"管理员",
									password:$this.$store.state.administratorInfo.password,
									describe:"生成许可",
									time:"2121/3/17",
									limitTime:"",
									error_count:$this.$store.state.administratorInfo.error_count,
									isAdmin:true
								}
								$this.myCommon.updateIndexedDB(id,data);
							}else{
								$this.$message({
								    showClose: true,
									type: 'error',
								    message: '账号已锁定,请5分钟后尝试'
								});
								if($this.$store.state.administratorInfo.error_count===4){
									//更新锁定时间
									var id=$this.$store.state.user_table_id;
									$this.$store.state.administratorInfo.limitTime=parseInt(new Date().getTime()) + 300000;
									var data ={
										id:$this.$store.state.administratorInfo.id,
										user_id:$this.$store.state.administratorInfo.user_id,
										name:"管理员",
										password:$this.$store.state.administratorInfo.password,
										describe:"生成许可",
										time:"2121/3/17",
										limitTime:$this.$store.state.administratorInfo.limitTime,
										error_count:4,
										isAdmin:true
									}
									$this.myCommon.updateIndexedDB(id,data);
								}
							}
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				$this.userPost[0].name="注销";
				$this.$store.state.administratorInfo.name = "管理员";
				$this.$store.state.administratorInfo.time="2121/3/17";
				$this.$store.state.administratorInfo.describe="生成许可";
				$this.$store.state.administratorInfo.isAdmin=true;
				$this.$store.state.administratorInfo.limitTime="";
				$this.$store.state.administratorInfo.error_count=0;
				var id=$this.$store.state.user_table_id;
				$this.myCommon.updateIndexedDB(id,$this.$store.state.administratorInfo);
			}).catch(() => {
				
			});
		}else if(post.name==="注销"){
			$this.$confirm('管理员注销?是否继续', '管理员注销', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
				closeOnClickModal:false,
			    type: 'warning'
			}).then(() => {
				$this.userPost[0].name="登录";
				$this.$store.state.administratorInfo.name = "限时用户";
				var id=$this.$store.state.user_table_id;
				$this.myCommon.get_user_time(id,"限时用户");
			}).catch(() => {
			});
		}else if(post.name==="生成许可"){
			if($this.$store.state.administratorInfo.name==="限时用户"){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '管理员特有功能,请先登录'
				});
				return false;
			}
			$this.$confirm(<getlicence ref='getlicence'/>, '生成许可', {
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
						var urlRegex = /[a-zA-Z0-9]+\-[a-zA-Z0-9]+\-[a-zA-Z0-9]+\-[a-zA-Z0-9]+\-[a-zA-Z0-9]+\-[a-zA-Z0-9]+/;
						if(!taskRegex.test($this.$refs.getlicence.task_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '任务名称,格式不正确'
							});
							return false;
						}
						if($this.$refs.getlicence.isName){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '该路径下已存在同名文件'
							});
							return false;
						}
						if(!urlRegex.test($this.$refs.getlicence.url_name)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '计算机物理地址格式不正确'
							});
							return false;
						}
						if(!pathRegex.test($this.$refs.getlicence.save_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '存储地址,格式不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var time = new Date($this.$refs.getlicence.value);
				var formatTime=time.getFullYear() + '/' + (time.getMonth() + 1) + '/' + time.getDate();
				var temp_base = $this.Base64.encode(formatTime);
				var temp_url = $this.Base64.encode($this.$refs.getlicence.url_name);
				var data = {
					task_name:$this.$refs.getlicence.task_name,
					save_path:$this.$refs.getlicence.save_path,
					time:temp_base,
					url:temp_url,
				};
				//调用后端处理函数
				get_licence(data);
				async function get_licence(data){
					await eel.get_licence(data)();
				}
			}).catch(() => {
				
			});
		}else if(post.name==="更新许可"){
			if($this.$store.state.administratorInfo.name==="管理员"){
				$this.$message({
				    showClose: true,
					type: 'error',
				    message: '限时用户功能,管理员无需更新许可'
				});
				return false;
			}
			$this.$confirm(<updatelicence ref='updatelicence'/>, '更新许可', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				closeOnClickModal:false,
				beforeClose:function(action, instance, done){
					if(action==="close"){
						done();
					}else if(action==="cancel"){
						done();
					}else if(action==="confirm"){
						var pathRegex = /[a-zA-Z]:\//;
						if(!pathRegex.test($this.$refs.updatelicence.import_file_path)){
							$this.$message({
							    showClose: true,
								type: 'error',
							    message: '文件格式或路径不正确'
							});
							return false;
						}else{
							done();
						}
					}
				}
			}).then(() => {
				var data={
					url:$this.$refs.updatelicence.import_file_path,
				}
				//调用后端处理函数
				update_licence(data);
				async function update_licence(data){
					var result = await eel.update_licence(data)();
					if(!result.url_correct){
						$this.$message({
						    showClose: true,
							type: 'error',
						    message: '计算机物理地址不匹配,请更换正确许可'
						});
					}else{
						var time = result.time;
						$this.$store.state.administratorInfo.time = result.time;
						var temp = {
							id: $this.$store.state.administratorInfo.user_id,
							name: "限时用户",
							describe: "无需登录,更新许可即可使用本应用",
							isAdmin: false,
							time: time
						};
						var id = $this.$store.state.user_table_id;
						$this.myCommon.updateIndexedDB(id,temp);
					}
				}
			}).catch(() => {
				
			});
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
