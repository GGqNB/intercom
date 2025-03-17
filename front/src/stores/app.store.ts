import { defineStore } from 'pinia';

export interface AppStateInterface {
  collapseSidebar: boolean;
  miniCollapseSidebar: boolean;
  activeTabMenuIndex: string;
}

export const useAppStore = defineStore('app', {
  persist: true,

  state: (): AppStateInterface => ({
    collapseSidebar: false,
    miniCollapseSidebar: false,
    activeTabMenuIndex: '1',
  }),

  getters: {
    getCollapseSidebar: (state) => state.collapseSidebar,
    getMiniCollapseSidebar: (state) => state.miniCollapseSidebar,
    getActiveTabMenuIndex: (state) => state.activeTabMenuIndex,
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
  },
});
