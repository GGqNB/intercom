/* eslint-disable no-undef */
/* eslint-disable @typescript-eslint/no-unused-vars */
import { computed, Ref, ref } from 'vue';
import { useUserStore } from 'stores/user.store';
import { UserInfo } from 'AdminDir/declarations/access';
import { useLocalAuthStore } from 'src/stores/auth.store';
import { User } from 'src/declarations/responses/user';

export function useCurrentUser() {
  const userStore = useUserStore();
  const authStore = useLocalAuthStore();

  const accessToken = computed(() => authStore.getToken);
  const getUser = computed(()=> userStore.getUser )
  const isAuthenticated = computed(() => authStore.isAuthenticated);

  const $userDataSet = {
    // setToken(accessToken: string | null, refreshToken: string | null) {
    //   authStore.setToken(accessToken);
    //   authStore.setRefreshToken(refreshToken);
    // },
    setPhone(phone : string) {
      userStore.setPhone(phone);
    },
    setUuid(uuid : string) {
      userStore.setUuid(uuid);
     
    },
    getUuid() {
     return userStore.watchUuid;
    },
    getPhone() {
      return userStore.watchPhone;
     },
    setToken(accessToken: string | null) {
      authStore.setAccessToken(accessToken);
    },
    setUser(user: User.UserNewBare | null) {
      userStore.setUser(user);
    },
    setHaveWorkers(val : boolean) {
      userStore.setHaveWorkers(val);
    },
    logout() {
      this.setToken(null, null);
      userStore.clearUser();
    },
  };

  return {
    // accessToken,
    // refreshToken,
    // isAuthenticated,
    $userDataSet,
    accessToken,
    isAuthenticated,
    getUser
    // role,
    // fioFull,
    // isSimpleUser,
    // isRoot,
    // isLibrarian,
    // isCourier,
    // roleName,
  };
}
