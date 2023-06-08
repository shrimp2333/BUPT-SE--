import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import VueSetupExtend from 'vite-plugin-vue-setup-extend';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

const baseURL: string = 'http://10.128.201.42:5000'

export default defineConfig({
	server: {
		// 跨域的写法
		proxy: {
			'/a': {
				target: baseURL, // 实际请求地址
				changeOrigin: true,
				rewrite: (path) => path.replace("^/a", ""),
			},
			'/admin': {
				target: baseURL, // 实际请求地址
				changeOrigin: true,
				rewrite: (path) => path.replace("^/admin", ""),
			},
		},
	},
	base: './',
	plugins: [
		vue(),
		VueSetupExtend(),
		AutoImport({
			resolvers: [ElementPlusResolver()]
		}),
		Components({
			resolvers: [ElementPlusResolver()]
		})
	],
	optimizeDeps: {
		include: ['schart.js']
	}
});
