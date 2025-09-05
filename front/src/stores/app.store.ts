import { defineStore } from 'pinia';
import { Crm } from 'src/declarations/responses/crm';
import { IntercomCall } from 'src/declarations/responses/intercom-call';
export interface AppStateInterface {
  collapseSidebar: boolean;
  miniCollapseSidebar: boolean;
  activeTabMenuIndex: string;
  intercomData: Crm.IntercomBrief;
  stownDevice: IntercomCall.BlockDevice;
}

export const useAppStore = defineStore('app', {
  persist: true,

  state: (): AppStateInterface => ({
    collapseSidebar: false,
    miniCollapseSidebar: false,
    activeTabMenuIndex: '1',
    intercomData: null,
    stownDevice: null,
  }),

  getters: {
    getCollapseSidebar: (state) => state.collapseSidebar,
    getMiniCollapseSidebar: (state) => state.miniCollapseSidebar,
    getActiveTabMenuIndex: (state) => state.activeTabMenuIndex,
    getIntercomData: (state) => state.intercomData,
    getStownDevice: (state) => state.stownDevice,
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
     setIntercomData(val: Crm.IntercomBrief) {
      this.intercomData = val;
    },
    setStownDevice(val: IntercomCall.BlockDevice) {
      this.stownDevice = val;
    },
  },
});
