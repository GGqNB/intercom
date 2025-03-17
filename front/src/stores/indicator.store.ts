// Ваш файл с хранилищем useUserStore
import { defineStore } from 'pinia';

export interface IndicatorStateInterface {
  activeWifi: boolean;
  activePhone: boolean;
  pastNetworks: Array<string>;
  currentNetwork: string;
}

export const useIndicatorStore = defineStore('indicator', {
  persist: true,

  state: (): IndicatorStateInterface => ({
    activeWifi: false,
    activePhone: false,
    pastNetworks: [],
    currentNetwork: '',
  }),

  getters: {
    getActiveWifi: (state: IndicatorStateInterface) => state.activeWifi,
    getActivePhone: (state: IndicatorStateInterface) => state.activePhone,
    getPastNetworks: (state: IndicatorStateInterface) => state.pastNetworks,
    getCurrentNetwork: (state: IndicatorStateInterface) => state.currentNetwork,
    watchActiveWifi: (state): boolean => {
      return state.activeWifi;
    },
    watchActivePhone: (state): boolean => {
      return state.activePhone;
    },
    watchPastNetworks: (state): Array<string> => {
      return state.pastNetworks;
    },
    watchCurrentNetwork: (state): string => {
      return state.currentNetwork;
    }
  },

  actions: {
    setActivePhone(val : boolean) {
      this.activePhone = val;
    },
    setActiveWifi(val : boolean) {
      this.activeWifi = val;
    },
    setPastNetworks(val : string) {
      this.pastNetworks.push(val);
    },
    setCurrentNetwork(val : string) {
      this.currentNetwork = val;
    },
  }, 
});
