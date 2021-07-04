<template>
	<div>
		<el-input v-model="dinput" size="small"></el-input>
		<div class="dfm_button_parent">
			<el-button type="text" @click="d_trans_dfm">度
				<i class="el-icon-right"></i>
			度分秒
			</el-button>
			<el-button type="text" @click="dfm_trans_d">度分秒
				<i class="el-icon-right"></i>
			度</el-button>
		</div>
		<el-input v-model="dfminput" size="small"></el-input>
	</div>
</template>

<script>
export default {
  name: 'dfmtransitionbox',
  data(){
    return {
		dinput:"100.100000",
		dfminput:"",
		// image:require('../assets/maptools/reverse.png'),
	}
  },
  methods:{
	//度 转 度分秒
	d_trans_dfm(){
		var reg = /^(-?\d+)\.(\d+)+$/;
		var flag = reg.test(this.dinput);
		if(flag&&parseInt(this.dinput)<=180.00&&parseInt(this.dinput)>=-180.00){
			var dfm = this.duToGpsDMS(this.dinput);
			this.dfminput=dfm;
		}else{
			this.$message({
			    showClose: true,
				type: 'error',
			    message: '度格式不正确'
			});
			return false;
		}
	},
	//度分秒 转 度
	dfm_trans_d(){
		var reg = /^(-?\d+)\°(\d+)\′(\d+)\.(\d+)\″+$/;
		var flag = reg.test(this.dfminput);
		if(flag){
			var du = this.gpsDMSToDu(this.dfminput);
			this.dinput=du;
		}else{
			this.$message({
			    showClose: true,
				type: 'error',
			    message: '度分秒格式不正确'
			});
			return false;
		}
		
	},
	duToGpsDMS(duStr){
	    var strLength=duStr.length;
	    var tempString="";
	    var tempStrArray=new Array();
	    var tempCount=0;
	    var tempPointFlag=0;
	    var gpsDMS;
	    for(var i=0;i<=strLength;i++){
	        if(duStr[i]>='0' && duStr[i]<='9') {
	            tempString += duStr[i];
	            continue;
	        }else if(duStr[i]=='.'){
	            tempStrArray[tempCount]=tempString;
	            tempString="";
	            tempCount++;
	            tempStrArray[tempCount]='.';
	            tempPointFlag=1;
	            tempCount++;
	        }else if(tempString.length>0){
	            tempStrArray[tempCount]=tempString;
	            tempString="";
	            tempCount++;
	        }
	    }
	    if(tempPointFlag==1){
	        var num1=tempStrArray[0];
	        var num2=parseFloat('0'+tempStrArray[1]+ tempStrArray[2],10)*60;
	        var num3=parseFloat((num2-parseInt(num2,10))*60,10).toFixed(2);
	        num2=parseInt(num2,10);
	        gpsDMS=num1+"°"+num2+"′"+num3+"″";
	    }
	    return gpsDMS;
	},
	gpsDMSToDu(gpsStr){
	    gpsStr=gpsStr.toLowerCase();
	    gpsStr=gpsStr.replace(/\s+/g,"");
	    var tempStrArray=new Array();
	    var flag=1;
	    var lastFlag=0;
	    var strLength=gpsStr.length;
	    var gpsDu=new Array();
	    var gpsDir;
	    var tempcount=0;
	    var tempString="";
	    var tempPointFlag=0;
	    if (gpsStr[0] == 'w' || gpsStr[0] == 's') {
	        flag = -1;
	        lastFlag=0;
	        gpsDir=gpsStr[0];
	    } else if (gpsStr[strLength - 1] == 'w' || gpsStr[strLength - 1] == 's') {
	        flag = -1;
	        lastFlag=1;
	        gpsDir=gpsStr[strLength - 1];
	    }
	    for(var i=0;i<=strLength;i++){
	        if(gpsStr[i]>='0' && gpsStr[i]<='9') {
	          tempString += gpsStr[i];
	            continue;
	        }else if(gpsStr[i]=='.'){
	            tempStrArray[tempcount]=tempString;
	            tempString="";
	            tempcount++;
	            tempStrArray[tempcount]='.';
	            tempPointFlag=1;
	            tempcount++;
	        }else if(tempString.length>0){
	            tempStrArray[tempcount]=tempString;
	            tempString="";
	            tempcount++;
	        }
	    }
	    if(tempPointFlag==0){
	        var num1=parseInt(tempStrArray[0],10);
	        var num2=parseInt(tempStrArray[1],10);
	        var num3=parseInt(tempStrArray[2],10);
	        gpsDu[1]=num1+num2/60+num3/(60*60);
	        gpsDu[1]=gpsDu[1]*flag;
	        gpsDu[0]=gpsDir;
	    }else if (tempPointFlag==1){
	        var num1=parseInt(tempStrArray[0],10);
	        var num2=parseFloat(tempStrArray[1]+'.'+tempStrArray[3],10);
	        gpsDu[1]=num1+num2/60;
	        gpsDu[1]=gpsDu[1]*flag;
	        gpsDu[0]=gpsDir;
	    }
	    return gpsDu[1].toFixed(6)+"";
	},
  },
}
</script>

<style lang="less">
.dfm_button_parent{
	display: flex;
	flex-direction: row;
	justify-content:space-around;
}
.tipClass{
	position:absolute;
}
</style>