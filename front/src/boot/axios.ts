/* eslint-disable @typescript-eslint/no-explicit-any */
import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';
import { API_SERVER } from 'src/constants/common';
import { IStringifyOptions, stringify } from 'qs';
import { useLocalAuthStore } from 'src/stores/auth.store';
import { Router } from 'vue-router';
import { useUserStore } from 'src/stores/user.store';
import { useNotifications } from 'src/composables/useNotifications';
import { USER } from 'src/backend/endpoints/user';
;

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}
const $notify = useNotifications(); 
const api = axios.create({ baseURL: API_SERVER });
const defaultStringifyParams: IStringifyOptions = {
  arrayFormat: 'repeat',
  skipNulls: true,
};

export const axiosParamsSerializer =
  (options: IStringifyOptions = {}): ((params: any) => string) =>
  (params) =>
    stringify(params, {
      ...defaultStringifyParams,
      ...options,
    });

export default boot(({ store, router }: { store: any; router: Router }) => {
  const authStore = useLocalAuthStore(store);
  const userStore = useUserStore(store);
  axios.interceptors.request.use((request) => {
    if (!authStore.isAuthenticated) {
      return request;
    }
    request.headers.Authorization = `${authStore.getToken}`;
    // request.headers.Authorization = `Bearer ${authStore.getToken}`;
    return request;
  });
  api.defaults.paramsSerializer = axiosParamsSerializer();
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response.status === 401) {
        authStore.logout();
        userStore.clearUser();
        router.push('/login');
      }
      return Promise.reject(error);
    }
  );


  let unauthorizedCounter = 0;

  axios.interceptors.request.use(
    (config) => {
      if (unauthorizedCounter > 3) {
        throw new Error('Превышено количество неавторизованных запросов');
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response.status === 422 && error.request.responseURL == USER.LOGIN.url 
        || error.response.status === 500 && error.request.responseURL == USER.LOGIN.url 
        || error.response.status === 400 && error.request.responseURL == USER.LOGIN.url 
        
        ) {
        unauthorizedCounter += 1;
        if (unauthorizedCounter > 3) {
          authStore.logout();
          userStore.clearUser();
          $notify.error('Превышено допустмимое кол-во запросов, F5')
        }
      }
      return Promise.reject(error);
    }
  );
});
export { api };

