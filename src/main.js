import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

Vue.use(Toast);

// Create a customized instance of Axios
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5000/', // Ensure this is the correct base URL for your backend
});

// Assign axiosInstance to global properties of the Vue app
Vue.prototype.$axios = axiosInstance;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
