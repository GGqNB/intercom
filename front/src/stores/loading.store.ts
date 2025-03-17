import { defineStore } from 'pinia';

export interface LoadingStateInterface {
  loading: boolean; // Loading используемый при ожидании ответа от сервера или выполнении каких-то общих действий
  routeLoading: boolean; // Loading используемый при переходе между компонентами
  actionLoading: boolean; // Loading используемый для блокировки определенных управляющих элементов (кнопок например, когда запускаем экспорт в эксель)
}

export const useLoadingStore = defineStore('loading', {
  persist: false,

  state: (): LoadingStateInterface => ({
    loading: false,
    routeLoading: false,
    actionLoading: false,
  }),

  getters: {
    getLoading: (state: LoadingStateInterface) => state.loading,
    getRouteLoading: (state: LoadingStateInterface) => state.routeLoading,
    getActionLoading: (state: LoadingStateInterface) => state.actionLoading,
  },

  actions: {
    setLoading(val: boolean) {
      this.loading = val;
    },
    setRouteLoading(val: boolean) {
      this.routeLoading = val;
    },
    setActionLoading(val: boolean) {
      this.actionLoading = val;
    },
  },
});
