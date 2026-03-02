import { defineStore } from 'pinia';

export type ComponentSettings = Array<unknown> | object | string | number | null;

export interface VisibleColumnItem {
  name: string;
  label: string;
  show: boolean;
}

export interface SettingStoreInterface {
  settings: Record<string, ComponentSettings>;
}

export const useSettingsStore = defineStore('settings', {
  persist: !process.env.SERVER,

  state: (): SettingStoreInterface => ({
    settings: {},
  }),

  getters: {
    restore: (state) => state.settings,
  },

  actions: {
    save(key: string, value: ComponentSettings) {
      this.settings[key] = value;
    },
  },
});
