// /* eslint-disable no-underscore-dangle */
// import { BootFileParams } from '@quasar/app-webpack';
// import { useNotifications } from 'AdminDir/composables/useNotifications';
// import { HTTP_CODE_ERROR } from 'SharedDir/constants/http-codes';
// import { AUTHORIZATION } from 'SharedDir/backend/endpoints/access';
// import axios, { InternalAxiosRequestConfig, AxiosError } from 'axios';
// import { useLocalAuthStore } from 'AdminDir/stores/auth.store';
// import { parseJwt } from 'SharedDir/utils/http-handle';
// import { useUserStore } from 'AdminDir/stores/user.store';
// import { LoginUserInfo } from 'AdminDir/declarations/access';

// const loginUrls = [AUTHORIZATION.LOGIN.url, AUTHORIZATION.ESIA_LOGIN.url];

// let isRefreshing = false;
// let failedQueue: Array<any> = [];

// const processQueue = (error, token: string | null = null) => {
//   failedQueue.forEach((promise: any) => {
//     if (error) {
//       promise.reject(error);
//     } else {
//       promise.resolve(token);
//     }
//   });

//   failedQueue = [];
// };

// type ExtendedInternalAxiosRequestConfig = InternalAxiosRequestConfig & { _retry: boolean };

// /**
//  *
//  * @param context Контекст пробрасывается в том числе для возможности использования router при разоавторизации пользователя в случае наличия 401 ошибки
//  * @param error
//  * @returns
//  */
// const errorHandleInterceptors = async <TState>(
//   context: BootFileParams<TState>,
//   error: AxiosError,
// ) => {
//   const notify = useNotifications();
//   const authStore = useLocalAuthStore();
//   const userStore = useUserStore();

//   const originalRequest = error.config as ExtendedInternalAxiosRequestConfig;

//   /**
//    * В данное условие попадает только запрос, который пошёл за токеном, но сам получил 401 ошибку
//    * В таком случае гарантированно делаем разлогин пользователя и перекидываем на главную страницу
//    */
//   if (isRefreshing && originalRequest.url === AUTHORIZATION.REFRESH_TOKEN.url) {
//     processQueue(true, null);
//     isRefreshing = false;
//     authStore.logout();
//     userStore.clearUser();
//     context.router.push({ name: 'login' });
//   }

//   // Если нет соединения с сервером
//   if (typeof error.response === 'undefined') {
//     const message = 'Ошибка соединения с сервером, через несколько минут всё заработает!';
//     notify.failureNotification(message);

//     return Promise.reject(error);
//   }

//   /**
//    * Обработка 429 Too Many Requests («слишком много запросов»)
//    */
//   if (error.response.status === HTTP_CODE_ERROR.MANY_REQUESTS) {
//     const message = 'Превышено допустимое количество запросов. Пожалуйста, повторите через несколько минут!';
//     notify.failureNotification(message);
//   }

//   /**
//    * Обработка 401 ошибки Unauthorized («не авторизован (не представился)») и вызывался не метод авторизации
//    *
//    * Пытаемся выполнить переавторизацию пользователя, если ошибка возникла не при вызове запроса на вторизацию
//    */
//   if (
//     error.response.status === HTTP_CODE_ERROR.UNAUTHORIZED
//     && !loginUrls.includes(error.request.responseURL)
//     && !originalRequest._retry
//   ) {
//     /**
//      * Проверка используемая для того, чтобы только первый запрос, получивший 401 ошибку ходил за новым токеном
//      * Остальные запросы встают в очередь и ждут, когда первый запрос вернется с новым токеном и достанет их из очереди с использованием
//      * функции processQueue
//      */
//     if (isRefreshing) {
//       return new Promise((resolve, reject) => {
//         failedQueue.push({ resolve, reject });
//       })
//         .then((token) => {
//           originalRequest.headers.Authorization = `Bearer ${token}`;
//           return axios(originalRequest);
//         })
//         .catch((err) => Promise.reject(err));
//     }

//     originalRequest._retry = true;
//     // Флаг, сообщающий, что за рефреш токеном уже отправились
//     isRefreshing = true;

//     /**
//      * Выполнение переавторизации с сохранением нового токена
//      * и запуском функции, достающей из очереди запросы, которые ожидают обновления рефреш токена
//      */
//     return new Promise((resolve, reject) => {
//       axios({
//         ...AUTHORIZATION.REFRESH_TOKEN,
//         data: { refresh_token: authStore.getRefreshToken },
//       })
//         .then(({ data }: { data: LoginUserInfo }) => {
//           const { token, user } = data;
//           authStore.setToken(token);
//           originalRequest.headers.Authorization = `Bearer ${token}`;

//           const parsedRefreshToken = parseJwt(token)?.refresh_token ?? null;
//           authStore.setRefreshToken(parsedRefreshToken);
//           userStore.setUser(user);

//           resolve(axios(originalRequest));
//           processQueue(null, token);
//         })
//         .catch((err) => {
//           processQueue(err, null);
//           reject(err);

//           authStore.logout();
//           userStore.clearUser();
//           context.router.push({ name: 'login' });
//         })
//         .finally(() => {
//           isRefreshing = false;
//         });
//     });
//   }

//   return Promise.reject(error);
// };

// export default errorHandleInterceptors;
