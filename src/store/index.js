import Vue from 'vue'
import Vuex from 'vuex'
import L from 'leaflet'
//引入加载第三方地图需要的Proj4
import proj4 from 'proj4';
import proj4leaflet from 'proj4leaflet';
//加载自定义脚本
import '../assets/plugins/leaflet.ChineseTmsProviders.js';
import '../assets/plugins/leaflet-bing-layer.js';
import '../assets/plugins/polyfill.min.js';
//引入cesium
import Cesium from 'cesium/Cesium';
var matrixIds=[];
for(let i=0;i<19;i++){
	matrixIds[i]=i+1;
}
function BaiduImageryProvider(options) {
	this._errorEvent = new Cesium.Event();
	this._tileWidth = 256;
	this._tileHeight = 256;
	this._maximumLevel = 18;
	this._minimumLevel = 1;
	var southwestInMeters = new Cesium.Cartesian2(-33554054, -33746824);
	var northeastInMeters = new Cesium.Cartesian2(33554054, 33746824);
	this._tilingScheme = new Cesium.WebMercatorTilingScheme({
		rectangleSouthwestInMeters: southwestInMeters,
		rectangleNortheastInMeters: northeastInMeters
	});
	this._rectangle = this._tilingScheme.rectangle;
	var resource = Cesium.Resource.createIfNeeded(options.url);
	this._resource = resource;
	this._tileDiscardPolicy = undefined;
	this._credit = undefined;
	this._readyPromise = undefined;
}

Object.defineProperties(BaiduImageryProvider.prototype, {
	url: {
		get: function () {
			return this._resource.url;
		}
	},
	proxy: {
		get: function () {
			return this._resource.proxy;
		}
	},
	tileWidth: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('tileWidth must not be called before the imagery provider is ready.');
			}
			return this._tileWidth;
		}
	},

	tileHeight: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('tileHeight must not be called before the imagery provider is ready.');
			}
			return this._tileHeight;
		}
	},

	maximumLevel: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('maximumLevel must not be called before the imagery provider is ready.');
			}
			return this._maximumLevel;
		}
	},

	minimumLevel: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('minimumLevel must not be called before the imagery provider is ready.');
			}
			return this._minimumLevel;
		}
	},

	tilingScheme: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('tilingScheme must not be called before the imagery provider is ready.');
			}
			return this._tilingScheme;
		}
	},

	tileDiscardPolicy: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('tileDiscardPolicy must not be called before the imagery provider is ready.');
			}
			return this._tileDiscardPolicy;
		}
	},

	rectangle: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('rectangle must not be called before the imagery provider is ready.');
			}
			return this._rectangle;
		}
	},

	errorEvent: {
		get: function () {
			return this._errorEvent;
		}
	},
	ready: {
		get: function () {
			return this._resource;
		}
	},
	readyPromise: {
		get: function () {
			return this._readyPromise;
		}
	},
	credit: {
		get: function () {
			if (!this.ready) {
				throw new Cesium.DeveloperError('credit must not be called before the imagery provider is ready.');
			}
			return this._credit;
		}
	},
});

BaiduImageryProvider.prototype.requestImage = function (x, y, level, request) {
	var r = this._tilingScheme.getNumberOfXTilesAtLevel(level);
	var c = this._tilingScheme.getNumberOfYTilesAtLevel(level);
	var s = this.url.replace("{x}", x - r / 2).replace("{y}", c / 2 - y - 1).replace("{z}", level).replace("{s}", Math.floor(10 * Math.random()));
	return Cesium.ImageryProvider.loadImage(this, s);
};

Vue.use(Vuex)

function UUID(){
	function S4() {
		return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
	}
				
	return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4())
}
export default new Vuex.Store({
	//共享数据
    state: {
		viewer:"",
		navigation_tree:[],
		layer_delete_options:[],
		zoom_slider_info:{
			mask_height:"",
			cursor_top:""
		},
		//测试单位
		measure_unit:{
			distance_unit:"米",
			old_distance_unit:"米",
			area_unit:"平方米",
			old_area_unit:"平方米"
		},
		//当前选中图层参数
		layerSelectInfo:{
			option_value:"",
			type:"",
			options:[]
		},
		//当前选取图层参数
		layerOperationInfo:{
			option_value:"",
			type:"",
			options:[]
		},
		administratorInfo:{
			id:"",
			user_id:"",
			name:"限时用户",
			password:"supermap@123",
			describe:"无需登录,更新许可即可使用本应用",
			time:"2022/3/17",
			limitTime:"",
			error_count:"",
			isAdmin:false
		},
		mapContainer:[
			{
				type:"commonMap",
				isShow:true,
				map:"",
				layer:"",
			},
			{
				type:"baiduMap",
				isShow:false,
				map:"",
				layer:"",
			}
		],
		mapList:[
			{
				id:UUID(),
				name:"高德地图",
				isShow:true,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"高德地图-街道",
						isActive:true,
						isShow:false,
						minZoom: 3,
						maxZoom: 18,
						image:require('../assets/gaode/gaoderoad.png'),
						url:"GaoDe.Normal.road",
						realUrl:"http://webrd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
						imageProvider:new Cesium.UrlTemplateImageryProvider({url:"http://webrd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}"}),
					},
					{
						id:UUID(),
						name:"高德地图-影像",
						isActive:false,
						isShow:false,
						minZoom: 3,
						maxZoom: 15,
						image:require('../assets/gaode/gaodeyx.png'),
						url:"GaoDe.Normal.yx",
						realUrl:"http://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
						imageProvider:new Cesium.UrlTemplateImageryProvider({url:"http://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}"}),
					},
				]
			},
			{
				id:UUID(),
				name:"谷歌地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"谷歌地图-街道",
						isActive:false,
						isShow:false,
						minZoom: 0,
						maxZoom: 18,
						url:"Google.Normal.road",
						image:require('../assets/google/googleroad.png'),
						realUrl:"http://maps.allinprior.com/859564aab8d20cc425d0d50d6430309d/vt/lyrs=m@169000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
						imageProvider:new Cesium.UrlTemplateImageryProvider({url:"http://maps.allinprior.com/859564aab8d20cc425d0d50d6430309d/vt/lyrs=m@169000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil"}),
					},
					// {
					// 	id:UUID(),
					// 	name:"百度地图-街道",
					// 	minZoom: 3,
					// 	maxZoom: 18,
					// 	image:require('../assets/baidu/baiduroad.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"Baidu.Normal.road",
					// 	realUrl:"http://maponline3.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20181205&from=jsapi2_0",
					// 	imageProvider:new BaiduImageryProvider({
					// 		url: 'http://maponline3.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20181205&from=jsapi2_0',
					// 	}),
					// },
					// {
					// 	id:UUID(),
					// 	name:"谷歌地图-影像",
					// 	isActive:false,
					// 	isShow:false,
					// 	image:require('../assets/google/googleyx.png'),
					// 	url:"Google.Normal.yx"
					// },
					// {
					// 	id:UUID(),
					// 	name:"谷歌地图-地形",
					// 	isActive:false,
					// 	isShow:false,
					// 	isOff:false,
					// 	mapId:"commonMap",
					// 	image:require('../assets/google/googledx.png'),
					// 	url:"Google.Normal.dx"
					// },
					// {
					// 	id:UUID(),
					// 	name:"谷歌地图-路网",
					// 	isActive:false,
					// 	isShow:false,
					// 	isOff:true,
					// 	mapId:"commonMap",
					// 	image:require('../assets/google/googlelw.png'),
					// 	url:"Google.Normal.lw"
					// },
				]
			},
			{
				id:UUID(),
				name:"OSM地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"OSM地图-街道",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/osm/osmroad.png'),
						isActive:false,
						isShow:false,
						url:"OSM.Normal.road",
						realUrl:"http://tile.openstreetmap.org/{z}/{x}/{y}.png",
						imageProvider:new Cesium.UrlTemplateImageryProvider({url:"http://tile.openstreetmap.org/{z}/{x}/{y}.png"}),
					},
					{
						id:UUID(),
						name:"OSM地图-地形",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/osm/osmzxc.png'),
						isActive:false,
						isShow:false,
						url:"OSM.Normal.dx",
						realUrl:"http://b.tile.thunderforest.com/cycle/{z}/{x}/{y}@2x.png?apikey=6170aad10dfd42a38d4d8c709a536f38",
						imageProvider:new Cesium.UrlTemplateImageryProvider({url:"http://b.tile.thunderforest.com/cycle/{z}/{x}/{y}@2x.png?apikey=6170aad10dfd42a38d4d8c709a536f38"}),
					},
					// {
					// 	id:UUID(),
					// 	name:"OSM地图-交通",
					// 	image:require('../assets/osm/osmjt.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"OSM.Normal.jt",
					// },
					// {
					// 	id:UUID(),
					// 	name:"OSM地图-公共交通",
					// 	image:require('../assets/osm/osmggjt.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"OSM.Normal.ggjt",
					// },
					// {
					// 	id:UUID(),
					// 	name:"OSM地图-人道主义",
					// 	image:require('../assets/osm/osmrdzy.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"OSM.Normal.rdzy",
					// },
				]
			},
			{
				id:UUID(),
				name:"天地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"天地图-街道",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/tianditu/tiandituroad.png'),
						isActive:false,
						isShow:false,
						url:"TianDiTu.Normal.road",
						realUrl:"http://t1.tianditu.gov.cn/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
						imageProvider:new Cesium.WebMapTileServiceImageryProvider({
							url:"http://t0.tianditu.com/vec_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=vec&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
							layer: "vec",
							style: "default",
							format: "tiles",
							tileMatrixSetID: "w",
							maximumLevel: 18,
							show: true
						}),
					},
					{
						id:UUID(),
						name:"天地图-影像",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/tianditu/tiandituyx.png'),
						isActive:false,
						isShow:false,
						url:"TianDiTu.Normal.yx",
						realUrl:"http://t1.tianditu.gov.cn/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
						imageProvider:new Cesium.WebMapTileServiceImageryProvider({
							url:"http://t0.tianditu.com/img_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=img&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
							layer: "img",
							style: "default",
							format: "tiles",
							tileMatrixSetID: "w",
							maximumLevel: 18,
							show: true
						}),
					},
					{
						id:UUID(),
						name:"天地图-地形",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/tianditu/tianditudx.png'),
						isActive:false,
						isShow:false,
						url:"TianDiTu.Normal.dx",
						realUrl:"http://t1.tianditu.gov.cn/DataServer?T=ter_w&X={x}&Y={y}&L={z}&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
						imageProvider:new Cesium.WebMapTileServiceImageryProvider({
							url:"http://t0.tianditu.com/ter_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=ter&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=0da630fb8b2ad4f4fe39c0be421d8aa3",
							layer: "ter",
							style: "default",
							format: "tiles",
							tileMatrixSetID: "w",
							maximumLevel: 18,
							show: true
						}),
					},
				]
			},
			{
				id:UUID(),
				name:"必应地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					// {
					// 	id:UUID(),
					// 	name:"必应地图-街道",
					// 	minZoom: 1,
					// 	maxZoom: 18,
					// 	image:require('../assets/bingmap/bingroad.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
					// 	url:"Road",
					// 	imageProvider:new Cesium.BingMapsImageryProvider({
					// 		url : 'https://dev.virtualearth.net',
					// 		mapStyle : Cesium.BingMapsStyle.ROAD,
					// 		key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y"
					// 	}),
					// },
					{
						id:UUID(),
						name:"必应地图-影像",
						minZoom: 1,
						maxZoom: 18,
						image:require('../assets/bingmap/bingyx.png'),
						isActive:false,
						isShow:false,
						key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
						url:"Aerial",
						imageProvider:new Cesium.BingMapsImageryProvider({
							url : 'https://dev.virtualearth.net',
							mapStyle : Cesium.BingMapsStyle.AERIAL,
							key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y"
						}),
					},
					{
						id:UUID(),
						name:"必应地图-影像+路网",
						minZoom: 1,
						maxZoom: 18,
						image:require('../assets/bingmap/bingyxlw.png'),
						isActive:false,
						isShow:false,
						key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
						url:"AerialWithLabels",
						imageProvider:new Cesium.BingMapsImageryProvider({
							url : 'https://dev.virtualearth.net',
							mapStyle : Cesium.BingMapsStyle.AERIAL_WITH_LABELS,
							key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y"
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"必应地图-黑夜",
					// 	image:require('../assets/bingmap/binghy.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
					// 	url:"CanvasDark"
					// },
					// {
					// 	id:UUID(),
					// 	name:"必应地图-精简",
					// 	image:require('../assets/bingmap/bingjj.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
					// 	url:"CanvasLight"
					// },
					// {
					// 	id:UUID(),
					// 	name:"必应地图-灰色",
					// 	image:require('../assets/bingmap/binghs.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	key:"AlZYB-gED-VU97g8sxXkkQFR9lodXJtSByPb-yoZsE4mnpfD35DIqwhPAQMXwo8Y",
					// 	url:"CanvasGray"
					// },
				]
			},
			{
				id:UUID(),
				name:"腾讯地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"腾讯地图-街道",
						minZoom: 3,
						maxZoom: 18,
						image:require('../assets/tengxun/tengxunroad.png'),
						isActive:false,
						isShow:false,
						url:"TengXun.Normal.road",
						realUrl:"http://rt2.map.gtimg.com/realtimerender?z={z}&x={x}&y={y}&type=vector&style=0",
						imageProvider:new Cesium.UrlTemplateImageryProvider({
							url:"http://rt2.map.gtimg.com/realtimerender?z={z}&x={x}&y={reverseY}&type=vector&style=0",
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"腾讯地图-影像",
					// 	minZoom: 3,
					// 	maxZoom: 18,
					// 	image:require('../assets/tengxun/tengxunyx.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"TengXun.Normal.yx",
					// 	realUrl:"https://p2.map.gtimg.com/sateTiles/{z}/{x}/{y}/{x}_{y}.jpg?",
					// 	imageProvider:new Cesium.UrlTemplateImageryProvider({
					// 		url:"https://p2.map.gtimg.com/sateTiles/{z}/{sx}/{sy}/{x}_{reverseY}.jpg?version=229",
					// 		customTags:{
					// 		    sx: function(imageryProvider, x, y, level) {
					// 			    return x>>4;
					// 		    },
					// 		    sy:function(imageryProvider, x, y, level) {
					// 			    return ((1<<level)-y)>>4;
					// 		    }
					// 		}
					// 	}),
					// },
					{
						id:UUID(),
						name:"腾讯地图-地形",
						minZoom: 3,
						maxZoom: 18,
						image:require('../assets/tengxun/tengxundx.png'),
						isActive:false,
						isShow:false,
						url:"TengXun.Normal.dx",
						realUrl:"http://p2.map.gtimg.com/demTiles/{z}/{x}/{y}/{x}_{y}.jpg",
						imageProvider:new Cesium.UrlTemplateImageryProvider({
							url:"https://p2.map.gtimg.com/demTiles/{z}/{sx}/{sy}/{x}_{reverseY}.jpg?version=229",
							customTags:{
							    sx: function(imageryProvider, x, y, level) {
								    return x>>4;
							    },
							    sy:function(imageryProvider, x, y, level) {
								    return ((1<<level)-y)>>4;
							    }
							}
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"腾讯地图-路网标注",
					// 	image:require('../assets/tengxun/tengxunlwbz.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"TengXun.Normal.lwbz"
					// },
					// {
					// 	id:UUID(),
					// 	name:"腾讯地图-强边界",
					// 	image:require('../assets/tengxun/tengxunqbj.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"TengXun.Normal.qbj"
					// },
					// {
					// 	id:UUID(),
					// 	name:"腾讯地图-黑夜",
					// 	image:require('../assets/tengxun/tengxunhy.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"TengXun.Normal.hy"
					// },
				]
			},
			{
				id:UUID(),
				name:"易智瑞",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"易智瑞-街道",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/esri/esriroad.png'),
						isActive:false,
						isShow:false,
						url:"Esri.Normal.road",
						realUrl:"http://map.geoq.cn/arcgis/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://map.geoq.cn/arcgis/rest/services/ChinaOnlineCommunity/MapServer',
						}),
					},
					{
						id:UUID(),
						name:"易智瑞-影像",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/esri/esriyx.png'),
						isActive:false,
						isShow:false,
						url:"Esri.Normal.yx",
						realUrl:"http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer'
						}),
					},
					{
						id:UUID(),
						name:"易智瑞-地形",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/esri/esridx.png'),
						isActive:false,
						isShow:false,
						url:"Esri.Normal.dx",
						realUrl:"http://server.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://server.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer'
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"易智瑞-蓝黑",
					// 	image:require('../assets/esri/esrilh.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"Esri.Normal.lh"
					// },
				]
			},
			{
				id:UUID(),
				name:"Here地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"Here地图-精简",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/heremap/herejj.png'),
						isActive:false,
						isShow:false,
						url:"HereMap.Normal.jj",
						realUrl:"http://1.base.maps.api.here.com/maptile/2.1/xbasetile/newest/reduced.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
						imageProvider:new Cesium.UrlTemplateImageryProvider({
							url:"http://1.base.maps.api.here.com/maptile/2.1/xbasetile/newest/reduced.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
						}),
					},
					{
						id:UUID(),
						name:"Here地图-影像",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/heremap/hereyx.png'),
						isActive:false,
						isShow:false,
						url:"HereMap.Normal.yx",
						realUrl:"http://1.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/satellite.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=/eng",
						imageProvider:new Cesium.UrlTemplateImageryProvider({
							url:"http://1.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/satellite.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=/eng",
						}),
					},
					{
						id:UUID(),
						name:"Here地图-地形",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/heremap/heredx.png'),
						isActive:false,
						isShow:false,
						url:"HereMap.Normal.dx",
						realUrl:"http://4.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/terrain.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
						imageProvider:new Cesium.UrlTemplateImageryProvider({
							url:"http://4.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/terrain.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
						}),
					},
				]
			},
			{
				id:UUID(),
				name:"智图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:340097336",
					"1:170048668",
					"1:85024334",
					"1:42512167",
					"1:21256083",
					"1:10628041",
					"1:5314020",
					"1:2657010",
					"1:1328505",
					"1:664252",
					"1:332126",
					"1:166063",
					"1:83031",
					"1:41515",
					"1:20757",
					"1:10378",
					"1:5189",
					"1:2594",
					"1:1297",
				],
				urls:[
					{
						id:UUID(),
						name:"智图-彩色",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/zhitu/zhitucs.png'),
						isActive:false,
						isShow:false,
						url:"ZhiTu.Normal.cs",
						realUrl:"http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer',
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"智图-暖色",
					// 	image:require('../assets/zhitu/zhituns.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"ZhiTu.Normal.ns"
					// },
					{
						id:UUID(),
						name:"智图-灰色",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/zhitu/zhituhs.png'),
						isActive:false,
						isShow:false,
						url:"ZhiTu.Normal.hs",
						realUrl:"http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetGray/MapServer',
						}),
					},
					{
						id:UUID(),
						name:"智图-蓝黑",
						minZoom: 0,
						maxZoom: 18,
						image:require('../assets/zhitu/zhitulh.png'),
						isActive:false,
						isShow:false,
						url:"ZhiTu.Normal.lh",
						realUrl:"http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}",
						imageProvider:new Cesium.ArcGisMapServerImageryProvider({
							url: 'http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetPurplishBlue/MapServer',
						}),
					},
				]
			},
			{
				id:UUID(),
				name:"百度地图",
				isShow:false,
				center: [39.550339, 100.114129],
				dpi:96,
				scale:[
					"1:743085354",
					"1:371542677",
					"1:185771338",
					"1:92885669",
					"1:46442834",
					"1:23221417",
					"1:11610708",
					"1:5805354",
					"1:2902677",
					"1:1451338",
					"1:725669",
					"1:362834",
					"1:181417",
					"1:90708",
					"1:45354",
					"1:22677",
					"1:11338",
					"1:5669",
					"1:2834",
				],
				crs:L.CRS.Baidu,
				urls:[
					{
						id:UUID(),
						name:"百度地图-街道",
						minZoom: 3,
						maxZoom: 18,
						image:require('../assets/baidu/baiduroad.png'),
						isActive:false,
						isShow:false,
						url:"Baidu.Normal.road",
						realUrl:"http://maponline3.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20181205&from=jsapi2_0",
						imageProvider:new BaiduImageryProvider({
							url: 'http://maponline3.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20181205&from=jsapi2_0',
						}),
					},
					{
						id:UUID(),
						name:"百度地图-影像",
						minZoom: 3,
						maxZoom: 18,
						image:require('../assets/baidu/baiduyx.png'),
						isActive:false,
						isShow:false,
						url:"Baidu.Normal.yx",
						realUrl:"http://shangetu1.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46&udt=20181205&scale=1",
						imageProvider:new BaiduImageryProvider({
							url: 'http://shangetu1.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46&udt=20181205&scale=1',
						}),
					},
					// {
					// 	id:UUID(),
					// 	name:"百度地图-黑夜",
					// 	image:require('../assets/baidu/baiduhy.png'),
					// 	isActive:false,
					// 	isShow:false,
					// 	url:"Baidu.Normal.hy"
					// },
				]
			},
		],
		gaodeKey:"0244190557d71e34ec9394db3d75ce32",
		downLoadTableId:"dc876853-e318-4e16-a962-f002e8f9cdce",
		user_table_id:"befa2a7b-4a45-4e5d-8fe8-8d700cfbf64c",
		scopeInfo:{
			isXZQH:"",
			adcode:"",
			scopeLayer:[],
			geojson:"",
		},
		downloadInfo:{
			vector_load_info:{
				id:"",
				url:"./osm/osm.udbx",
				dataset_name:"",
				dataset_names:[],
				scope:"",
				taskName:"",
				downType:"",
				time:"",
				savePath:"",
			},
			coordinate_trans_info:{
				id:"",
				url:"",
				downType:"坐标转换",
				taskName:"",
				savePath:"",
				coordinate:"",
				saveType:"",
				time:"",
			},
			id:"",
			mapName:"高德地图",
			taskName:"",
			savePath:"D:/SuperMap DownLoad",
			layer_type:"",
			geometrys:[],
			time:"",
			total:0,
			saveType:"",
			downType:"",
			northWest:"",
			coordinate:"",
			bounds:"",
			area:[],
			isJoint:false,
			url:"http://webrd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
			scope:[],
			scopeLngLat:{},
			zoom:[],
			resolution:[]
		},
		downloadTableDatas:[],
		taskTableDatas:[],
		attributeHeader:[],
		attributeTable:[],
		layerGroups:[
			{
				id: UUID(),
				label: '我的图层',
				layerGroupId:"",
				index:"1",
				isTip:false,
				isSelect:false,
				children: [],
			},
		],
	},
	//更新状态
    mutations: {
		// update_map(state, map){
		// 	state.map = map;
		// },
	},
    actions: {},
    modules: {}
})
