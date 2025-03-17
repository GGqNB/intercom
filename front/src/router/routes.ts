import { RouteRecordRaw } from 'vue-router';

const AddPhonePage= () => import(
  /* webpackChunkName: "ActivityDirectionList" */ 'src/modules/AddPhone/pages/AddPhone.vue'
);
const LoginPage = () => import('src/modules/Authorization/Login.vue');
const MainLayout = () => import('src/layouts/MainLayout.vue');
const AuthLayout = () => import('src/layouts/AuthLayout.vue');
const IntercomPage = () =>
  import('src/modules/Intercom/pages/DomophonePage.vue');
const ClientPage = () =>
  import('src/modules/Client/pages/ClientPage.vue');

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout,
    children: [{ path: '', component: AddPhonePage, name : 'add_number' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    }
  },
  {
    path: '/login',
    component: AuthLayout,
    children: [{ path: '', component: LoginPage, name : 'login' }],
    meta: {
      title: 'STOWN',
      authorization: false,

    }
  },
  {
    path: '/domophone',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: IntercomPage, name: 'domophone' }],
    meta: {
      title: 'STOWN',
      authorization: true,
      

    },
  },
  {
    path: '/client',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: ClientPage, name: 'client' }],
    meta: {
      title: 'STOWN',
      authorization: true,

    },
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
    meta: {
      title: 'STOWN',
      authorization: false,
    }
  },
];

export default routes;
