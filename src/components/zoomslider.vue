<template>
	<div class="zoomSliderParent">
		<div class="panClass">
			<div v-for="p in pan_post" :class="p.style_class" @click="pan_click(p)" @mouseenter="pan_enter(p)" @mouseleave="pan_leave(p)"></div>
		</div>
		<div class="sliderClass" @mouseenter="ruler_enter" @mouseleave="ruler_leave">
			<div class="zoom_add" @click="zoom_add_click"></div>
			<div class="zoom_ruler" :style="{height:ruler_height+'px'}" >
				<div class="zoom_mask" :style="{height:get_mask_height}" @click.stop="mask_click"></div>
				<div class="zoom_base" :style="{height:ruler_height+'px'}" @click.stop="base_click"></div>
				<div class="zoom_cursor" :style="{top:get_cursor_top}" @mousedown="cursor_down"></div>
				<div class="zoom_label" v-if="is_label_show">
					<div v-for="p in label_post" :class="p.style_class" @click="label_click(p)"></div>
				</div>
			</div>
			<div class="zoom_sub" @click="zoom_sub_click"></div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'zoomslider',
  data(){
    return {
		pan_post:[
			{
				direction:"left",
				style_class:{
					pan_left:true,
					is_left_enter:false
				},
			},
			{
				direction:"top",
				style_class:{
					pan_top:true,
					is_top_enter:false
				},
			},
			{
				direction:"right",
				style_class:{
					pan_right:true,
					is_right_enter:false
				},
			},
			{
				direction:"bottom",
				style_class:{
					pan_bottom:true,
					is_bottom_enter:false
				},
			},
		],
		pan_offset:500,
		label_post:[
			{
				describe:"街道",
				style_class:{
					zoom_label_street:true,
				},
			},
			{
				describe:"城市",
				style_class:{
					zoom_label_city:true,
				},
			},
			{
				describe:"省份",
				style_class:{
					zoom_label_province:true,
				},
			},
			{
				describe:"国家",
				style_class:{
					zoom_label_country:true,
				},
			},
		],
		is_label_show:false,
		ruler_height:147,
		cursor_top:135,
		cursor_move:{
			//相对于body 位置
			client_y:0,
			//相对于div 位置
			off_top:0,
			is_down:false
		}
	}
  },
  computed:{
  	  get_mask_height:function(){
  		  return this.$store.state.zoom_slider_info.mask_height+"px";
  	  },
  	  get_cursor_top:function(){
  		  return this.$store.state.zoom_slider_info.cursor_top+"px";
  	  },
  },
  mounted:function(){
	// 初始化地图事件
	this.init_map_event();
  	//初始化级别指示条
  	this.init_zoom_slider();
  },
  methods:{
	cursor_down(e){
		var $this=this;
		let disX = e.clientX - $(".zoom_cursor").get(0).offsetLeft;
		let disY = e.clientY - $(".zoom_cursor").get(0).offsetTop;
		let t ="";
		var map = $this.myCommon.getMap();
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		document.onmousemove = function(f){
			//通过事件委托，计算移动的距离
			t = f.clientY - disY;
			if(t<=0){
				//设置mask高度
				$this.$store.state.zoom_slider_info.mask_height = 0;
				//设置cursor位置
				$this.$store.state.zoom_slider_info.cursor_top = 0;
			}else if(t>0&&t<135){
				//设置mask高度
				$this.$store.state.zoom_slider_info.mask_height = t+12;
				//设置cursor位置
				$this.$store.state.zoom_slider_info.cursor_top = t;
			}else if(t>=135){
				//设置mask高度
				$this.$store.state.zoom_slider_info.mask_height = 147;
				//设置cursor位置
				$this.$store.state.zoom_slider_info.cursor_top = 135;
			}
		}
		document.onmouseup = function(e){
			document.onmousemove = null;
			document.onmouseup = null;
			if(t<=0){
				map.setZoom(max_zoom);
			}else if(t>0&&t<135){
				// 获取间隔数or级别数
				var steps = max_zoom - min_zoom;
				//获取间隔高度
				var step_height = $this.ruler_height/steps;
				var step_top = $this.cursor_top/steps;
				var zoom = Math.round(t/step_top);
				map.setZoom(max_zoom-zoom);
			}else if(t>=135){
				map.setZoom(min_zoom);
			}
		};
	},
	mask_click(e){
		//获取鼠标点击位置  相对于 div
		var y = e.offsetY;
		var map = this.myCommon.getMap();
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		// 获取间隔数or级别数
		var steps = max_zoom - min_zoom;
		//获取间隔高度
		var step_height = this.ruler_height/steps;
		var zoom_num = parseInt(y/step_height);
		map.setZoom(max_zoom-zoom_num);
	},
	base_click(e){
		//获取鼠标点击位置  相对于 div
		var y = e.offsetY;
		var map = this.myCommon.getMap();
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		// 获取间隔数or级别数
		var steps = max_zoom - min_zoom;
		//获取间隔高度
		var step_height = this.ruler_height/steps;
		var zoom_num = Math.round(y/step_height);
		map.setZoom(max_zoom-zoom_num);
	},
	label_click(post){
		// 0 4 4 6 1
		var map = this.myCommon.getMap();
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		if(post.describe==="街道"){
			map.setZoom(max_zoom-1);
		}else if(post.describe==="城市"){
			map.setZoom(max_zoom-7);
		}else if(post.describe==="省份"){
			map.setZoom(min_zoom+4);
		}else if(post.describe==="国家"){
			map.setZoom(min_zoom);
		}
	},
	init_map_event(){
		var $this =this;
		var map = this.myCommon.getMap();
		map.on("zoomlevelschange",function(){
			$this.init_zoom_slider();
		})
		map.on("zoomend",function(){
			$this.init_zoom_slider();
		})
	},
	//初始化级别指示条
	init_zoom_slider(){
		var map = this.myCommon.getMap();
		var max_zoom = map.getMaxZoom();
		var min_zoom = map.getMinZoom();
		var current_zoom = map.getZoom();
		// 获取间隔数or级别数
		var steps = max_zoom - min_zoom;
		//获取间隔高度
		var step_height = this.ruler_height/steps;
		var step_top = this.cursor_top/steps;
		//设置mask高度
		this.$store.state.zoom_slider_info.mask_height = (max_zoom-current_zoom)*step_height;
		//设置cursor位置
		this.$store.state.zoom_slider_info.cursor_top = (max_zoom-current_zoom)*step_top;
	},
	zoom_add_click(){
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		if(map.getMaxZoom() === map.getZoom()){
			return false;
		}else{
			map.zoomIn();
		}
	},
	zoom_sub_click(){
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		if(map.getMinZoom() === map.getZoom()){
			return false;
		}else{
			map.zoomOut();
		}
	},
	ruler_enter(){
		this.is_label_show=true;
	},
	ruler_leave(){
		this.is_label_show=false;
	},
	pan_click(post){
		var map = this.myCommon.getMap();
		this.myCommon.unbindMapEvent(map);
		this.myCommon.switchMouseStyle(false,map);
		if(post.direction==="left"){
			map.panBy(new L.Point(-this.pan_offset,0));
		}else if(post.direction==="top"){
			map.panBy(new L.Point(0,-this.pan_offset));
		}else if(post.direction==="right"){
			map.panBy(new L.Point(this.pan_offset,0));
		}else if(post.direction==="bottom"){
			map.panBy(new L.Point(0,this.pan_offset));
		}
	},
  	pan_enter(post){
		if(post.direction==="left"){
			post.style_class.is_left_enter=true;
		}else if(post.direction==="top"){
			post.style_class.is_top_enter=true;
		}else if(post.direction==="right"){
			post.style_class.is_right_enter=true;
		}else if(post.direction==="bottom"){
			post.style_class.is_bottom_enter=true;
		}
  	},
	pan_leave(post){
		if(post.direction==="left"){
			post.style_class.is_left_enter=false;
		}else if(post.direction==="top"){
			post.style_class.is_top_enter=false;
		}else if(post.direction==="right"){
			post.style_class.is_right_enter=false;
		}else if(post.direction==="bottom"){
			post.style_class.is_bottom_enter=false;
		}
	},
  },
}
</script>

<style lang="less">
// 平移面板样式
.is_left_enter{
	background: url(../assets/zoomslider/zoomslider.png) -51px -110px;
	background-repeat: no-repeat;
}
.is_top_enter{
	background: url(../assets/zoomslider/zoomslider.png) -70px -110px;
	background-repeat: no-repeat;
}
.is_right_enter{
	background: url(../assets/zoomslider/zoomslider.png) -61px -110px;
	background-repeat: no-repeat;
}
.is_bottom_enter{
	background: url(../assets/zoomslider/zoomslider.png) -84px -110px;
	background-repeat: no-repeat;
}
.zoomSliderParent{
	position: absolute;
	right: 40px;
	top:60px;
	z-index:100000;
}
.panClass{
	position: relative;
	width: 52px;
	height: 52px;
	background: url(../assets/zoomslider/zoomslider.png) 0 -140px;
	background-repeat: no-repeat;
}
.pan_left{
	position:absolute;
	width: 12px;
	height: 18px;
	top: 17px;
	left: 6px;
	cursor:pointer;
	
}
.pan_top{
	position:absolute;
	width: 18px;
	height: 12px;
	top: 5px;
	left: 17px;
	cursor:pointer;
}
.pan_right{
	position:absolute;
	width: 12px;
	height: 18px;
	top: 17px;
	left: 32px;
	cursor:pointer;
}
.pan_bottom{
	position:absolute;
	width: 18px;
	height: 12px;
	top: 31px;
	left: 17px;
	cursor:pointer;
}
// 级别进度条样式
.sliderClass{
	position: relative;
	width: 48px;
	left: 14px;
}
.zoom_add{
	width: 24px;
	height: 21px;
	background: url(../assets/zoomslider/zoomslider.png) 0 -217px;
	background-repeat: no-repeat;
	cursor:pointer;
}
.zoom_ruler{
	position: relative;	
	width: 12px;
	left: 6px;
}
.zoom_base{
	position: absolute;
	width: 12px;
	background: url(../assets/zoomslider/zoombar.png) 0 0;
	cursor:pointer;
}
.zoom_mask{
	position: absolute;
	width: 12px;
	background: url(../assets/zoomslider/zoombar.png) -14px 0;
	z-index:1000000;
	cursor:pointer;
}
.zoom_cursor{
	position: absolute;
	width: 24px;
	height: 12px;
	left: -6px;
	background: url(../assets/zoomslider/zoomslider.png) -127px -164px;
	z-index:2000000;
	cursor:pointer;
}
.zoom_sub{
	width: 24px;
	height: 21px;
	background: url(../assets/zoomslider/zoomslider.png) -26px -224px;
	background-repeat: no-repeat;
	cursor:pointer;
}
.zoom_label_street{
	position: absolute;
	top: 0;
	width: 39px;
	height: 31px;
	left: 20px;
	background: url(../assets/zoomslider/zoomslider.png) -87px -140px;
	background-repeat: no-repeat;
	cursor:pointer;
}
.zoom_label_city{
	position: absolute;
	top: 54px;
	width: 39px;
	height: 31px;
	left: 20px;
	background: url(../assets/zoomslider/zoomslider.png) -87px -171px;
	background-repeat: no-repeat;
	cursor:pointer;
}
.zoom_label_province{
	position: absolute;
	top: 92px;
	width: 39px;
	height: 31px;
	left: 20px;
	background: url(../assets/zoomslider/zoomslider.png) -87px -203px;
	background-repeat: no-repeat;
	cursor:pointer;
}
.zoom_label_country{
	position: absolute;
	top: 129px;
	width: 39px;
	height: 31px;
	left: 20px;
	background: url(../assets/zoomslider/zoomslider.png) -87px -235px;
	background-repeat: no-repeat;
	cursor:pointer;
}
</style>
