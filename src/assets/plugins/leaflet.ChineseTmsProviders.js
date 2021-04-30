// this L.CRS.Baidu from https://github.com/muyao1987/leaflet-tileLayer-baidugaode/blob/master/src/tileLayer.baidu.js

if (L.Proj) {
    L.CRS.Baidu = new L.Proj.CRS('EPSG:900913', '+proj=merc +a=6378206 +b=6356584.314245179 +lat_ts=0.0 +lon_0=0.0 +x_0=0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs', {
        resolutions: function () {
            var level = 19
            var res = [];
            res[0] = Math.pow(2, 18);
            for (var i = 1; i < level; i++) {
                res[i] = Math.pow(2, (18 - i))
            }
            return res;
        }(),
        origin: [0, 0],
        bounds: L.bounds([20037508., 0], [0, 20037508.342789244])
    });
}

L.TileLayer.ChinaProvider = L.TileLayer.extend({

    initialize: function (type, options) { 
        var providers = L.TileLayer.ChinaProvider.providers;

        options = options || {}

        var parts = type.split('.');

        var providerName = parts[0];
        var mapName = parts[1];
        var mapType = parts[2];

        var url = providers[providerName][mapName][mapType];
        options.subdomains = providers[providerName].Subdomains;
        options.key = options.key || providers[providerName].key;

        if ('tms' in providers[providerName]) {
            options.tms = providers[providerName]['tms']
        }
        L.TileLayer.prototype.initialize.call(this, url, options);
    }
});

L.TileLayer.ChinaProvider.providers = {
    TianDiTu: {
        Normal: {
            road: "//t{s}.tianditu.gov.cn/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk={key}",
            yx:"//t{s}.tianditu.gov.cn/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk={key}",
			dx:"//t{s}.tianditu.gov.cn/DataServer?T=ter_w&X={x}&Y={y}&L={z}&tk={key}"
        },
        Satellite: {
            Map: "//t{s}.tianditu.gov.cn/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk={key}",
            Annotion: "//t{s}.tianditu.gov.cn/DataServer?T=cia_w&X={x}&Y={y}&L={z}&tk={key}"
        },
        Terrain: {
            Map: "//t{s}.tianditu.gov.cn/DataServer?T=ter_w&X={x}&Y={y}&L={z}&tk={key}",
            Annotion: "//t{s}.tianditu.gov.cn/DataServer?T=cta_w&X={x}&Y={y}&L={z}&tk={key}"
        },
        Subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
        key: "174705aebfe31b79b3587279e211cb9a"
    },

    GaoDe: {
        Normal: {
            road: '//webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
			yx:'//webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
			lw:'//wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=2&style=8&ltype=11',
        },
        Subdomains: ["1", "2", "3", "4"]
    },

    Google: {
        Normal: {
            road: "//maps.allinprior.com/859564aab8d20cc425d0d50d6430309d/vt/lyrs=m@169000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
			yx:"//webst03.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
			// dx:"//www.google.com/maps/vt/pb=!1m4!1m3!1i{z}!2i{x}!3i{y}!2m2!1e5!2sshading!2m2!1e6!2scontours!2m3!1e0!2sm!3i538262670!3m7!5e1105!12m1!1e67!12m1!1e63!12m1!1e3!4e0!5m2!5f1.5!6b1!28i538",
			// lw:"//wprd04.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=2&style=8&ltype=11"
        },
        Subdomains: []
    },

    Esri: {
        Normal: {
			road:"//map.geoq.cn/arcgis/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}",
            yx: "//server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            dx: "//server.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
            lh: "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}",
        },
        Subdomains: []
    },
	TengXun: {
	    Normal: {
	        road: "//rt2.map.gtimg.com/realtimerender?z={z}&x={x}&y={y}&type=vector&style=0",
	        yx: "//p2.map.gtimg.com/sateTiles/{z}/{x}/{y}/{x}_{y}.jpg?version=229",
	        dx: "//p2.map.gtimg.com/demTiles/{z}/{x}/{y}/{x}_{y}.jpg",
			lwbz:"//rt0.map.gtimg.com/tile?z={z}&x={x}&y={y}&styleid=2&version=629",
			qbj:"//rt0.map.gtimg.com/tile?z={z}&x={x}&y={y}&styleid=3&version=629",
			hy:"//rt0.map.gtimg.com/tile?z={z}&x={x}&y={y}&styleid=4&version=629",
	    },
	    Subdomains: [],
		tms:true
	},
	HereMap:{
		Normal: {
		    // road: "https://assets.vector.hereapi.com/styles/berlin/base/mapbox/tilezen?apikey=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=/eng",
			yx:"//1.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/satellite.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=/eng",
			dx:"//4.aerial.maps.api.here.com/maptile/2.1/xbasetile/newest/terrain.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
			jj:"//1.base.maps.api.here.com/maptile/2.1/xbasetile/newest/reduced.day/{z}/{x}/{y}/256/png8?app_id=5E8QOXI78RNGgasTxmPR&token=NJI0HzzrkzLyyne3mAFm3Q&lg=ENG",
		},
		Subdomains: []
	},
	ZhiTu:{
		Normal: {
		    cs: "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}",
			ns:"//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetWarm/MapServer/tile/{z}/{y}/{x}",
			hs:"//map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}",
			lh:"//map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}",
			ywbz:"//map.geoq.cn/arcgis/rest/services/ChinaOnlineCommunityENG/MapServer/tile/{z}/{y}/{x}",
			bjbz:"//thematic.geoq.cn/arcgis/rest/services/ThematicMaps/administrative_division_boundaryandlabel/MapServer/tile/{z}/{y}/{x}",
			sx:"//thematic.geoq.cn/arcgis/rest/services/ThematicMaps/WorldHydroMap/MapServer/tile/{z}/{y}/{x}",
		},
		Subdomains: []
	},
    OSM: {
        Normal: {
            road: "//tile.openstreetmap.org/{z}/{x}/{y}.png",
			dx:"//b.tile.thunderforest.com/cycle/{z}/{x}/{y}@2x.png?apikey=6170aad10dfd42a38d4d8c709a536f38",
			jt:"//a.tile.thunderforest.com/transport/{z}/{x}/{y}@2x.png?apikey=6170aad10dfd42a38d4d8c709a536f38",
			ggjt:"//tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png",
			rdzy:"//tile-a.openstreetmap.fr/hot/{z}/{x}/{y}.png"
        },
        Subdomains: []
    },
	BiYing: {
        Normal: {
            road: "//t0.dynamic.tiles.ditu.live.com/comp/ch/030?mkt=zh-CN&ur=CN&it=G,TW,RL&n=z&og=473&cstl=vb",
			yx:"//tile-a.openstreetmap.fr/hot/{z}/{x}/{y}.png"
        },
        Subdomains: []
    },
	
    Baidu: {
        Normal: {
            road: '//maponline3.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20181205&from=jsapi2_0',
			yx:'//shangetu{s}.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46&udt=20181205&scale=1',
			qxl:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=light',
			hy:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=dark',
			hsjj:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=redalert',
			jj:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=googlelite',
			zrl:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=grassgreen',
			wyl:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=midnight',
			lmf:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=pink',
			qcl:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=darkgreen',
			qxll:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=bluish',
			gdh:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=grayscale',
			qbj:'//api2.map.bdimg.com/customimage/tile?&x={x}&y={y}&z={z}&udt=20201229&scale=2&ak=E4805d16520de693a3fe707cdc962045&customid=hardedge',
        },
        Subdomains: '0123456789',
		tms:true
    }

};

L.tileLayer.chinaProvider = function (type, options) {
    return new L.TileLayer.ChinaProvider(type, options);
};

