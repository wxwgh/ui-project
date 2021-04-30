// const stylelint = require('stylelint-webpack-plugin');
const webpack = require('webpack')
module.exports = {
    outputDir: "web",
    // px转rem的配置（postcss-plugin-px2rem插件）
    lintOnSave: true,
    css: {
        loaderOptions: {
            postcss: {
                plugins: [
                    require('autoprefixer')({ // 配置使用 autoprefixer
                        // browsers: ['last 20 versions'],
                        overrideBrowserslist: ['last 2 versions'] // 记得这里要把 browsers 改为 overrideBrowserslist，autoprefixer 新版本的写法有变
                    }),
                    require('postcss-plugin-px2rem')({
                        rootValue: 16, // 换算基数， 默认100   此处30px 换换rem为 30/16=1.875rem
                        // unitPrecision: 5, //允许REM单位增长到的十进制数字。
                        // propWhiteList: [],  //默认值是一个空数组，这意味着禁用白名单并启用所有属性。
                        // propBlackList: [], //黑名单
                        exclude: /(node_module)/, // 默认false，可以（reg）利用正则表达式排除某些文件夹的方法，例如/(node_module)/ 。如果想把前端UI框架内的px也转换成rem，请把此属性设为默认值
                        // selectorBlackList: [], //要忽略并保留为px的选择器
                        // ignoreIdentifier: false,  //（boolean/string）忽略单个属性的方法，启用ignoreidentifier后，replace将自动设置为true。
                        // replace: true, // （布尔值）替换包含REM的规则，而不是添加回退。
                        mediaQuery: false, // （布尔值）允许在媒体查询中转换px。
                        minPixelValue: 0 // 设置要替换的最小像素值(3px会被转rem)。 默认 0
                    })
                ]
            }
        }
    },
    chainWebpack: config => {
        config.plugin('provide').use(webpack.ProvidePlugin, [{
            $: 'jquery',
            jquery: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }])
    },
	//天地图跨域问题
	// devServer:{
	// 	proxy:{
	// 		'/tdt': { // 程序中的地址
	// 			target: 'http://t1.tianditu.com/',
	// 			changeOrigin: true,
	// 			pathRewrite: {
	// 			  '^/tdt': '',
	// 			}  
	// 		}
	// 	}
	// }
}
