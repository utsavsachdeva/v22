import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store' // Import your Vuex store
import 'bootstrap/dist/css/bootstrap.min.css' 
import 'bootstrap/dist/js/bootstrap.bundle.min.js' 

createApp(App)
  .use(router) 
  .use(store)  
  .mount('#app')
