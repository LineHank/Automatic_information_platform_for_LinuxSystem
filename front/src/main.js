// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import App from './App'
import router from './router'
import Index from './components/index'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.prototype.$http = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { Index },
  template: '<Index/>'
})
