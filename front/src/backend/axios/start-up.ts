import { BootFileParams } from '@quasar/app-webpack';
import axios, { AxiosError } from 'axios';
import { stringify, IStringifyOptions } from 'qs';
// import { useLocalAuthStore } from 'stores/auth.store';
// import errorHandleInterceptors from './error.interceptors';

const defaultStringifyParams: IStringifyOptions = {
  arrayFormat: 'repeat',
  skipNulls: true,
};

export default <TState>(context: BootFileParams<TState>) => {
  // console.debug('Booting axios...', context);
  // const authStore = useLocalAuthStore(context.store);

  // context.app.config.globalProperties.$axios = axios;

  // axios.interceptors.request.use((request) => {
  //   console.debug(authStore.isAuthenticated);
  //   if (!authStore.isAuthenticated) {
  //     return request;
  //   }

  //   request.headers.Authorization = `Bearer ${authStore.token}`;
  //   return request;
  // });

  // axios.interceptors.response.use(
  //   (response) => response,
  //   async (error: AxiosError) =>
  //     const needErrorHandleInterceptors = error?.config?.headers?.interceptors ?? true;
  //     if (needErrorHandleInterceptors) {
  //       return errorHandleInterceptors(context, error);
  //     }
  //     Promise.reject(error)
  //   ,
  // );
};
