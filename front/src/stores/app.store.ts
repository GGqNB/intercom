import { defineStore } from 'pinia';
import { Crm } from 'src/declarations/responses/crm';
export interface AppStateInterface {
  collapseSidebar: boolean;
  miniCollapseSidebar: boolean;
  activeTabMenuIndex: string;
  intercomData: Crm.CityBrief;
}

export const useAppStore = defineStore('app', {
  persist: true,

  state: (): AppStateInterface => ({
    collapseSidebar: false,
    miniCollapseSidebar: false,
    activeTabMenuIndex: '1',
    intercomData: null,
  }),

  getters: {
    getCollapseSidebar: (state) => state.collapseSidebar,
    getMiniCollapseSidebar: (state) => state.miniCollapseSidebar,
    getActiveTabMenuIndex: (state) => state.activeTabMenuIndex,
    getIntercomData: (state) => state.intercomData,
  },

  actions: {
    setCollapseSidebar(val: boolean) {
      this.collapseSidebar = val;
    },
    setMiniCollapseSidebar(val: boolean) {
      this.miniCollapseSidebar = val;
    },
    setActiveTabMenuIndex(val: string) {
      this.activeTabMenuIndex = val;
    },
     setIntercomData(val: Crm.CityBrief) {
      this.intercomData = val;
    },
  },
});
