import { defineStore } from 'pinia';
import { StoreFlag } from 'src/declarations/store/store-flag';
import { useUserStore } from './user.store';
// import { cookiesStorage } from './cookiesStorage';
// function getStorageSettings() {
//   if (process.env.AUTH_TOKEN_STORAGE === 'cookie') {
//     return {
//       storage: cookiesStorage,
//     };
//   }
//   return true;
// }


export const useLocalAuthStore = defineStore('auth', {
  persist: true,

  state: (): StoreFlag.AuthStateInterface => ({
    accessToken: null,
  }),

  getters: {
    getToken: (state: StoreFlag.AuthStateInterface) => state.accessToken,
    isAuthenticated: (state: StoreFlag.AuthStateInterface) => !!state.accessToken,
  },

  actions: {
    setAccessToken(token: string | null) {
      this.accessToken = token;
    },

    async logout() {
      const userStore = useUserStore();
      this.setAccessToken(null);
      userStore.clearUser();

    },

    // /**
    //  * Обновляем токен авторизации.
    //  *
    //  * @dispatches `setToken`
    //  * @dispatches `setRefreshToken`
    //  * @dispatches `user/setUser`
    //  * @param {ActionContext<AuthStateInterface, SharedStateInterface>} { state, dispatch, rootState }
    //  * @returns {Promise<'REFRESHED'>}
    //  */
    // async refreshToken(
    //   { state, dispatch }: ActionContext<AuthStateInterface, SharedStateInterface>,
    //   axiosInstance?: any
    // ): Promise<'REFRESHED'> {
    //   const axiosTransport = axiosInstance || axios;
    //   const data = (({ refreshToken: token }) => ({ token }))(state);

    //   const {
    //     data: { token: newToken, user: userInfo, userProfiles },
    //   } = (await axiosTransport({ ...AUTHORIZATION.REFRESH_TOKEN, data })) as AxiosResponse<{
    //     token: string;
    //     user: Record<string, unknown>;
    //     userProfiles: Array<unknown>;
    //   }>;

    //   const newRefreshToken = parseJwt(newToken)?.refresh_token ?? null;
    //   await dispatch('setToken', newToken);
    //   await dispatch('setRefreshToken', newRefreshToken);
    //   // await dispatch('user/setUser', { token: newToken, ...userInfo }, { root: true });
    //   // await dispatch('user/setUserProfiles', userProfiles, { root: true });
    //   return 'REFRESHED';
    // },
  },
});
