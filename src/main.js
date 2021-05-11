import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//引入element-ui
import ElementUI from 'element-ui';
//引入elment-ui css
import 'element-ui/lib/theme-chalk/index.css';
//引入awesome
import 'font-awesome/css/font-awesome.min.css';
//引入自定义全局样式
import './assets/less/style.css';
//引入自定义全局方法
import myCommon from './assets/common/common.js';
//引入jquery
import $ from 'jquery';
//引入leaflet
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
//引入地图纠偏插件
import './assets/plugins/leaflet.mapCorrection.min.js';
//引入加载第三方地图需要的Proj4
import proj4 from 'proj4';
import proj4leaflet from 'proj4leaflet';
//加载自定义脚本
import './assets/plugins/leaflet.ChineseTmsProviders.js';
import './assets/plugins/leaflet-bing-layer.js';
import './assets/plugins/polyfill.min.js';
//引入turf
import * as turf from '@turf/turf';
//引入axios
import axios from 'axios';

//引入awesome
import 'font-awesome/css/font-awesome.min.css';
//引入cesium
import Cesium from 'cesium/Cesium';
import 'cesium/Widgets/widgets.css';

//坐标转换插件
import {gcj02towgs84} from './assets/plugins/correct.js';
import {Base64} from 'js-base64';

//引入漫游插件
// import './assets/plugins/L.Control.Zoomslider.css';
// import './assets/plugins/L.Control.Zoomslider.js';
//引入移动面板插件
// import './assets/plugins/pancontrol/L.Control.Pan.css';
// import './assets/plugins/pancontrol/L.Control.Pan.js';
//引入解析shp文件插件
import './assets/plugins/analyzeshapefile/shapefile.js';

Vue.prototype.gcj02towgs84=gcj02towgs84;
Vue.prototype.Base64=Base64;
Vue.prototype.Cesium=Cesium;
Vue.prototype.axios = axios;
Vue.prototype.turf = turf;
Vue.prototype.myCommon = myCommon;
Vue.use(ElementUI);
Vue.config.productionTip = false
Vue.prototype.$UUID = function () {
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
    }

    return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4())
}
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
