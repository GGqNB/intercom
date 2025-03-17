// Ваш файл с хранилищем useUserStore
import { defineStore } from 'pinia';
import { User } from 'src/declarations/responses/user';

export interface UserStateInterface {
  phone: string;
  uuid: string;
  user: User.UserNewBare | null;
}

export const useUserStore = defineStore('user', {
  persist: true,

  state: (): UserStateInterface => ({
    phone: '',
    uuid: '',
    user: null,
  }),

  getters: {
    getUser: (state) => state.user,
    getPhone: (state: UserStateInterface) => state.phone,
    getUuid: (state: UserStateInterface) => state.uuid,
    watchUuid: (state): string => {
      return state.uuid;
    },
    watchPhone: (state): string => {
      return state.phone;
    }
  },

  actions: {
    setPhone(val: string) {
      this.phone = val;
    },
    setUuid(val: string) {
      this.uuid = val;
    },
    setUser(userData: User.UserNewBare | null) {
      this.user = userData;
    },
    setHaveWorkers(val : boolean) {
      this.haveWorkers = val;
    },
    clearUser() {
      this.user = null;
      this.haveWorkers = false;
    },
  },
});
