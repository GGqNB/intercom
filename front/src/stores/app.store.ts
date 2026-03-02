import { defineStore } from 'pinia';
import { Crm } from 'src/declarations/responses/crm';
import { IntercomCall } from 'src/declarations/responses/intercom-call';
export interface AppStateInterface {
  collapseSidebar: boolean;
  miniCollapseSidebar: boolean;
  activeTabMenuIndex: string;
  intercomData: Crm.IntercomBrief;
  stownDevice: IntercomCall.BlockDevice;
  adminBar: boolean;
  localUrlControlBoard: string;
  localIdLock: string;
}

export const useAppStore = defineStore('app', {
  persist: true,

  state: (): AppStateInterface => ({
    collapseSidebar: false,
    miniCollapseSidebar: false,
    activeTabMenuIndex: '1',
    intercomData: null,
    stownDevice: null,
    adminBar: false,
    localUrlControlBoard: '',
    localIdLock: '',
  }),

  getters: {
    getCollapseSidebar: (state) => state.collapseSidebar,
    getMiniCollapseSidebar: (state) => state.miniCollapseSidebar,
    getActiveTabMenuIndex: (state) => state.activeTabMenuIndex,
    getIntercomData: (state) => state.intercomData,
    getStownDevice: (state) => state.stownDevice,
    getAdminBar: (state) => state.adminBar,
    getlocalUrlControlBoard: (state) => state.localUrlControlBoard,
    getLocalIdLock: (state) => state.localIdLock,
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
    setAdminBar(val: boolean) {
      this.adminBar = val;
    },
     setlocalUrlControlBoard(val: string) {
      this.localUrlControlBoard = val;
    },
      setLocalIdLock(val: string) {
      this.localIdLock = val;
    },
  },
});
