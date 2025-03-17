import { computed } from 'vue';
import { useLoadingStore } from 'src/stores/loading.store';

export function useLoading() {
  const loadingStore = useLoadingStore();

  const action = {
    show() {
      loadingStore.setActionLoading(true);
    },
    hide() {
      loadingStore.setActionLoading(false);
    },
    state: computed(() => loadingStore.getActionLoading),
  };

  const route = {
    show() {
      loadingStore.setRouteLoading(true);
    },
    hide() {
      loadingStore.setRouteLoading(false);
    },
    state: computed(() => loadingStore.getRouteLoading),
  };

  const general = {
    show() {
      loadingStore.setLoading(true);
    },
    hide() {
      loadingStore.setLoading(false);
    },
    state: computed(() => loadingStore.getLoading),
  };

  return {
    action,
    route,
    general,
  };
}