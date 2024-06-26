import Vue from 'vue';
import VueRouter from 'vue-router';
import UserSignup from '@/authorization/UserSignup.vue';
import LoginPage from '@/authorization/LoginPage.vue';
import DashBoard from '@/components/DashBoard.vue';
import AdminPage from '@/components/AdminPage.vue';
import SearchPage from '@/components/SearchPage.vue';
import HomePage from '@/components/HomePage.vue';
import AddSection from '@/components/AddSection.vue';
import CreateBook from '@/components/CreateBook.vue';
import ViewBook from '@/components/ViewBooks.vue';


Vue.use(VueRouter);

const routes = [
  { path: '/signup', component: UserSignup, name: 'UserSignup' },
  { path: '/login', component: LoginPage, name: 'LoginPage' },
  { path: '/dashboard',component:DashBoard,name:'DashBoard'},
  {path:'/admin',component:AdminPage,name:'AdminPage'},
  {path:'/search/user',component:SearchPage,name:'SearchPage'},
  {path:'/',component:HomePage,name:'HomePage'},
  {path:'/add/section',component:AddSection,name:'AddSection'},
  {path:'/Create/book',component:CreateBook,name:'CreateBook'},
  {path:'/books',component:ViewBook,name:'ViewBook'}
  
  // { path: '*', redirect: '/login' }
  // Add more routes as needed
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
