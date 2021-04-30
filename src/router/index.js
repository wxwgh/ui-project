import Vue from 'vue'
import VueRouter from 'vue-router'
import CommonMap from '../views/CommonMap.vue'
import BaiduMap from '../views/BaiduMap.vue'

Vue.use(VueRouter)

const routes = [
	{
		path:"/",
		redirect:'/commonMap'
	},
    {
      path: '/commonMap',
      name: 'CommonMap',
      component: CommonMap
    },
	{
	  path: '/baiduMap',
	  name: 'BaiduMap',
	  component: BaiduMap
	},
]

const router = new VueRouter({
    routes
})

export default router
