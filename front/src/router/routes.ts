import { RouteRecordRaw } from 'vue-router';

const AddPhonePage = () =>
  import(
    /* webpackChunkName: "ActivityDirectionList" */ 'src/modules/AddPhone/pages/AddPhone.vue'
  );
const LoginPage = () => import('src/modules/Authorization/Login.vue');
const MainLayout = () => import('src/layouts/MainLayout.vue');
const AuthLayout = () => import('src/layouts/AuthLayout.vue');
const IntercomPage = () =>
  import('src/modules/Intercom/pages/IntercomPage.vue');
const CourierIntercomPage = () =>
  import('src/modules/Intercom/pages/CourierIntercomPage.vue');
const ClientPage = () => import('src/modules/Client/pages/ClientPage.vue');
const TestClientPage = () =>
  import('src/modules/Client/pages/TestClientPage.vue');

const IntercomList = () =>
  import('src/modules/CRM/Intercom/pages/IntercomList.vue');
const EntryList = () =>
  import('src/modules/CRM/Entry/pages/EntryList.vue');
const HouseList = () =>
  import('src/modules/CRM/House/pages/HouseList.vue');

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout,
    children: [{ path: '', component: AddPhonePage, name: 'add_number' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    },
  },
  {
    path: '/login',
    component: AuthLayout,
    children: [{ path: '', component: LoginPage, name: 'login' }],
    meta: {
      title: 'STOWN',
      authorization: false,
    },
  },
  {
    path: '/intercom',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: IntercomPage, name: 'intercom' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    },
  },
  {
    path: '/courier-intercom',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: CourierIntercomPage, name: 'courier-intercom' },
    ],
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
  {
    path: '/test-client',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: TestClientPage, name: 'test-client' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    },
  },
  {
    path: '/intercom-list',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: IntercomList, name: 'intercom-list' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    },
  },
    {
    path: '/entry-list',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: EntryList, name: 'entry-list' }],
    meta: {
      title: 'STOWN',
      authorization: true,
    },
  },
    {
    path: '/house-list',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: HouseList, name: 'house-list' }],
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
    },
  },
];

export default routes;
